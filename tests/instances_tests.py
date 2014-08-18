#!/usr/bin/env python
# encoding: utf-8

import json

import mock

from ec2stack.helpers import read_file, generate_signature
from . import Ec2StackAppTestCase


class InstancesTestCase(Ec2StackAppTestCase):

    def test_describe_instance_attribute(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeInstanceAttribute'
        data['InstanceId'] = '43791f77-26f8-48ca-b557-3a9392f735ae'
        data['Attribute'] = 'instanceType'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_instance.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'DescribeInstanceAttributeResponse' in response.data

    def test_describe_invalid_instance_attribute(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeInstanceAttribute'
        data['InstanceId'] = '43791f77-26f8-48ca-b557-3a9392f735ae'
        data['Attribute'] = 'invalid_attribute'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_instance.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert 'InvalidParameterValue' in response.data

    def test_describe_instances(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeInstances'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_instances.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'DescribeInstancesResponse' in response.data

    def test_empty_response_describe_instances(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeInstances'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/empty_describe_instances.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'DescribeInstancesResponse' in response.data

    def test_describe_instance_by_id(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeInstances'
        data['InstanceId.1'] = 'aa10a43e-56db-4a34-88bd-1c2a51c0bc04'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_instances.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'DescribeInstancesResponse' in response.data
        assert 'aa10a43e-56db-4a34-88bd-1c2a51c0bc04' in response.data

    def test_invalid_describe_instance_by_id(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeInstances'
        data['InstanceId.1'] = 'invalid-instance-id'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_describe_instances.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert 'InvalidInstanceId.NotFound' in response.data

    def test_empty_response_describe_instance_by_id(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeInstances'
        data['InstanceId.1'] = 'invalid-instance-id'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/empty_describe_instances.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_bad_request(response)
        assert 'InvalidInstanceId.NotFound' in response.data

    def test_reboot_instance(self):
        data = self.get_example_data()
        data['Action'] = 'RebootInstances'
        data['InstanceId.1'] = '076166a1-9f6e-11e3-b8df-3c075456b21a'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_reboot_instance.json'
        )
        get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assert_ok(response)
        assert 'RebootInstancesResponse' in response.data

    def test_start_instance(self):
        data = self.get_example_data()
        data['Action'] = 'StartInstances'
        data['InstanceId.1'] = '076166a1-9f6e-11e3-b8df-3c075456b21a'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_start_instance.json'
        )
        get.return_value.status_code = 200

        get_instance = mock.Mock()
        get_instance.return_value = json.loads(read_file(
            'tests/data/valid_get_instance_by_id.json'
        ))

        with mock.patch('requests.get', get):
            with mock.patch(
                    'ec2stack.providers.cloudstack.instances.describe_instance_by_id',
                    get_instance
            ):
                response = self.post(
                    '/',
                    data=data
                )

        self.assert_ok(response)
        assert 'StartInstancesResponse' in response.data

    def test_stop_instance(self):
        data = self.get_example_data()
        data['Action'] = 'StopInstances'
        data['InstanceId.1'] = '076166a1-9f6e-11e3-b8df-3c075456b21a'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_stop_instance.json'
        )
        get.return_value.status_code = 200

        get_instance = mock.Mock()
        get_instance.return_value = json.loads(read_file(
            'tests/data/valid_get_instance_by_id.json'
        ))

        with mock.patch('requests.get', get):
            with mock.patch(
                    'ec2stack.providers.cloudstack.instances.describe_instance_by_id',
                    get_instance
            ):
                response = self.post(
                    '/',
                    data=data
                )

        self.assert_ok(response)
        assert 'StopInstancesResponse' in response.data

    def test_terminate_instance(self):
        data = self.get_example_data()
        data['Action'] = 'TerminateInstances'
        data['InstanceId.1'] = '076166a1-9f6e-11e3-b8df-3c075456b21a'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_terminate_instance.json'
        )
        get.return_value.status_code = 200

        get_instance = mock.Mock()
        get_instance.return_value = json.loads(read_file(
            'tests/data/valid_get_instance_by_id.json'
        ))

        with mock.patch('requests.get', get):
            with mock.patch(
                    'ec2stack.providers.cloudstack.instances.describe_instance_by_id',
                    get_instance
            ):
                response = self.post(
                    '/',
                    data=data
                )

        self.assert_ok(response)
        assert 'TerminateInstancesResponse' in response.data

    def test_run_instance(self):
        data = self.get_example_data()
        data['Action'] = 'RunInstances'
        data['ImageId'] = 'a32d70ee-95e4-11e3-b2e4-d19c9d3e5e1d'
        data['MinCount'] = '0'
        data['MaxCount'] = '0'
        data['SecurityGroupId.1'] = 'example-security-group-id'
        data['SecurityGroup.1'] = 'example-security-group-name'
        data['KeyName'] = 'example-ssh-key-name'
        data['UserData'] = 'example-user-data'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_run_instance.json'
        )
        get.return_value.status_code = 200

        get_service_offering = mock.Mock()
        get_service_offering.return_value = json.loads(read_file(
            'tests/data/service_offering_search.json'
        ))

        get_zone = mock.Mock()
        get_zone.return_value = json.loads(read_file(
            'tests/data/zones_search.json'
        ))

        with mock.patch('requests.get', get):
            with mock.patch(
                    'ec2stack.providers.cloudstack.service_offerings.get_service_offering',
                    get_service_offering
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
        assert 'RunInstancesResponse' in response.data

    def test_run_instance_gp2(self):
        data = self.get_example_data()
        data['Action'] = 'RunInstances'
        data['ImageId'] = 'a32d70ee-95e4-11e3-b2e4-d19c9d3e5e1d'
        data['MinCount'] = '0'
        data['MaxCount'] = '0'
        data['SecurityGroupId.1'] = 'example-security-group-id'
        data['SecurityGroup.1'] = 'example-security-group-name'
        data['KeyName'] = 'example-ssh-key-name'
        data['UserData'] = 'example-user-data'
        data['BlockDeviceMapping.1.Ebs.VolumeType'] = 'gp2'
        data['BlockDeviceMapping.1.Ebs.VolumeSize'] = '20'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_run_instance.json'
        )
        get.return_value.status_code = 200

        get_disk_offering = mock.Mock()
        get_disk_offering.return_value = json.loads(read_file(
            'tests/data/disk_offering_search.json'
        ))

        get_service_offering = mock.Mock()
        get_service_offering.return_value = json.loads(read_file(
            'tests/data/service_offering_search.json'
        ))

        get_zone = mock.Mock()
        get_zone.return_value = json.loads(read_file(
            'tests/data/zones_search.json'
        ))

        with mock.patch('requests.get', get):
            with mock.patch(
                    'ec2stack.providers.cloudstack.disk_offerings.get_disk_offering',
                    get_disk_offering
            ):
                with mock.patch(
                        'ec2stack.providers.cloudstack.service_offerings.get_service_offering',
                        get_service_offering
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
        assert 'RunInstancesResponse' in response.data

    def test_run_instance_gp2_no_volume_size(self):
        data = self.get_example_data()
        data['Action'] = 'RunInstances'
        data['ImageId'] = 'a32d70ee-95e4-11e3-b2e4-d19c9d3e5e1d'
        data['MinCount'] = '0'
        data['MaxCount'] = '0'
        data['SecurityGroupId.1'] = 'example-security-group-id'
        data['SecurityGroup.1'] = 'example-security-group-name'
        data['KeyName'] = 'example-ssh-key-name'
        data['UserData'] = 'example-user-data'
        data['BlockDeviceMapping.1.Ebs.VolumeType'] = 'gp2'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_run_instance.json'
        )
        get.return_value.status_code = 200

        get_disk_offering = mock.Mock()
        get_disk_offering.return_value = json.loads(read_file(
            'tests/data/disk_offering_search.json'
        ))

        get_service_offering = mock.Mock()
        get_service_offering.return_value = json.loads(read_file(
            'tests/data/service_offering_search.json'
        ))

        get_zone = mock.Mock()
        get_zone.return_value = json.loads(read_file(
            'tests/data/zones_search.json'
        ))

        with mock.patch('requests.get', get):
            with mock.patch(
                    'ec2stack.providers.cloudstack.disk_offerings.get_disk_offering',
                    get_disk_offering
            ):
                with mock.patch(
                        'ec2stack.providers.cloudstack.service_offerings.get_service_offering',
                        get_service_offering
                ):
                    with mock.patch(
                            'ec2stack.providers.cloudstack.zones.get_zone',
                            get_zone
                    ):
                        response = self.post(
                            '/',
                            data=data
                        )

        self.assert_bad_request(response)
        assert 'VolumeSize not found in BlockDeviceMapping' in response.data


    def test_run_instance_with_zone_and_type_(self):
        data = self.get_example_data()
        data['Action'] = 'RunInstances'
        data['InstanceType'] = 'micro'
        data['Placement.AvailabilityZone'] = 'example-zone'
        data['ImageId'] = 'a32d70ee-95e4-11e3-b2e4-d19c9d3e5e1d'
        data['MinCount'] = '0'
        data['MaxCount'] = '0'
        data['SecurityGroupId.1'] = 'example-security-group-id'
        data['SecurityGroup.1'] = 'example-security-group-name'
        data['KeyName'] = 'example-ssh-key-name'
        data['UserData'] = 'example-user-data'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/valid_run_instance.json'
        )
        get.return_value.status_code = 200

        get_service_offering = mock.Mock()
        get_service_offering.return_value = json.loads(read_file(
            'tests/data/service_offering_search.json'
        ))

        get_zone = mock.Mock()
        get_zone.return_value = json.loads(read_file(
            'tests/data/zones_search.json'
        ))

        with mock.patch('requests.get', get):
            with mock.patch(
                    'ec2stack.providers.cloudstack.service_offerings.get_service_offering',
                    get_service_offering
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
        assert 'RunInstancesResponse' in response.data

    def test_run_instance_invalid_image_id(self):
        data = self.get_example_data()
        data['Action'] = 'RunInstances'
        data['ImageId'] = 'invalid-id'
        data['MinCount'] = '0'
        data['MaxCount'] = '0'
        data['SecurityGroupId.1'] = 'example-security-group-id'
        data['SecurityGroup.1'] = 'example-security-group-name'
        data['KeyName'] = 'example-ssh-key-name'
        data['UserData'] = 'example-user-data'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/invalid_run_instance_image_not_found.json'
        )
        get.return_value.status_code = 431

        get_service_offering = mock.Mock()
        get_service_offering.return_value = json.loads(read_file(
            'tests/data/service_offering_search.json'
        ))

        get_zone = mock.Mock()
        get_zone.return_value = json.loads(read_file(
            'tests/data/zones_search.json'
        ))

        with mock.patch('requests.get', get):
            with mock.patch(
                    'ec2stack.providers.cloudstack.service_offerings.get_service_offering',
                    get_service_offering
            ):
                with mock.patch(
                        'ec2stack.providers.cloudstack.zones.get_zone',
                        get_zone
                ):
                    response = self.post(
                        '/',
                        data=data
                    )

        self.assert_bad_request(response)
        assert 'InvalidAMIID.NotFound' in response.data

    def test_run_instance_invalid_security_group(self):
        data = self.get_example_data()
        data['Action'] = 'RunInstances'
        data['ImageId'] = 'a32d70ee-95e4-11e3-b2e4-d19c9d3e5e1d'
        data['MinCount'] = '0'
        data['MaxCount'] = '0'
        data['SecurityGroupId.1'] = 'invalid-security-group-id'
        data['SecurityGroup.1'] = 'invalid-security-group-name'
        data['KeyName'] = 'example-ssh-key-name'
        data['UserData'] = 'example-user-data'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/invalid_run_instance_security_group_not_found.json'
        )
        get.return_value.status_code = 431

        get_service_offering = mock.Mock()
        get_service_offering.return_value = json.loads(read_file(
            'tests/data/service_offering_search.json'
        ))

        get_zone = mock.Mock()
        get_zone.return_value = json.loads(read_file(
            'tests/data/zones_search.json'
        ))

        with mock.patch('requests.get', get):
            with mock.patch(
                    'ec2stack.providers.cloudstack.service_offerings.get_service_offering',
                    get_service_offering
            ):
                with mock.patch(
                        'ec2stack.providers.cloudstack.zones.get_zone',
                        get_zone
                ):
                    response = self.post(
                        '/',
                        data=data
                    )

        self.assert_bad_request(response)
        assert 'InvalidGroup.NotFound' in response.data

    def test_run_instance_invalid_keyname(self):
        data = self.get_example_data()
        data['Action'] = 'RunInstances'
        data['ImageId'] = 'a32d70ee-95e4-11e3-b2e4-d19c9d3e5e1d'
        data['MinCount'] = '0'
        data['MaxCount'] = '0'
        data['SecurityGroupId.1'] = 'example-security-group-id'
        data['SecurityGroup.1'] = 'example-security-group-name'
        data['KeyName'] = 'invalid-ssh-key-name'
        data['UserData'] = 'example-user-data'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/invalid_run_instance_keypair_not_found.json'
        )
        get.return_value.status_code = 431

        get_service_offering = mock.Mock()
        get_service_offering.return_value = json.loads(read_file(
            'tests/data/service_offering_search.json'
        ))

        get_zone = mock.Mock()
        get_zone.return_value = json.loads(read_file(
            'tests/data/zones_search.json'
        ))

        with mock.patch('requests.get', get):
            with mock.patch(
                    'ec2stack.providers.cloudstack.service_offerings.get_service_offering',
                    get_service_offering
            ):
                with mock.patch(
                        'ec2stack.providers.cloudstack.zones.get_zone',
                        get_zone
                ):
                    response = self.post(
                        '/',
                        data=data
                    )

        self.assert_bad_request(response)
        assert 'InvalidKeyPair.NotFound' in response.data

    def test_run_instance_unknown_issue(self):
        data = self.get_example_data()
        data['Action'] = 'RunInstances'
        data['ImageId'] = 'a32d70ee-95e4-11e3-b2e4-d19c9d3e5e1d'
        data['MinCount'] = '0'
        data['MaxCount'] = '0'
        data['SecurityGroupId.1'] = 'example-security-group-id'
        data['SecurityGroup.1'] = 'example-security-group-name'
        data['KeyName'] = 'example-ssh-key-name'
        data['UserData'] = 'example-user-data'
        data['Signature'] = generate_signature(data, 'POST', 'localhost', '/')

        get = mock.Mock()
        get.return_value.text = read_file(
            'tests/data/invalid_run_instance_unknown_issue.json'
        )
        get.return_value.status_code = 431

        get_service_offering = mock.Mock()
        get_service_offering.return_value = json.loads(read_file(
            'tests/data/service_offering_search.json'
        ))

        get_zone = mock.Mock()
        get_zone.return_value = json.loads(read_file(
            'tests/data/zones_search.json'
        ))

        with mock.patch('requests.get', get):
            with mock.patch(
                    'ec2stack.providers.cloudstack.service_offerings.get_service_offering',
                    get_service_offering
            ):
                with mock.patch(
                        'ec2stack.providers.cloudstack.zones.get_zone',
                        get_zone
                ):
                    response = self.post(
                        '/',
                        data=data
                    )

        self.assert_bad_request(response)
        assert 'InvalidRequest' in response.data
