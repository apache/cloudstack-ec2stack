#!/usr/bin/env python
# encoding: utf-8

import urllib
from urllib import urlencode
import hashlib
import base64
import hmac
import json

from flask import current_app, abort
import requests


def make_request(args, secretkey):
    args['response'] = 'json'
    request_url = _generate_request_url(args, secretkey)

    response = requests.get(request_url)
    cloudstack_response = json.loads(response.text)

    current_app.logger.debug(
        'status code: ' + str(response.status_code) +
        json.dumps(cloudstack_response, indent=4, separators=(',', ': '))
    )

    if response.status_code in [531, 401, 431]:
        abort(response.status_code)
    else:
        return cloudstack_response


def _generate_request_url(args, secretkey):
    keys = sorted(args.keys())
    values = map(args.get, keys)

    request_url = urlencode(
        list(
            zip(keys, values)
        )
    )

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
    signature = request_url.lower().replace('+', '%20')

    signature = urllib.quote_plus(base64.encodestring(
        hmac.new(bytes(secretkey), 
        bytes(signature), 
        hashlib.sha1
    ).digest()).strip())
    
    return signature
