#!/usr/bin/env python
# encoding: utf-8

from ec2stack.helpers import *
from ec2stack.controllers.cloudstack import requester
from flask import request


cloudstack_attributes_to_aws = {
    'id': 'id',
    'name': 'name',
    'state': 'state',
    'zonename': 'availability_zone',
    'hypervisor': 'hypervisor',
    'templateid': 'imageid',
    'created': 'launchTime',
    'serviceofferingname': 'instanceType'
}


@authentication_required
def describe_instances():
    if contains_parameter('InstanceId.1'):
        instances = _describe_specific_instances()
    else:
        instances = _describe_all_instances()

    return _create_describe_instances_response(instances)


def describe_instance_attribute():
    require_parameters(['InstanceId', 'Attribute'])
    instance_id = get('InstanceId', request.form)
    attribute = get('Attribute', request.form)

    response = _describe_virtual_machine(instance_id)
    instance = _get_instances_from_response(response, attribute)

    response = _create_describe_instance_attribute_response(instance, attribute)
    return response


def _describe_virtual_machines_request(args=None):
    if not args:
        args = {}

    args['command'] = 'listVirtualMachines'

    response = requester.make_request(args)

    return response


def _describe_all_instances():
    response = _describe_virtual_machines_request()
    instances = _get_instances_from_response(response)

    return instances


def _describe_specific_instances():
    current_instance_num = 1
    current_instance = 'InstanceId.' + str(current_instance_num)
    instances = []

    while contains_parameter(current_instance):
        instance_id = get(current_instance, request.form)
        response = _describe_virtual_machine(instance_id)
        instances = instances + _get_instances_from_response(response)
        current_instance_num += 1
        current_instance = 'InstanceId.' + str(current_instance_num)

    return instances


def _describe_virtual_machine(instance_id):
    args = {
        'keyword': instance_id
    }

    return _describe_virtual_machines_request(args)


def _get_instances_from_response(response, attribute=None):
    instances = []
    response = response['listvirtualmachinesresponse']
    if response:
        for virtual_machine in response['virtualmachine']:
            instances.append(
                _cloudstack_virtual_machine_to_aws(virtual_machine, attribute)
            )

    return instances


def _cloudstack_virtual_machine_to_aws(response, attribute=None):
    instance = {}
    if attribute is not None:
        if response[attribute] is not None:
            instance[cloudstack_attributes_to_aws[attribute]] = response[attribute]
    else:
        for cloudstack_attr, aws_attr in cloudstack_attributes_to_aws.iteritems():
            instance[aws_attr] = response[cloudstack_attr]

    return instance


def _create_describe_instance_attribute_response(response, attribute):
    response = {
        'template_name_or_list': 'instance_attribute.xml',
        'response_type': 'DescribeInstanceAttributes',
        'attribute': cloudstack_attributes_to_aws[attribute],
        'value': response[0][cloudstack_attributes_to_aws[attribute]]
    }

    return response


def _create_describe_instances_response(instances):
    response = {
        'template_name_or_list': 'instances.xml',
        'response_type': 'DescribeInstancesResponse',
        'reservation_id': 'None',
        'instances': instances
    }

    return response
