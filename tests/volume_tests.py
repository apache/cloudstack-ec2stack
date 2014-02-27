#!/usr/bin/env python
# encoding: utf-8

import mock

from ec2stack.helpers import read_file, generate_signature
from . import Ec2StackAppTestCase


class VolumeTestCase(Ec2StackAppTestCase):

    def test_describe_volumes(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeVolumes'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_volumes.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assertOk(response)
        assert 'DescribeVolumesResponse' in response.data
