#!/usr/bin/env python
# encoding: utf-8

import os
import hmac
import hashlib
from uuid import uuid1 as uuid
from base64 import b64encode
from urllib import urlencode
from functools import wraps

from flask import request, make_response, render_template

from ec2stack.services import USERS
from ec2stack.core import Ec2stackError
from ec2stack import errors


def get(item, data=None):
    if data is None:
        data = request.form

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


def normalize_dict_keys(dct):
    return dict((key.lower(), value) for key, value in dct.iteritems())


def require_parameters(required_parameters):
    for parameter in required_parameters:
        if not contains_parameter(parameter):
            errors.missing_paramater(parameter)


def require_atleast_one_parameter(parameters):
    parameter = None
    for parameter in parameters:
        if contains_parameter(parameter):
            return

    errors.missing_paramater(parameter)


def error_to_aws(response, error_map):
    for errortext, error_function in error_map.iteritems():
        if errortext in response['errortext']:
            error_function()


def contains_parameter(parameter, data=None):
    if data is None:
        data = request.form

    return (get(parameter, data)) is not None


def contains_parameter_with_keyword(key):
    return len(get_request_parameter_keys(key)) >= 1


def get_request_parameter_keys(prefix, data=None):
    if data is None:
        data = request.form

    return [item for item in data if prefix in item]


def get_secretkey(data=None):
    if data is None:
        data = request.form

    apikey = get('AWSAccessKeyId', data)
    user = USERS.get(apikey)

    if user is None:
        raise Ec2stackError(
            '401',
            'AuthFailure',
            'Unable to find a secret key for %s, please insure you registered'
            % apikey
        )

    return user.secretkey.encode('utf-8')


def _valid_signature_method():
    signature_method = get('SignatureMethod')
    if signature_method not in ['HmacSHA1', 'HmacSHA256']:
        raise Ec2stackError(
            '400',
            'InvalidParameterValue',
            'Value (%s) for parameter SignatureMethod is invalid. '
            'Unknown signature method.' % signature_method
        )


def _valid_signature_version():
    signature_version = get('SignatureVersion')
    if signature_version != '2':
        raise Ec2stackError(
            '400',
            'InvalidParameterValue',
            'Value (%s) for parameter SignatureVersion is invalid.'
            'Valid Signature versions are 2.'
            % signature_version
        )


def _valid_signature():
    signature = get('Signature')
    generated_signature = generate_signature()

    if signature != generated_signature:
        raise Ec2stackError(
            '401',
            'AuthFailure',
            'AWS was not able to validate the provided access credentials.'
        )


def generate_signature(data=None, method=None, host=None):
    if data is None:
        data = request.form

    secretkey = get_secretkey(data)
    request_string = _get_request_string(data, method, host)

    if get('SignatureMethod') == 'HmacSHA1':
        digestmod=hashlib.sha1
    else:
        digestmod=hashlib.sha256

    signature = hmac.new(
        key=secretkey,
        msg=bytes(request_string),
        digestmod=digestmod
    ).digest()

    signature = b64encode(signature)

    return signature


def _get_request_string(data, method=None, host=None):
    if method is None:
        method = request.method
    if host is None:
        host = request.host
    query_string = _get_query_string(data)

    request_string = '\n'.join(
        [method, host, '/', query_string]
    )

    return request_string.encode('utf-8')


def _get_query_string(data):
    params = {}
    for param in data:
        if param != 'Signature':
            params[param] = data[param]

    keys = sorted(params.keys())
    values = map(params.get, keys)

    query_string = urlencode(
        list(
            zip(keys, values)
        )
    )

    query_string = query_string.replace('+', '%20')

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
    return _create_response(response, int(code))


def successful_response(**kwargs):
    content = render_template(request_id=uuid(), **kwargs)
    response = make_response(content)
    return _create_response(response, '200')


def _create_response(response, code):
    response.headers['Content-Type'] = 'application/xml'
    response.status_code = int(code)
    return response


def read_file(name):
    filepath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '../',
        name
    )
    data = open(filepath)
    return data.read()
