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
        required_params = {'Action', 'AWSAccessKeyId', 'Signature',
                           'SignatureMethod', 'SignatureVersion', 'Timestamp',
                           'Version'}
        require_parameters(required_params)
        _valid_signature_method()
        _valid_signature_version()
        _valid_signature()
        return f(*args, **kwargs)
    return decorated


def require_parameters(required_parameters):
    for parameter in required_parameters:
        if (get(parameter, request.form)) is None:
            raise Ec2stackError(
                '400',
                'MissingParameter',
                'The request must contain the parameter %s' % parameter
            )


def _valid_signature_method():
    signature_method = get('SignatureMethod', request.form)
    if signature_method not in ['HmacSHA1', 'HmacSHA256']:
        raise Ec2stackError(
            '400',
            'InvalidParameterValue',
            'Value (%s) for parameter SignatureMethod is invalid. '
            'Unknown signature method.' % signature_method
        )


def _valid_signature_version():
    signature_version = get('SignatureVersion', request.form)
    if signature_version != '2':
        raise Ec2stackError(
            '400',
            'InvalidParameterValue',
            'Value (%s) for parameter SignatureVersion is invalid.'
            'Valid Signature versions are 2.'
            % signature_version
        )


def _valid_signature():
    signature = get('Signature', request.form)
    generated_signature = _generate_signature()

    print 'Supplied signature: ' + signature
    print 'Generated signature: ' + generated_signature

    if signature != generated_signature:
        raise Ec2stackError(
            '401',
            'AuthFailure',
            'AWS was not able to validate the provided access credentials.'
        )


def _get_secretkey():
    apikey = get('AWSAccessKeyId', request.form)
    user = USERS.get(apikey)

    if user is None:
        raise Ec2stackError(
            '401',
            'AuthFailure',
            'Unable to find a secret key for %s, please insure you registered'
            % apikey
        )

    return user.secretkey.encode('utf-8')


def _generate_signature():
    secretkey = _get_secretkey()
    request_string = _get_request_string()

    signature = hmac.new(
        key=secretkey,
        msg=bytes(request_string),
        digestmod=hashlib.sha256
    ).digest()

    signature = b64encode(signature)

    return signature


def _get_request_string():
    query_string = _get_query_string()

    request_string = '\n'.join(
        [request.method, request.host, '/', query_string]
    )

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


def error_response(code, error, message):
    response = make_response(
        render_template(
            "generic_error.xml",
            response_type='Response',
            error=error,
            message=message,
            request_id=uuid()
        )
    )
    response.headers['Content-Type'] = 'application/xml'
    response.status_code = int(code)
    return response


def successful_response(content):
    response = make_response(content)
    response.headers['Content-Type'] = 'application/xml'
    response.status_code = 200
    return response
