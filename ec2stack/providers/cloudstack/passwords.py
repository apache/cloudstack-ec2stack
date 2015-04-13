#!/usr/bin/env python
# encoding: utf-8
#
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.
#

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
