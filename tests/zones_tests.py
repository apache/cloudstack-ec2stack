#!/usr/bin/env python
# encoding: utf-8

import json

import mock

from ec2stack.helpers import read_file, generate_signature
from . import Ec2StackAppTestCase


class ZonesTestCase(Ec2StackAppTestCase):

    def test_describe_zone(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeAvailabilityZones'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

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

    def test_describe_zone_by_name(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeAvailabilityZones'
        data['ZoneName.1'] = 'CH-GV2'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

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

    def test_invalid_describe_zone_by_name(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeAvailabilityZones'
        data['ZoneName.1'] = 'invalid-zone-name'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

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
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

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

    def test_get_zone(self):
        data = self.get_example_data()
        data['Action'] = 'CreateVolume'
        data['Size'] = '80'
        data['AvailabilityZone'] = 'Sandbox-simulator'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_create_volume.json'
        )
        get.return_value.status_code = 200

        get_disk_offering = mock.Mock()
        get_disk_offering.return_value = json.loads(read_file(
            'tests/data/disk_offering_search.json'
        ))

        describe_zone = mock.Mock()
        describe_zone.return_value = json.loads(read_file(
            'tests/data/zones_search.json'
        ))

        with mock.patch('requests.get', get):
            with mock.patch(
                    'ec2stack.providers.cloudstack.describe_item_request',
                    get_disk_offering
            ):
                with mock.patch(
                        'ec2stack.providers.cloudstack.describe_item',
                        describe_zone
                ):
                    response = self.post(
                        '/',
                        data=data
                    )

        self.assert_ok(response)
        assert 'CreateVolumeResponse' in response.data
