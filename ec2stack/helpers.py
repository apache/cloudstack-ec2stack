#!/usr/bin/env python
# encoding: utf-8


import hmac
import hashlib
from uuid import uuid1 as uuid
from base64 import b64encode
from urllib import urlencode
from functools import wraps

from flask import request, make_response, render_template

from .services import USERS
from .core import Ec2stackError


def get(item, data):
    if item in data:
        return data[item]
    else:
        return None


def authentication_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            required_params = {'Action', 'AWSAccessKeyId', 'Signature',
                               'SignatureMethod', 'SignatureVersion',
                               'Timestamp', 'Version'}
            _require_parameters(required_params)

            _valid_signature_method()
            _valid_signature_version()
            _valid_signature()
        except Ec2stackError as err:
            response = error_response(err.error, err.message)
            return response
        return f(*args, **kwargs)

    return decorated


def _require_parameters(required_parameters):
    for parameter in required_parameters:
        if (get(parameter, request.form)) is None:
            raise Ec2stackError(
                'MissingParameter',
                'The request must contain the parameter %s' % parameter
            )


def _valid_signature_method():
    signature_method = get('SignatureMethod', request.form)
    if signature_method not in ['HmacSHA1', 'HmacSHA256']:
        raise Ec2stackError(
            'InvalidParameterValue',
            'Value (%s) for parameter SignatureMethod is invalid. '
            'Unknown signature method.' % signature_method
        )


def _valid_signature_version():
    signature_version = get('SignatureVersion', request.form)
    if signature_version != '2':
        raise Ec2stackError(
            'InvalidParameterValue',
            'Value (%s) for parameter SignatureVersion is invalid.'
            'Valid Signature versions are 2.'
            % signature_version
        )


def _valid_signature():
    apikey = get('AWSAccessKeyId', request.form)
    secretkey = USERS.get(apikey)

    params = {}

    for param in request.form:
        if param != 'Signature':
            params[param] = request.form[param]

    _generate_signature(secretkey)

    if secretkey is None:
        raise Ec2stackError(
            'AuthFailure',
            'Unable to find a secret key for %s, please insure you registered'
            % apikey
        )


def _generate_signature(secretkey):
    request_string = _get_request_string()
    signature = hmac.new(
        key=secretkey,
        msg=bytes(request_string),
        digestmod=hashlib.sha256
    ).digest()

    signature = b64encode(signature)

    print signature

    return signature


def _get_request_string():
    query_string = _get_query_string()
    print query_string
    request_string = '\n'.join(
        [request.method, request.host, '/', query_string]
    )
    print request_string
    return request_string.encode('utf-8')


def _get_query_string():
    params = {}
    for param in request.form:
        if param != 'Signature':
            params[param] = request.form[param]

    keys = sorted(params.keys())
    values = map(params.get, keys)

    query_string = urlencode(
        list(
            zip(keys, values)
        )
    )

    return query_string


def error_response(error, message):
    response = make_response(
        render_template(
            "generic_error.xml",
            error=error,
            message=message,
            requestid=uuid()
        )
    )
    response.headers['Content-Type'] = 'application/xml'
    response.status_code = 400
    return response
