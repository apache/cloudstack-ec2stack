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
        data['InstanceId.1'] = 'aa10a43e-56db-4a34-88bd-1c2a51c0bc04'
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

    def test_describe_instance_attribute(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeInstanceAttribute'
        data['InstanceId'] = '43791f77-26f8-48ca-b557-3a9392f735ae'
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
