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

import mock

from ec2stack.helpers import read_file, generate_signature
from . import Ec2StackAppTestCase


class ImagesTestCase(Ec2StackAppTestCase):

    def test_describe_image(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeImages'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_images.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'DescribeImagesResponse' in response.data

    def test_describe_image_by_id(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeImages'
        data['ImageId.1'] = 'a32d70ee-95e4-11e3-b2e4-d19c9d3e5e1d'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_images.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'DescribeImagesResponse' in response.data
        assert 'a32d70ee-95e4-11e3-b2e4-d19c9d3e5e1d' in response.data

    def test_invalid_describe_image_by_id(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeImages'
        data['ImageId.1'] = 'invalid-image-id'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_images.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert 'InvalidAMIID.NotFound' in response.data

    def test_empty_response_describe_images_by_id(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeImages'
        data['ImageId.1'] = 'invalid-images-id'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/empty_describe_images.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert 'InvalidAMIID.NotFound' in response.data

    def test_describe_image_attribute(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeImageAttribute'
        data['ImageId'] = 'a32d70ee-95e4-11e3-b2e4-d19c9d3e5e1d'
        data['Attribute'] = 'description'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_image.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'DescribeImageAttributeResponse' in response.data

    def test_describe_invalid_image_attribute(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeImageAttribute'
        data['ImageId'] = 'a32d70ee-95e4-11e3-b2e4-d19c9d3e5e1d'
        data['Attribute'] = 'invalid_attribute'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_image.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert 'InvalidParameterValue' in response.data
