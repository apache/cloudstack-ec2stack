#!/usr/bin/env python
# encoding: utf-8

import mock

from ec2stack.helpers import read_file, generate_signature
from . import Ec2StackAppTestCase


class ZonesTestCase(Ec2StackAppTestCase):

    def test_describe_zone(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeAvailabilityZones'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_key_pairs.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'DescribeAvailabilityZonesResponse' in response.data

    def test_describe_instance_by_name(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeAvailabilityZones'
        data['ZoneName.1'] = 'CH-GV2'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_zone.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'DescribeAvailabilityZonesResponse' in response.data
        assert 'CH-GV2' in response.data

    def test_invalid_describe_instance_by_name(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeAvailabilityZones'
        data['ZoneName.1'] = 'invalid-zone-name'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_zone.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert 'InvalidZone.NotFound' in response.data

    def test_empty_response_describe_zone_by_name(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeAvailabilityZones'
        data['ZoneName.1'] = 'invalid-zone-name'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/empty_describe_zone.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert 'InvalidZone.NotFound' in response.data
