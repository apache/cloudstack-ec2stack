#!/usr/bin/env python
# encoding: utf-8

"""This module contains functions for handling the execution of requests
against Cloudstack.
"""

from urllib import urlencode, quote_plus
from hashlib import sha1
from base64 import b64encode
import hmac
import json
import time

from flask import current_app, abort
import requests

from ec2stack import helpers


def make_request(args):
    """
    Makes a request to Cloudstack.

    @param args: Request Payload.
    @return: Response.
    """
    args['apikey'] = helpers.get('AWSAccessKeyId')
    args['response'] = 'json'

    secretkey = helpers.get_secretkey()

    request_url = _generate_request_url(args, secretkey)

    response = requests.get(request_url)

    response_data = json.loads(
        response.text,
        object_hook=helpers.normalize_dict_keys
    )
    current_app.logger.debug(
        'request url:' + str(request_url) +
        'status code: ' + str(response.status_code) +
        json.dumps(response_data, indent=4, separators=(',', ': '))
    )

    if response.status_code in [401, 432]:
        abort(400)
    else:
        return response_data


def make_request_async(args, poll_period=2, timeout=3600):
    """
    Makes an async request to Cloudstack.

    @param args: Request payload.
    @param poll_period: Poll time period.
    @param timeout: Time before giving up on the request.
    @return: Response.
    """
    response = make_request(args)

    responsekey = response.keys()[0]

    if 'jobid' in response[responsekey]:
        args = {'command': 'queryAsyncJobResult',
                'jobid': response[responsekey]['jobid']}

        response = make_request(args)

        response = response['queryasyncjobresultresponse']
        job_status = response['jobstatus']

        if job_status in [1, 2]:
            return response['jobresult']
        elif job_status == 0:
            time.sleep(poll_period)
            timeout -= poll_period
            return make_request_async(args, poll_period=poll_period,
                                      timeout=timeout)
    else:
        return response[responsekey]


def _generate_request_url(args, secretkey):
    """
    Generates a request URL.

    @param args: Request payload.
    @param secretkey: User's secret key.
    @return: Request URL.
    """
    keys = sorted(args.keys())
    values = map(args.get, keys)

    request_url = urlencode(
        list(
            zip(keys, values)
        )
    )

    request_url = request_url.replace('%5B', '[')
    request_url = request_url.replace('%5D', ']')

    signature = _generate_signature(request_url, secretkey)

    request_url += '&signature=%s' % signature

    request_url = "%s://%s:%s%s?%s" % (
        current_app.config['CLOUDSTACK_PROTOCOL'],
        current_app.config['CLOUDSTACK_HOST'],
        current_app.config['CLOUDSTACK_PORT'],
        current_app.config['CLOUDSTACK_PATH'],
        request_url
    )

    return request_url


def _generate_signature(request_url, secretkey):
    """
    Generates a Signature.

    @param request_url: Request URL.
    @param secretkey: User's secret key.
    @return: Signature.
    """
    signature = request_url.lower().replace('+', '%20')

    signature = hmac.new(
        key=bytes(secretkey),
        msg=bytes(signature),
        digestmod=sha1,
    ).digest()

    signature = b64encode(signature)
    signature = quote_plus(signature)

    return signature
