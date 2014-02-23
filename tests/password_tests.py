#!/usr/bin/env python
# encoding: utf-8

import mock

from ec2stack.helpers import read_file, generate_signature
from . import Ec2StackAppTestCase


class PasswordTestCase(Ec2StackAppTestCase):

    def test_get_password_data(self):
        data = self.get_example_data()
        data['Action'] = 'GetPasswordData'
        data['InstanceId'] = 'Test'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        get = mock.Mock()
        text = get.return_value.text = read_file(
            'tests/data/valid_instance_get_password.json'
        )
        status_code = get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assertOk(response)
        assert 'GetPasswordDataResponse' in response.data

    def test_invalid_get_password(self):
        data = self.get_example_data()
        data['Action'] = 'GetPasswordData'
        data['InstanceId'] = 'Test'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        get = mock.Mock()
        text = get.return_value.text = read_file(
            'tests/data/invalid_instance_get_password.json'
        )
        status_code = get.return_value.status_code = 431

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assertBadRequest(response)
        assert 'InvalidInstanceID.NotFound' in response.data
