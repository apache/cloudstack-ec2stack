#!/usr/bin/env python
# encoding: utf-8

from base64 import b64encode

import mock
import json

from ec2stack.helpers import read_file, generate_signature
from . import Ec2StackAppTestCase


class SnapshotTestCase(Ec2StackAppTestCase):

    def test_create_snapshot(self):
        data = self.get_example_data()
        data['Action'] = 'CreateSnapshot'
        data['VolumeId'] = 'daa492b4-bd09-46b0-a4ad-142e187ecdbe'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_create_snapshot.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'CreateSnapshotResponse' in response.data

    def test_describe_snapshots(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeSnapshots'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_snapshots.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'DescribeSnapshotsResponse' in response.data

    def test_describe_snapshot_by_name(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeSnapshots'
        data['SnapshotId'] = 'examplesnapshot'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_snapshot.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        print response.data
        self.assert_ok(response)
        assert 'DescribeSnapshotsResponse' in response.data
        assert 'examplesnapshot' in response.data

    def test_describe_snapshot_by_name_invalid_name(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeSnapshots'
        data['SnapshotId'] = 'invalidsnapshot'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_snapshot.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert 'InvalidSnapshot.NotFound' in response.data

    def test_delete_snapshot(self):
        data = self.get_example_data()
        data['Action'] = 'DeleteSnapshot'
        data['SnapshotId'] = 'Test'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_delete_snapshot.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'DeleteSnapshotResponse' in response.data