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

"""This module provides functions to register AWSAccessKeyIds and AWSSecretKeys.
"""

import argparse
from xml.dom.minidom import parseString as xmlparse

import requests


def _generate_args(description):
    """
    Generates the base application with required parameters.

    @param description: Description of the command.
    @return: The args associated with the command.
    """
    parser = argparse.ArgumentParser(
        description=description
    )

    parser.add_argument(
        'ec2stack_server_address',
        help='The address of the ec2stack server http://localhost:5000'
    )

    parser.add_argument(
        'AWSAccessKeyId',
        help='Your Cloudstack API Key'
    )

    parser.add_argument(
        'AWSSecretKey',
        help='Your Cloudstack Secret Key'
    )

    args = parser.parse_args()

    return vars(args)


def register():
    """
    Entry point for registering an api key and secret key.

    """
    args = _generate_args(
        'Command line utility for registering a secret key with ec2stack'
    )
    args['Action'] = 'RegisterSecretKey'
    _execute_request(args)


def remove():
    """
    Entry point for removing an api key and secret key.

    """
    args = _generate_args(
        'Command line utility for removing a secret key from ec2stack'
    )
    args['Action'] = 'RemoveSecretKey'
    _execute_request(args)


def _execute_request(args):
    """
    Executes the register/remove request.

    @param args: Request payload.
    """
    host = args.pop('ec2stack_server_address')
    response = requests.post(host, args)
    response = xmlparse(response.text)
    message = response.getElementsByTagName('Message')[0].firstChild.nodeValue
    print message
