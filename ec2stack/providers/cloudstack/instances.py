#!/usr/bin/env python
# encoding: utf-8

from ec2stack.providers import cloudstack

from ec2stack import helpers, errors


@helpers.authentication_required
def describe_instances():
    args = {}
    args['command'] = 'listVirtualMachines'
    response = cloudstack.describe_item(
        args, 'virtualmachine', errors.invalid_instance_id, 'InstanceId'
    )

    return _describe_instances_response(
        response
    )


def describe_instance_by_id(instance_id):
    args = {}
    args['id'] = instance_id
    args['command'] = 'listVirtualMachines'
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
    helpers.require_parameters(['InstanceId', 'Attribute'])
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
