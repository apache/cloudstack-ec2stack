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

from ec2stack.helpers import read_file, generate_signature
from . import Ec2StackAppTestCase


class TagsTestCase(Ec2StackAppTestCase):

    def test_create_tag(self):
        data = self.get_example_data()
        data['Action'] = 'CreateTags'
        data['Tag.1.Key'] = 'examplekey'
        data['Tag.1.value'] = 'examplevalue'
        data['ResourceId.1'] = 'exampleresourceid'

        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_create_tag.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'CreateTagsResponse' in response.data

    def test_create_tag_resource_id_not_in_config(self):
        data = self.get_example_data()
        data['Action'] = 'CreateTags'
        data['Tag.1.Key'] = 'examplekey'
        data['Tag.1.value'] = 'examplevalue'
        data['ResourceId.1'] = 'exampleunconfigredresourceid'

        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_create_tag.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert ' not found in configuration' in response.data

    def test_create_tag_resource_id_not_found(self):
        data = self.get_example_data()
        data['Action'] = 'CreateTags'
        data['Tag.1.Key'] = 'examplekey'
        data['Tag.1.value'] = 'examplevalue'
        data['ResourceId.1'] = 'exampleresourceid'

        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/invalid_create_tag_not_found.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert 'The specified ID for the resource you are trying to tag is not valid.' in response.data

    def test_delete_tag(self):
        data = self.get_example_data()
        data['Action'] = 'DeleteTags'
        data['Tag.1.Key'] = 'examplekey'
        data['ResourceId.1'] = 'exampleresourceid'

        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_delete_tag.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'DeleteTagsResponse' in response.data

    def test_delete_tag_resource_id_not_in_config(self):
        data = self.get_example_data()
        data['Action'] = 'DeleteTags'
        data['Tag.1.Key'] = 'examplekey'
        data['ResourceId.1'] = 'exampleunconfigredresourceid'

        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_delete_tag.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert ' not found in configuration' in response.data

    def test_delete_tag_resource_id_not_found(self):
        data = self.get_example_data()
        data['Action'] = 'DeleteTags'
        data['Tag.1.Key'] = 'examplekey'
        data['ResourceId.1'] = 'exampleresourceid'

        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/invalid_delete_tag_tag_not_found.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert 'The specified ID for the resource you are trying to tag is not valid.' in response.data

    def test_delete_keypair(self):
        data = self.get_example_data()
        data['Action'] = 'DeleteKeyPair'
        data['KeyName'] = 'Test'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_delete_keypair.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'DeleteKeyPairResponse' in response.data

    def test_describe_tags(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeTags'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_tags.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'DescribeTagsResponse' in response.data
