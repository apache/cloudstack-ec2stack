#!/usr/bin/env python
# encoding: utf-8

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
            'tests/data/create_tag.json'
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
            'tests/data/create_tag.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert ' not found in configuration' in response.data

    def test_delete_tag(self):
        data = self.get_example_data()
        data['Action'] = 'DeleteTags'
        data['Tag.1.Key'] = 'examplekey'
        data['ResourceId.1'] = 'exampleresourceid'


        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/delete_tag.json'
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
            'tests/data/delete_tag.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert ' not found in configuration' in response.data

    def test_delete_keypair(self):
        data = self.get_example_data()
        data['Action'] = 'DeleteKeyPair'
        data['KeyName'] = 'Test'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/delete_keypair.json'
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
            'tests/data/list_tags.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'DescribeTagsResponse' in response.data


