#!/usr/bin/env python
# encoding: utf-8

import mock

from ec2stack.helpers import read_file, generate_signature
from . import Ec2StackAppTestCase


class SecurityGroupTestCase(Ec2StackAppTestCase):
    def test_create_security_group(self):
        data = self.get_example_data()
        data['Action'] = 'CreateSecurityGroup'
        data['GroupName'] = 'securitygroupname'
        data['GroupDescription'] = 'security group description'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        get = mock.Mock()
        text = get.return_value.text = read_file(
            'tests/data/valid_create_security_group.json'
        )
        status_code = get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assertOk(response)
        assert 'CreateSecurityGroupResponse' in response.data

    def test_duplicate_security_group(self):
        data = self.get_example_data()
        data['Action'] = 'CreateSecurityGroup'
        data['GroupName'] = 'securitygroupname'
        data['GroupDescription'] = 'security group description'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        get = mock.Mock()
        text = get.return_value.text = read_file(
            'tests/data/duplicate_create_security_group.json'
        )
        status_code = get.return_value.status_code = 431

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assertBadRequest(response)
        assert 'InvalidGroup.Duplicate' in response.data

    def test_name_delete_security_group(self):
        data = self.get_example_data()
        data['Action'] = 'DeleteSecurityGroup'
        data['GroupName'] = 'securitygroupname'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        get = mock.Mock()
        text = get.return_value.text = read_file(
            'tests/data/valid_delete_security_group.json'
        )
        status_code = get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assertOk(response)
        assert 'DeleteSecurityGroupResponse' in response.data

    def test_groupid_delete_security_group(self):
        data = self.get_example_data()
        data['Action'] = 'DeleteSecurityGroup'
        data['GroupId'] = 'securitygroupname'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        get = mock.Mock()
        text = get.return_value.text = read_file(
            'tests/data/valid_delete_security_group.json'
        )
        status_code = get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assertOk(response)
        assert 'DeleteSecurityGroupResponse' in response.data

    def test_invalid_delete_security_group(self):
        data = self.get_example_data()
        data['Action'] = 'DeleteSecurityGroup'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        response = self.post(
            '/',
            data=data
        )

        self.assertBadRequest(response)
        assert 'MissingParameter' in response.data
