#!/usr/bin/env python
# encoding: utf-8

from flask import current_app

from ec2stack.providers import cloudstack
from ec2stack.providers.cloudstack import requester, service_offerings, zones
from ec2stack import helpers, errors


@helpers.authentication_required
def describe_instances():
    args = {'command': 'listVirtualMachines'}
    response = cloudstack.describe_item(
        args, 'virtualmachine', errors.invalid_instance_id, 'InstanceId'
    )

    return _describe_instances_response(
        response
    )


def describe_instance_by_id(instance_id):
    args = {'id': instance_id, 'command': 'listVirtualMachines'}
    response = cloudstack.describe_item_request(
        args, 'virtualmachine', errors.invalid_instance_id
    )
    return response


def _describe_instances_response(response):
    return {
        'template_name_or_list': 'instances.xml',
        'response_type': 'DescribeInstancesResponse',
        'response': response
    }


@helpers.authentication_required
def describe_instance_attribute():
    instance_id = helpers.get('InstanceId')
    attribute = helpers.get('Attribute')

    supported_attribute_map = {
        'instanceType': 'serviceofferingname',
        'groupSet': 'securitygroup'
    }

    if attribute not in supported_attribute_map.iterkeys():
        errors.invalid_paramater_value(
            'The specified attribute is not valid, please specify a valid ' +
            'instance attribute.'
        )

    response = describe_instance_by_id(instance_id)
    return _describe_instance_attribute_response(
        response, attribute, supported_attribute_map)


def _describe_instance_attribute_response(response, attribute, attr_map):
    response = {
        'template_name_or_list': 'instance_attribute.xml',
        'response_type': 'DescribeInstanceAttributeResponse',
        'attribute': attribute,
        'response': response[attr_map[attribute]],
        'id': response['id']
    }

    return response


@helpers.authentication_required
def run_instance():
    helpers.require_parameters(
        ['ImageId', 'InstanceType', 'MinCount', 'MaxCount'])
    response = _run_instance_request()
    return _run_instance_response(response)


def _run_instance_request():
    args = {}

    # TODO setup mappings for this.....
    # if helpers.get('InstanceType') in current_app.config['InstanceMappings']:
    #    instance_type = helpers.get('InstanceType')
    # else:
    instance_type = helpers.get('InstanceType')

    args['serviceofferingid'] = \
        service_offerings.get_service_offering(instance_type)['id']
    args['templateid'] = helpers.get('ImageId')

    if helpers.contains_parameter('Placement.AvailabilityZone'):
        args['zoneid'] = zones.get_zone(
            helpers.get('Placement.AvailabilityZone')
        )
    else:
        args['zoneid'] = zones.get_zone(
            current_app.config['CLOUDSTACK_DEFAULT_ZONE']
        )['id']

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
    if 'errortext' in response:
        if 'Invalid parameter templateid' in response['errortext']:
            errors.invalid_image_id()
        elif 'Unable to find group' in response['errortext']:
            errors.invalid_security_group()
        elif 'Invalid parameter securitygroupids' in response['errortext']:
            errors.invalid_security_group()
        elif 'A key pair with name' in response['errortext']:
            errors.invalid_keypair_name()
        else:
            errors.invalid_paramater_value(response['errortext'])
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
    helpers.require_parameters(['InstanceId.1'])
    instance_id = helpers.get('InstanceId.1')
    previous_instance_state_description = describe_instance_by_id(instance_id)
    new_instance_state_description = _start_instance_request(instance_id)
    return _start_instance_response(
        previous_instance_state_description,
        new_instance_state_description
    )


def _start_instance_request(instance_id):
    args = {'command': 'startVirtualMachine',
            'id': instance_id}

    response = requester.make_request_async(args)

    response = response['virtualmachine']

    return response


def _start_instance_response(previous_state, new_state):
    response = {
        'template_name_or_list': 'change_instance_state.xml',
        'response_type': 'StartInstancesResponse',
        'previous_state': previous_state,
        'new_state': new_state
    }

    return response


@helpers.authentication_required
def terminate_instance():
    helpers.require_parameters(['InstanceId.1'])
    instance_id = helpers.get('InstanceId.1')
    previous_instance_state_description = describe_instance_by_id(instance_id)
    new_instance_state_description = _terminate_instance_request(instance_id)
    return _terminate_instance_response(
        previous_instance_state_description,
        new_instance_state_description
    )


def _terminate_instance_request(instance_id):
    args = {'command': 'destroyVirtualMachine',
            'id': instance_id}

    response = requester.make_request_async(args)

    response = response['virtualmachine']

    return response


def _terminate_instance_response(previous_state, new_state):
    response = {
        'template_name_or_list': 'change_instance_state.xml',
        'response_type': 'TerminateInstancesResponse',
        'previous_state': previous_state,
        'new_state': new_state
    }

    return response


@helpers.authentication_required
def stop_instance():
    helpers.require_parameters(['InstanceId.1'])
    instance_id = helpers.get('InstanceId.1')
    previous_instance_state_description = describe_instance_by_id(instance_id)
    new_instance_state_description = _stop_instance_request(instance_id)
    return _stop_instance_response(
        previous_instance_state_description,
        new_instance_state_description
    )


def _stop_instance_request(instance_id):
    args = {'command': 'stopVirtualMachine',
            'id': instance_id}
    response = requester.make_request_async(args)
    response = response['virtualmachine']
    return response


def _stop_instance_response(previous_state, new_state):
    response = {
        'template_name_or_list': 'change_instance_state.xml',
        'response_type': 'StopInstancesResponse',
        'previous_state': previous_state,
        'new_state': new_state
    }

    return response


@helpers.authentication_required
def reboot_instance():
    helpers.require_parameters(['InstanceId.1'])
    instance_id = helpers.get('InstanceId.1')
    _reboot_instance_request(instance_id)
    return _reboot_instance_response()


def _reboot_instance_request(instance_id):
    args = {'command': 'rebootVirtualMachine',
            'id': instance_id}
    response = requester.make_request_async(args)
    response = response['virtualmachine']
    return response


def _reboot_instance_response():
    response = {
        'template_name_or_list': 'status.xml',
        'response_type': 'RebootInstancesResponse',
        'return': 'true'
    }

    return response
