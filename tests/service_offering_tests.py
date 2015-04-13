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

import json

import mock

from ec2stack.helpers import read_file, generate_signature
from . import Ec2StackAppTestCase


class ServiceOfferingsTestCase(Ec2StackAppTestCase):

    def test_get_service_offering(self):
        data = self.get_example_data()
        data['Action'] = 'RunInstances'
        data['ImageId'] = 'a32d70ee-95e4-11e3-b2e4-d19c9d3e5e1d'
        data['InstanceType'] = 'Small Instance'
        data['MinCount'] = '0'
        data['MaxCount'] = '0'
        data['SecurityGroupId.1'] = 'example-security-group-id'
        data['SecurityGroup.1'] = 'example-security-group-name'
        data['KeyName'] = 'example-ssh-key-name'
        data['UserData'] = 'example-user-data'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_run_instance.json'
        )
        get.return_value.status_code = 200

        get_service_offering = mock.Mock()
        get_service_offering.return_value = json.loads(read_file(
            'tests/data/service_offerings_search.json'
        ))

        get_zone = mock.Mock()
        get_zone.return_value = json.loads(read_file(
            'tests/data/zones_search.json'
        ))

        with mock.patch('requests.get', get):
            with mock.patch(
                    'ec2stack.providers.cloudstack.describe_items_request',
                    get_service_offering
            ):
                with mock.patch(
                        'ec2stack.providers.cloudstack.zones.get_zone',
                        get_zone
                ):
                    response = self.post(
                        '/',
                        data=data
                    )

        self.assert_ok(response)
        assert 'RunInstancesResponse' in response.data

    def test_get_service_offering_invalid_name(self):
        data = self.get_example_data()
        data['Action'] = 'RunInstances'
        data['ImageId'] = 'a32d70ee-95e4-11e3-b2e4-d19c9d3e5e1d'
        data['InstanceType'] = 'invalid-instance-type'
        data['MinCount'] = '0'
        data['MaxCount'] = '0'
        data['SecurityGroupId.1'] = 'example-security-group-id'
        data['SecurityGroup.1'] = 'example-security-group-name'
        data['KeyName'] = 'example-ssh-key-name'
        data['UserData'] = 'example-user-data'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_run_instance.json'
        )
        get.return_value.status_code = 200

        get_service_offering = mock.Mock()
        get_service_offering.return_value = json.loads(read_file(
            'tests/data/service_offerings_search.json'
        ))

        get_zone = mock.Mock()
        get_zone.return_value = json.loads(read_file(
            'tests/data/zones_search.json'
        ))

        with mock.patch('requests.get', get):
            with mock.patch(
                    'ec2stack.providers.cloudstack.describe_items_request',
                    get_service_offering
            ):
                with mock.patch(
                        'ec2stack.providers.cloudstack.zones.get_zone',
                        get_zone
                ):
                    response = self.post(
                        '/',
                        data=data
                    )

        self.assert_bad_request(response)
        assert 'InvalidServiceOffering.NotFound' in response.data
