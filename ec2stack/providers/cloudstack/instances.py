#!/usr/bin/env python
# encoding: utf-8

from ec2stack.helpers import *
from ec2stack.providers.cloudstack import requester, translator


cloudstack_instance_attributes_to_aws = {
    'templateid': 'imageid',
    'serviceofferingname': 'instanceType',
    'id': 'instanceId',
    'created': 'launchTime'
}


@authentication_required
def describe_instances():
    if contains_parameter('InstanceId.1'):
        instances = _describe_specific_instances()
    else:
        instances = _describe_all_instances()

    response =  _create_describe_instances_response(instances)

    return response


@authentication_required
def describe_instance_attribute():
    require_parameters(['InstanceId', 'Attribute'])
    instance_id = get('InstanceId', request.form)
    attribute = get('Attribute', request.form)

    response = _describe_virtual_machine_by_id(instance_id)
    virtual_machine = response['virtualmachine'][0]
    
    instance_attribute = translator.cloudstack_item_attribute_to_aws(
        virtual_machine, cloudstack_instance_attributes_to_aws, attribute)

    response = _create_describe_instance_attribute_response(instance_attribute)

    return response


def _describe_virtual_machines_request(args=None):
    if not args:
        args = {}

    args['command'] = 'listVirtualMachines'

    cloudstack_response = requester.make_request(args)

    cloudstack_response = cloudstack_response['listvirtualmachinesresponse']

    return cloudstack_response


def _describe_all_instances():
    response = _describe_virtual_machines_request()
    instances = _get_instances_from_response(response)

    return instances


def _describe_specific_instances():
    instance_ids = get_request_paramaters('InstanceId')
    instances = []
    
    for instance_id in instance_ids:
        response = _describe_virtual_machine_by_id(instance_id)
        instances = instances + _get_instances_from_response(response)

    return instances


def _describe_virtual_machine_by_id(instance_id):
    args = {
        'id': instance_id
    }

    return _describe_virtual_machines_request(args)


def _get_instances_from_response(response):
    instances = []
    if response:
        for virtual_machine in response['virtualmachine']:
            instances.append(
                translator.cloudstack_item_to_aws(
                        virtual_machine, 
                        cloudstack_instance_attributes_to_aws
                )
            )

    return instances


def _create_describe_instance_attribute_response(item_attribute):
    response = {
        'template_name_or_list': 'instance_attribute.xml',
        'response_type': 'DescribeInstanceAttributes',
        'attribute': get('Attribute', request.form),
        'value': item_attribute.values()[0],
        'id': get('InstanceId', request.form)
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
