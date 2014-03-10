#!/usr/bin/env python
# encoding: utf-8

"""This module contains functions for handling requests in relation to password
data.
"""

from ec2stack import helpers, errors
from ec2stack.providers.cloudstack import requester


@helpers.authentication_required
def get_password_data():
    """
    Gets the password for a specified instance.

    @return: Response.
    """
    helpers.require_parameters(['InstanceId'])
    response = _get_password_data_request()
    return _get_password_data_format_response(response)


def _get_password_data_request():
    """
    Request to get password.

    @return: Response.
    """
    args = {'command': 'getVMPassword', 'id': helpers.get('InstanceId')}

    response = requester.make_request(args)

    response = response['getvmpasswordresponse']

    return response


def _get_password_data_format_response(response):
    """
    Generate a response for get password request.

    @param response: Cloudstack response.
    @return: Response
    """
    if 'errortext' in response:
        errors.invalid_instance_id()
    else:
        response = response['password']
        return {
            'template_name_or_list': 'password.xml',
            'response_type': 'GetPasswordDataResponse',
            'response': response
        }
