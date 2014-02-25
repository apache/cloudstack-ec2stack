#!/usr/bin/env python
# encoding: utf-8

from ec2stack import helpers
from ec2stack.providers.cloudstack import requester


@helpers.authentication_required
def describe_instances():
    if helpers.contains_parameter_with_keyword('InstanceId.'):
        response = _describe_specific_instances()
    else:
        response = _describe_all_instances()

    response = _describe_instances_response(response)

    return response


def _describe_all_instances():
    response = _describe_virtual_machines_request()
    return response


def _describe_specific_instances():
    instance_id_keys = helpers.get_request_parameter_keys('InstanceId.')

    response = {}
    response['virtualmachine'] = []

    for instance_id_key in instance_id_keys:
        instance_id = helpers.get(instance_id_key)
        instance_response = describe_instance_by_id(instance_id)
        response['virtualmachine'].append(instance_response)

    return response


def describe_instance_by_id(instance_id):
    args = {}
    args['id'] = instance_id
    response = _describe_virtual_machines_request(args)
    response = response['virtualmachine'][0]
    return response


def _describe_virtual_machines_request(args=None):
    if not args:
        args = {}

    args['command'] = 'listVirtualMachines'

    cloudstack_response = requester.make_request(args)
    cloudstack_response = cloudstack_response['listvirtualmachinesresponse']

    return cloudstack_response


def _describe_instances_response(response):
    return {
        'template_name_or_list': 'instances.xml',
        'response_type': 'DescribeInstancesResponse',
        'response': response
    }


@helpers.authentication_required
def describe_instance_attribute():
    instance_id = helpers.get('InstanceId')

    response = describe_instance_by_id(instance_id)

    return _describe_instance_attribute_response(response)


def _describe_instance_attribute_response(response):
    attribute = helpers.get('Attribute')

    response = {
        'template_name_or_list': 'instance_attribute.xml',
        'response_type': 'DescribeInstanceAttributeResponse',
        'attribute': attribute,
        'id': response['id'],
        'value': response[attribute]
    }

    return response
