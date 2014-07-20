#!/usr/bin/env python
# encoding: utf-8

import json

import mock

from ec2stack.helpers import read_file, generate_signature
from . import Ec2StackAppTestCase


class SecurityGroupTestCase(Ec2StackAppTestCase):

    def test_authorize_security_group_ingress_by_name(self):
        data = self.get_example_data()
        data['Action'] = 'AuthorizeSecurityGroupIngress'
        data['GroupName'] = 'test'
        data['FromPort'] = '1000'
        data['ToPort'] = '1024'
        data['IpProtocol'] = 'tcp'
        data['CidrIp'] = '0.0.0.0/0'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_authorize_security_group_ingress.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'AuthorizeSecurityGroupIngressResponse' in response.data

    def test_authorize_security_group_ingress_by_id(self):
        data = self.get_example_data()
        data['Action'] = 'AuthorizeSecurityGroupIngress'
        data['GroupId'] = '7ae5b92f-3a0d-4977-bc33-f1aaecee5776'
        data['FromPort'] = '-1'
        data['ToPort'] = '-1'
        data['IpProtocol'] = 'icmp'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_authorize_security_group_ingress.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'AuthorizeSecurityGroupIngressResponse' in response.data

    def test_authorize_security_group_egress_by_name(self):
        data = self.get_example_data()
        data['Action'] = 'AuthorizeSecurityGroupEgress'
        data['GroupName'] = 'test'
        data['FromPort'] = '1000'
        data['ToPort'] = '1024'
        data['IpProtocol'] = 'tcp'
        data['CidrIp'] = '0.0.0.0/0'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_authorize_security_group_egress.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'AuthorizeSecurityGroupEgressResponse' in response.data

    def test_authorize_security_group_egress_by_id(self):
        data = self.get_example_data()
        data['Action'] = 'AuthorizeSecurityGroupEgress'
        data['GroupId'] = '7ae5b92f-3a0d-4977-bc33-f1aaecee5776'
        data['FromPort'] = '-1'
        data['ToPort'] = '-1'
        data['IpProtocol'] = 'icmp'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_authorize_security_group_egress.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'AuthorizeSecurityGroupEgressResponse' in response.data

    def test_duplicate_authorize_security_group(self):
        data = self.get_example_data()
        data['Action'] = 'AuthorizeSecurityGroupEgress'
        data['GroupName'] = 'test'
        data['FromPort'] = '1000'
        data['ToPort'] = '1024'
        data['IpProtocol'] = 'tcp'
        data['CidrIp'] = '0.0.0.0/0'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/invalid_authorize_security_group_egress_duplicate.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert 'InvalidPermission.Duplicate' in response.data

    def test_invalid_rule_authorize_security_group(self):
        data = self.get_example_data()
        data['Action'] = 'AuthorizeSecurityGroupEgress'
        data['GroupName'] = 'test'
        data['FromPort'] = '1000'
        data['ToPort'] = '99999'
        data['IpProtocol'] = 'tcp'
        data['CidrIp'] = '0.0.0.0/24'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/invalid_authorize_security_group_egress.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert 'InvalidRequest' in response.data

    def test_invalid_security_group_authorize_security_group(self):
        data = self.get_example_data()
        data['Action'] = 'AuthorizeSecurityGroupEgress'
        data['GroupName'] = 'invalid-security-group'
        data['FromPort'] = '1000'
        data['ToPort'] = '1024'
        data['IpProtocol'] = 'tcp'
        data['CidrIp'] = '0.0.0.0/24'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/'
            'invalid_security_group_authorize_security_group.json'
        )
        get.return_value.status_code = 431

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert 'InvalidGroup.NotFound' in response.data

    def test_create_security_group(self):
        data = self.get_example_data()
        data['Action'] = 'CreateSecurityGroup'
        data['GroupName'] = 'securitygroupname'
        data['GroupDescription'] = 'security group description'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_create_security_group.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'CreateSecurityGroupResponse' in response.data

    def test_create_duplicate_security_group(self):
        data = self.get_example_data()
        data['Action'] = 'CreateSecurityGroup'
        data['GroupName'] = 'securitygroupname'
        data['GroupDescription'] = 'security group description'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/invalid_create_security_group_duplicate.json'
        )
        get.return_value.status_code = 431

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert 'InvalidGroup.Duplicate' in response.data

    def test_delete_security_group_by_name(self):
        data = self.get_example_data()
        data['Action'] = 'DeleteSecurityGroup'
        data['GroupName'] = 'securitygroupname'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_delete_security_group.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'DeleteSecurityGroupResponse' in response.data

    def test_delete_security_group_by_id(self):
        data = self.get_example_data()
        data['Action'] = 'DeleteSecurityGroup'
        data['GroupId'] = 'securitygroupname'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_delete_security_group.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'DeleteSecurityGroupResponse' in response.data

    def test_invalid_delete_security_group(self):
        data = self.get_example_data()
        data['Action'] = 'DeleteSecurityGroup'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        response = self.post(
            '/',
            data=data
        )

        self.assert_bad_request(response)
        assert 'MissingParameter' in response.data

    def test_describe_security_groups(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeSecurityGroups'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_security_groups.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'DescribeSecurityGroupsResponse' in response.data

    def test_describe_security_group_by_id(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeSecurityGroups'
        data['GroupId'] = '3b637c2e-b0a8-40ae-a7a3-2bef2871d36d'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_security_groups.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'DescribeSecurityGroupsResponse' in response.data
        assert '3b637c2e-b0a8-40ae-a7a3-2bef2871d36d' in response.data

    def test_invalid_describe_security_group_by_id(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeSecurityGroups'
        data['GroupId'] = 'invalid-security-group-id'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_security_groups.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert 'InvalidGroup.NotFound' in response.data

    def test_empty_response_describe_security_group_by_id(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeSecurityGroups'
        data['GroupId'] = 'invalid-security-group-id'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/empty_describe_security_groups.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert 'InvalidGroup.NotFound' in response.data

    def test_describe_security_group_by_name(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeSecurityGroups'
        data['GroupName'] = 'test'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_security_groups.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'DescribeSecurityGroupsResponse' in response.data
        assert 'test' in response.data

    def test_invalid_describe_security_group_by_name(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeSecurityGroups'
        data['GroupName'] = 'invalid-name'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_security_groups.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert 'InvalidGroup.NotFound' in response.data

    def test_empty_response_describe_security_group_by_name(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeSecurityGroups'
        data['GroupName'] = 'invalid-name'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/empty_describe_security_groups.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert 'InvalidGroup.NotFound' in response.data

    def test_revoke_security_group_ingress(self):
        data = self.get_example_data()
        data['Action'] = 'RevokeSecurityGroupIngress'
        data['GroupId'] = '7ae5b92f-3a0d-4977-bc33-f1aaecee5776'
        data['FromPort'] = '1000'
        data['ToPort'] = '1024'
        data['IpProtocol'] = 'tcp'
        data['CidrIp'] = '192.168.0.0/24'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/revoke_security_group_ingress.json'
        )
        get.return_value.status_code = 200

        describe_item_request = mock.Mock()
        describe_item_request.return_value = json.loads(read_file(
            'tests/data/revoke_security_group_search.json'
        ))

        with mock.patch('requests.get', get):
            with mock.patch(
                    'ec2stack.providers.cloudstack.describe_item_request',
                    describe_item_request
            ):
                response = self.post(
                    '/',
                    data=data
                )

        self.assert_ok(response)
        assert 'RevokeSecurityGroupIngressResponse' in response.data

    def test_revoke_security_group_egress(self):
        data = self.get_example_data()
        data['Action'] = 'RevokeSecurityGroupEgress'
        data['GroupId'] = '7ae5b92f-3a0d-4977-bc33-f1aaecee5776'
        data['FromPort'] = '-1'
        data['ToPort'] = '-1'
        data['IpProtocol'] = 'icmp'
        data['CidrIp'] = '192.168.0.0/24'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/revoke_security_group_egress.json'
        )
        get.return_value.status_code = 200

        describe_item_request = mock.Mock()
        describe_item_request.return_value = json.loads(read_file(
            'tests/data/revoke_security_group_search.json'
        ))

        with mock.patch('requests.get', get):
            with mock.patch(
                    'ec2stack.providers.cloudstack.describe_item_request',
                    describe_item_request
            ):
                response = self.post(
                    '/',
                    data=data
                )

        self.assert_ok(response)
        assert 'RevokeSecurityGroupEgressResponse' in response.data

    def test_invalid_revoke_security_group(self):
        data = self.get_example_data()
        data['Action'] = 'RevokeSecurityGroupEgress'
        data['GroupId'] = '7ae5b92f-3a0d-4977-bc33-f1aaecee5776'
        data['FromPort'] = '0'
        data['ToPort'] = '0'
        data['IpProtocol'] = 'invalid'
        data['CidrIp'] = '192.168.0.0/24'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/revoke_security_group_egress.json'
        )
        get.return_value.status_code = 200

        describe_item_request = mock.Mock()
        describe_item_request.return_value = json.loads(read_file(
            'tests/data/revoke_security_group_search.json'
        ))

        with mock.patch('requests.get', get):
            with mock.patch(
                    'ec2stack.providers.cloudstack.describe_item_request',
                    describe_item_request
            ):
                response = self.post(
                    '/',
                    data=data
                )

        self.assert_bad_request(response)
        assert 'InvalidPermission.NotFound' in response.data
