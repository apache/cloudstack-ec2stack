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
from base64 import b64encode

import mock
import json

from ec2stack.helpers import read_file, generate_signature
from . import Ec2StackAppTestCase


class VpcTestCase(Ec2StackAppTestCase):

    def test_create_vpc(self):
        data = self.get_example_data()
        data['Action'] = 'CreateVpc'
        data['CidrBlock'] = '192.168.0.0/24'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get_zone = mock.Mock()
        get_zone.return_value = json.loads(read_file(
            'tests/data/zones_search.json'
        ))

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_create_vpc.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            with mock.patch(
                'ec2stack.providers.cloudstack.zones.get_zone',
                get_zone
            ):
                response = self.post(
                    '/',
                    data=data
                )

        self.assert_ok(response)
        assert 'CreateVpcResponse' in response.data

    def test_create_vpc_invalid_cidr(self):
        data = self.get_example_data()
        data['Action'] = 'CreateVpc'
        data['CidrBlock'] = '192.168.0.0/33'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get_zone = mock.Mock()
        get_zone.return_value = json.loads(read_file(
            'tests/data/zones_search.json'
        ))

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/invalid_create_vpc_invalid_cidr.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            with mock.patch(
                'ec2stack.providers.cloudstack.zones.get_zone',
                get_zone
            ):
                response = self.post(
                    '/',
                    data=data
                )

        self.assert_bad_request(response)
        assert 'InvalidVpcRange' in response.data

    def test_describe_vpcs(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeVpcs'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_vpcs.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'DescribeVpcsResponse' in response.data

    def test_describe_vpc_by_name(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeVpcs'
        data['VpcId'] = 'examplevpc'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_vpc.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'DescribeVpcsResponse' in response.data
        assert 'examplevpc' in response.data


    def test_describe_vpc_by_name_invalid_name(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeVpcs'
        data['VpcId'] = 'invalidevpc'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_vpc.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert 'InvalidVpcID.NotFound' in response.data

    def test_delete_vpc(self):
        data = self.get_example_data()
        data['Action'] = 'DeleteVpc'
        data['VpcId'] = 'Test'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_delete_vpc.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'DeleteVpcResponse' in response.data