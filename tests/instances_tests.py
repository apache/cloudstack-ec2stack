#!/usr/bin/env python
# encoding: utf-8

import mock

from ec2stack.helpers import read_file, generate_signature
from . import Ec2StackAppTestCase


class InstancesTestCase(Ec2StackAppTestCase):

    def test_describe_instances(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeInstances'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        get = mock.Mock()
        text = get.return_value.text = read_file(
            'tests/data/valid_describe_instances.json'
        )
        status_code = get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assertOk(response)
        assert 'DescribeInstancesResponse' in response.data

    def test_describe_specific_instances(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeInstances'
        data['InstanceId.1'] = 'a32d70ee-95e4-11e3-b2e4-d19c9d3e5e1d'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        get = mock.Mock()
        text = get.return_value.text = read_file(
            'tests/data/valid_describe_instances.json'
        )
        status_code = get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assertOk(response)
        assert 'DescribeInstancesResponse' in response.data

    def test_describe_image_attribute(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeInstanceAttribute'
        data['ImageId.1'] = 'a32d70ee-95e4-11e3-b2e4-d19c9d3e5e1d'
        data['Attribute'] = 'name'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        get = mock.Mock()
        text = get.return_value.text = read_file(
            'tests/data/valid_describe_instance_attribute.json'
        )
        status_code = get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assertOk(response)
        assert 'DescribeInstanceAttributeResponse' in response.data
