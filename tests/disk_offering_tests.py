#!/usr/bin/env python
# encoding: utf-8

import json

import mock

from ec2stack.helpers import read_file, generate_signature
from . import Ec2StackAppTestCase


class DiskOfferingsTestCase(Ec2StackAppTestCase):

    def test_get_disk_offering(self):
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

        describe_disk_offering = mock.Mock()
        describe_disk_offering.return_value = json.loads(read_file(
            'tests/data/disk_offering_search.json'
        ))

        get_zone = mock.Mock()
        get_zone.return_value = json.loads(read_file(
            'tests/data/zones_search.json'
        ))

        with mock.patch('requests.get', get):
            with mock.patch(
                    'ec2stack.providers.cloudstack.describe_item_request',
                    describe_disk_offering
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
        assert 'CreateVolumeResponse' in response.data
