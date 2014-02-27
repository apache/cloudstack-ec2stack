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

        self.assert_ok(response)
        assert 'DescribeVolumesResponse' in response.data

    @mock.patch('ec2stack.providers.cloudstack.disk_offerings.get_disk_offerings_id_by_name')
    @mock.patch('ec2stack.providers.cloudstack.zones.get_zones_id_by_name')
    def test_create_volume_by_size(self, mock_get_zone, mock_get_disk):
        data = self.get_example_data()
        data['Action'] = 'CreateVolume'
        data['Size'] = 'size'
        data['AvailabilityZone'] = 'zone'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        mock_get_zone.return_value = 'zone'
        mock_get_disk.return_value = 'diskid'

        get_request = mock.Mock()
        get_request.return_value.text = read_file(
            'tests/data/create_volume_response.json'
        )
        get_request.return_value.status_code = 200

        with mock.patch('requests.get', get_request):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'CreateVolumeResponse' in response.data

    @mock.patch('ec2stack.providers.cloudstack.disk_offerings.get_disk_offerings_id_by_name')
    @mock.patch('ec2stack.providers.cloudstack.zones.get_zones_id_by_name')
    def test_create_volume_by_snapshot(self, mock_get_zone, mock_get_disk):
        data = self.get_example_data()
        data['Action'] = 'CreateVolume'
        data['SnapshotId'] = 'snapshotid'
        data['AvailabilityZone'] = 'zone'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        mock_get_zone.return_value = 'zone'
        mock_get_disk.return_value = 'diskid'

        get_request = mock.Mock()
        get_request.return_value.text = read_file(
            'tests/data/create_volume_response.json'
        )
        get_request.return_value.status_code = 200

        with mock.patch('requests.get', get_request):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'CreateVolumeResponse' in response.data

    @mock.patch('ec2stack.providers.cloudstack.disk_offerings.get_disk_offerings_id_by_name')
    def test_create_volume_invalid_zone(self, mock_get_disk):
        data = self.get_example_data()
        data['Action'] = 'CreateVolume'
        data['Size'] = 'size'
        data['AvailabilityZone'] = 'zone'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        mock_get_disk.return_value = 'diskid'

        get_request = mock.Mock()
        get_request.return_value.text = read_file(
            'tests/data/invalid_zone_name.json'
        )
        get_request.return_value.status_code = 200

        with mock.patch('requests.get', get_request):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert 'InvalidZone.NotFound' in response.data

    @mock.patch('ec2stack.providers.cloudstack.disk_offerings.get_disk_offerings_id_by_name')
    @mock.patch('requests.get')
    def test_create_volume_valid_zone(self, get, mock_get_disk):
        data = self.get_example_data()
        data['Action'] = 'CreateVolume'
        data['Size'] = 'size'
        data['AvailabilityZone'] = 'zone'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        mock_get_disk.return_value = 'diskid'

        get.return_value.text = read_file(
            'tests/data/create_volume_response.json'
        )
        get.return_value.status_code = 200

        get_zone = mock.Mock()
        get_zone.return_value.text = read_file(
            'tests/data/list_zone_by_name_response.json'
        )
        get_zone.return_value.status_code = 200

        with mock.patch('ec2stack.providers.cloudstack.zones.get_zones_id_by_name', get_zone):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'CreateVolumeResponse' in response.data

    @mock.patch('ec2stack.providers.cloudstack.disk_offerings.get_disk_offerings_id_by_name')
    @mock.patch('ec2stack.providers.cloudstack.zones.get_zones_id_by_name')
    def test_create_volume_inavild_snapshot(
            self, mock_get_zone, mock_get_disk):
        data = self.get_example_data()
        data['Action'] = 'CreateVolume'
        data['Size'] = 'size'
        data['AvailabilityZone'] = 'zone'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        mock_get_zone.return_value = 'zone'
        mock_get_disk.return_value = 'diskid'

        get_request = mock.Mock()
        get_request.return_value.text = read_file(
            'tests/data/create_volume_invalid_snapshot_response.json'
        )
        get_request.return_value.status_code = 431

        with mock.patch('requests.get', get_request):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert 'InvalidSnapshot.NotFound' in response.data

    def test_delete_volume(self):
        data = self.get_example_data()
        data['Action'] = 'DeleteVolume'
        data['VolumeId'] = 'volumeid'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        get_request = mock.Mock()
        get_request.return_value.text = read_file(
            'tests/data/delete_volume_response.json'
        )
        get_request.return_value.status_code = 200

        with mock.patch('requests.get', get_request):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'DeleteVolumeResponse' in response.data

    def test_delete_volume_invalid_volume_id(self):
        data = self.get_example_data()
        data['Action'] = 'DeleteVolume'
        data['VolumeId'] = 'volumeid'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        get_request = mock.Mock()
        get_request.return_value.text = read_file(
            'tests/data/invalid_volume_id.json'
        )
        get_request.return_value.status_code = 200

        with mock.patch('requests.get', get_request):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert 'InvalidVolume.NotFound' in response.data
