#!/usr/bin/env python
# encoding: utf-8

"""This module contains functions for handling requests in relation to
instances.
"""

from flask import current_app

from ec2stack.providers import cloudstack
from ec2stack.providers.cloudstack import requester, service_offerings, zones, \
    disk_offerings
from ec2stack import helpers, errors


@helpers.authentication_required
def describe_instance_attribute():
    """
    Describes an instance attribute.

    @return: Response.
    """
    instance_id = helpers.get('InstanceId')
    attribute = helpers.get('Attribute')

    supported_attribute_map = {
        'instanceType': 'serviceofferingname',
        'groupSet': 'securitygroup'
    }

    if attribute not in supported_attribute_map.iterkeys():
        errors.invalid_parameter_value(
            'The specified attribute is not valid, please specify a valid ' +
            'instance attribute.'
        )

    response = describe_instance_by_id(instance_id)
    return _describe_instance_attribute_response(
        response, attribute, supported_attribute_map)


def _describe_instance_attribute_response(response, attribute, attr_map):
    """
    Generates a response for a describe instance attribute request.

    @param response: Response from Cloudstack.
    @param attribute: Attribute to Describe.
    @param attr_map: Map of attributes from EC2 to Cloudstack.
    @return: Response.
    """
    response = {
        'template_name_or_list': 'instance_attribute.xml',
        'response_type': 'DescribeInstanceAttributeResponse',
        'attribute': attribute,
        'response': response[attr_map[attribute]],
        'id': response['id']
    }

    return response


@helpers.authentication_required
def describe_instances():
    """
    Describe a specific instance or all instances.

    @return: Response.
    """
    args = {'command': 'listVirtualMachines'}
    response = cloudstack.describe_item(
        args, 'virtualmachine', errors.invalid_instance_id, 'InstanceId'
    )

    return _describe_instances_response(
        response
    )


def describe_instance_by_id(instance_id):
    """
    Describe an instance by Id.

    @param instance_id: Id of the instance.
    @return: Response.
    """
    args = {'id': instance_id, 'command': 'listVirtualMachines'}
    response = cloudstack.describe_item_request(
        args, 'virtualmachine', errors.invalid_instance_id
    )
    return response


def _describe_instances_response(response):
    """
    Generates a response for a describe instance request.

    @param response: Response from Cloudstack.
    @return: Response.
    """
    return {
        'template_name_or_list': 'instances.xml',
        'response_type': 'DescribeInstancesResponse',
        'response': response
    }


@helpers.authentication_required
def reboot_instance():
    """
    Reboot an instance.

    @return: Response.
    """
    helpers.require_parameters(['InstanceId.1'])
    instance_id = helpers.get('InstanceId.1')
    _reboot_instance_request(instance_id)
    return _reboot_instance_response()


def _reboot_instance_request(instance_id):
    """
    Request to reboot an instance.

    @param instance_id: Id of instance to be rebooted.
    @return: Response.
    """
    args = {'command': 'rebootVirtualMachine',
            'id': instance_id}
    response = requester.make_request_async(args)
    response = response['virtualmachine']
    return response


def _reboot_instance_response():
    """
    Generates a response for a reboot instance request.

    @return: Response.
    """
    response = {
        'template_name_or_list': 'status.xml',
        'response_type': 'RebootInstancesResponse',
        'return': 'true'
    }

    return response


@helpers.authentication_required
def run_instance():
    """
    Run a instance.

    @return: Response.
    """
    helpers.require_parameters(
        ['ImageId', 'MinCount', 'MaxCount'])
    response = _run_instance_request()
    return _run_instance_response(response)


def _run_instance_request():
    """
    Request to bring up an instance.

    @return: Response.
    """
    args = {}
    if helpers.contains_parameter('Placement.AvailabilityZone'):
        args['zoneid'] = zones.get_zone(
            helpers.get('Placement.AvailabilityZone')
        )
    else:
        args['zoneid'] = zones.get_zone(
            current_app.config['CLOUDSTACK_DEFAULT_ZONE']
        )['id']

    if helpers.get('BlockDeviceMapping.1.Ebs.VolumeType') is not None:
        disk_type = helpers.get('BlockDeviceMapping.1.Ebs.VolumeType')
        if disk_type == 'gp2':
            args['diskofferingid'] = disk_offerings.get_disk_offering(
                current_app.config['CLOUDSTACK_CUSTOM_DISK_OFFERING']
            )['id']

        if helpers.get('BlockDeviceMapping.1.Ebs.VolumeSize') is None:
            errors.invalid_request("VolumeSize not found in BlockDeviceMapping")
        else:
            args['size'] = helpers.get('BlockDeviceMapping.1.Ebs.VolumeSize')

    if helpers.get('InstanceType') is None:
        instance_type = 'm1.small'
    else:
        instance_type = helpers.get('InstanceType')

    if instance_type in current_app.config['INSTANCE_TYPE_MAP']:
        instance_type = current_app.config[
            'INSTANCE_TYPE_MAP'][instance_type]
    else:
        instance_type = instance_type

    args['serviceofferingid'] = \
        service_offerings.get_service_offering(instance_type)['id']
    args['templateid'] = helpers.get('ImageId')

    if helpers.contains_parameter('KeyName'):
        args['keypair'] = helpers.get('KeyName')

    if helpers.contains_parameter('UserData'):
        args['userdata'] = helpers.get('UserData')

    if helpers.contains_parameter_with_keyword('SecurityGroupId.'):
        keys = helpers.get_request_parameter_keys('SecurityGroupId.')
        securitygroupids = []

        for key in keys:
            securitygroupids.append(helpers.get(key))

        args['securitygroupids'] = ",".join(securitygroupids)

    if helpers.contains_parameter_with_keyword('SecurityGroup.'):
        keys = helpers.get_request_parameter_keys('SecurityGroup.')
        securitygroupnames = []

        for key in keys:
            securitygroupnames.append(helpers.get(key))

        args['securitygroupnames'] = ",".join(securitygroupnames)

    args['command'] = 'deployVirtualMachine'

    response = requester.make_request_async(args)

    return response


def _run_instance_response(response):
    """
    Generates a response for a run instance request.

    @param response: Response from Cloudstack.
    @return: Response.
    """
    if 'errortext' in response:
        if 'Object vm_template' in response['errortext']:
            errors.invalid_image_id()
        elif 'Object security_group' in response['errortext']:
            errors.invalid_security_group()
        elif 'A key pair with name' in response['errortext']:
            errors.invalid_keypair_name()
        else:
            errors.invalid_request(response['errortext'])
    else:
        response = response['virtualmachine']
        response = {
            'template_name_or_list': 'run_instance.xml',
            'response_type': 'RunInstancesResponse',
            'response': response
        }

    return response


@helpers.authentication_required
def start_instance():
    """
    Starts an instance.

    @return: Response.
    """
    helpers.require_parameters(['InstanceId.1'])
    instance_id = helpers.get('InstanceId.1')
    previous_state = describe_instance_by_id(instance_id)
    new_state = _start_instance_request(instance_id)
    return _modify_instance_state_response(
        'StartInstancesResponse',
        previous_state,
        new_state
    )


def _start_instance_request(instance_id):
    """
    Request to start an instance.

    @param instance_id: Id of instance to start.
    @return: Response.
    """
    args = {'command': 'startVirtualMachine',
            'id': instance_id}

    response = requester.make_request_async(args)

    response = response['virtualmachine']

    return response


def _modify_instance_state_response(response_type, previous_state, new_state):
    """
    Generates a response for a Start, Stop, Terminate requests.

    @param response_type: Cloudstack response.
    @param previous_state: The previous state of the instance.
    @param new_state: The new state of the instance.
    @return: Response.
    """
    response = {
        'template_name_or_list': 'change_instance_state.xml',
        'response_type': response_type,
        'previous_state': previous_state,
        'new_state': new_state
    }

    return response


@helpers.authentication_required
def stop_instance():
    """
    Stop an instance.

    @return: Response.
    """
    helpers.require_parameters(['InstanceId.1'])
    instance_id = helpers.get('InstanceId.1')
    previous_state = describe_instance_by_id(instance_id)
    new_state = _stop_instance_request(instance_id)
    return _modify_instance_state_response(
        'StopInstancesResponse',
        previous_state,
        new_state
    )


def _stop_instance_request(instance_id):
    """
    Request to stop an instance.

    @param instance_id: Id of instance to stop.
    @return: Response.
    """
    args = {'command': 'stopVirtualMachine',
            'id': instance_id}
    response = requester.make_request_async(args)
    response = response['virtualmachine']
    return response


@helpers.authentication_required
def terminate_instance():
    """
    Terminate an instance.

    @return: Response.
    """
    helpers.require_parameters(['InstanceId.1'])
    instance_id = helpers.get('InstanceId.1')
    previous_state = describe_instance_by_id(instance_id)
    new_state = _terminate_instance_request(instance_id)
    return _modify_instance_state_response(
        'TerminateInstancesResponse',
        previous_state,
        new_state
    )


def _terminate_instance_request(instance_id):
    """
    Request to terminate an instance.

    @param instance_id: Id of instance to terminate.
    @return: Response.
    """
    args = {'command': 'destroyVirtualMachine',
            'id': instance_id}

    response = requester.make_request_async(args)

    response = response['virtualmachine']

    return response
