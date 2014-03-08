#!/usr/bin/env python
# encoding: utf-8

from ec2stack import helpers
from ec2stack.core import Ec2stackError
from ec2stack.providers.cloudstack import requester


@helpers.authentication_required
def get_password_data():
    """


    @return:
    """
    helpers.require_parameters(['InstanceId'])
    response = _get_password_data_request()
    return _get_password_data_format_response(response)


def _get_password_data_request():
    """


    @return:
    """
    args = {'command': 'getVMPassword', 'id': helpers.get('InstanceId')}

    response = requester.make_request(args)

    response = response['getvmpasswordresponse']

    return response


def _get_password_data_format_response(response):
    """

    @param response:
    @return: @raise Ec2stackError:
    """
    instanceid = helpers.get('InstanceId')
    if 'errortext' in response:
        raise Ec2stackError(
            '400',
            'InvalidInstanceID.NotFound',
            'The instance ID \'%s\' does not exist.' % instanceid
        )
    else:
        response = response['password']
        return {
            'template_name_or_list': 'password.xml',
            'response_type': 'GetPasswordDataResponse',
            'response': response
        }
