#!/usr/bin/env python
# encoding: utf-8

"""This module contains helper functions used across the package namespace.
"""

import os
import hmac
import hashlib
from uuid import uuid1 as uuid
from base64 import b64encode
from urllib import urlencode
from functools import wraps

from flask import request, make_response, render_template

from ec2stack.services import USERS
from ec2stack import errors


def get(item, data=None):
    """
    Gets the specified item in the given data.

    @param item: Key of the item.
    @param data: Data the item is in.
    @return: Item if found, otherwise None.
    """
    if data is None:
        data = request.form

    if item in data:
        return data[item]
    else:
        return None


def authentication_required(f):
    """
    Check that the given signature is valid.

    @param f: Function to wrap around.
    @return: Result of signature check.
    """

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
    """
    Normalizes all keys in the given dictionary.

    @param dct: Dictionary to normalize.
    @return: Dictionary normalized.
    """
    return dict((key.lower(), value) for key, value in dct.iteritems())


def require_parameters(required_parameters):
    """
    Checks that the given array of parameters are present.

    @param required_parameters: Array of required parameters.
    """
    for parameter in required_parameters:
        if not contains_parameter(parameter):
            errors.missing_parameter(parameter)


def require_atleast_one_parameter(parameters):
    """
    Require atleast one parameter.

    @param parameters: Array of possible parameters.
    @return: void.
    """
    parameter = None
    for parameter in parameters:
        if contains_parameter(parameter):
            return

    errors.missing_parameter(parameter)


def contains_parameter(parameter, data=None):
    """
    Checks if the parameter is contained within the given data.

    @param parameter: Parameter to check.
    @param data: Data to check in.
    @return: Boolean.
    """
    if data is None:
        data = request.form

    return (get(parameter, data)) is not None


def contains_parameter_with_keyword(prefix):
    """
    Checks if the request contains parameters with the given prefix.

    @param prefix: Prefix of parameters.
    @return: Boolean.
    """
    return len(get_request_parameter_keys(prefix)) >= 1


def get_request_parameter_keys(prefix, data=None):
    """
    Gets all parameters containing prefix.

    @param prefix: Prefix of parameters.
    @param data: Data to search.
    @return: List of matching parameters.
    """
    if data is None:
        data = request.form

    return [item for item in data if prefix in item]


def get_secretkey(data=None):
    """
    Get the secret key from the database.

    @param data: Data to get the API KEY from.
    @return: The users secret key.
    @raise Ec2stackError: if the secretkey is not found.
    """
    if data is None:
        data = request.form

    apikey = get('AWSAccessKeyId', data)
    user = USERS.get(apikey)

    if user is None:
        errors.apikey_not_found(apikey)

    return user.secretkey.encode('utf-8')


def _valid_signature_method():
    """
    Check that the given signature method is correct.

    @raise Ec2stackError: if the signature method is invalid.
    """
    signature_method = get('SignatureMethod')
    if signature_method not in ['HmacSHA1', 'HmacSHA256']:
        errors.invalid_parameter_value(
            'Value (%s) for parameter SignatureMethod is invalid. '
            'Unknown signature method.' % signature_method
        )


def _valid_signature_version():
    """
    Checks that the given signature version is correct.

    @raise Ec2stackError: if the signature version is invalid.
    """
    signature_version = get('SignatureVersion')
    if signature_version != '2':
        errors.invalid_parameter_value(
            'Value (%s) for parameter SignatureVersion is invalid.'
            'Valid Signature versions are 2.'
            % signature_version
        )


def _valid_signature():
    """
    Checks that the given signature matches the signature generated.

    @raise Ec2stackError: if the signature does not match the generated
                          signature.
    """
    signature = get('Signature')
    generated_signature = generate_signature()

    if signature != generated_signature:
        errors.authentication_failure()


def generate_signature(data=None, method=None, host=None, path=None):
    """
    Generates a signature.

    @param data: Data of the request.
    @param method: HTTP method used.
    @param host: HTTP post.
    @param path: HTTP hort.
    @return: A signature.
    """
    if data is None:
        data = request.form

    signature_type = get('SignatureMethod', data)

    secretkey = get_secretkey(data)
    request_string = _get_request_string(data, method, host, path)

    if signature_type == 'HmacSHA1':
        digestmod = hashlib.sha1
    else:
        digestmod = hashlib.sha256

    signature = hmac.new(
        key=secretkey,
        msg=bytes(request_string),
        digestmod=digestmod
    ).digest()

    signature = b64encode(signature)

    return signature


def _get_request_string(data, method=None, host=None, path=None):
    """
    Creates the request string.

    @param data: Data of the request.
    @param method: HTTP method used.
    @param host: HTTP host.
    @param path: HTTP path.
    @return: Request string.
    """
    if method is None:
        method = request.method
    if host is None:
        host = request.host
    if path is None:
        path = request.path

    query_string = _get_query_string(data)

    request_string = '\n'.join(
        [method, host, path, query_string]
    )

    return request_string.encode('utf-8')


def _get_query_string(data):
    """
    Creates the query string.

    @param data: Data of the request.
    @return: Query String.
    """
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
    """
    Returns a error response.

    @param code: Status code.
    @param error: Error type.
    @param message: Error message.
    @return: Response.
    """
    response = make_response(
        render_template(
            'generic_error.xml',
            response_type='Response',
            error=error,
            message=message,
            request_id=uuid()
        )
    )
    return _create_response(response, int(code))


def successful_response(**kwargs):
    """
    Returns a successful response.

    @param kwargs: Parameters to render the template with.
    @return: Response.
    """
    api_version = str(get("Version"))
    content = render_template(request_id=uuid(), api_version=api_version, **kwargs)
    response = make_response(content)
    return _create_response(response, '200')


def _create_response(response, code):
    """
    Creates a response.

    @param response: Response to use.
    @param code: Status code of the response.
    @return: Response.
    """
    response.headers['Content-Type'] = 'application/xml'
    response.status_code = int(code)
    return response


def read_file(name):
    """
    Reads the given file.

    @param name: Filename of the file to read.
    @return: Contents of the file.
    """
    filepath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '../',
        name
    )
    data = open(filepath)
    return data.read()
