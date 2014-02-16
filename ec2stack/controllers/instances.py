#!/usr/bin/env python
# encoding: utf-8

from ec2stack.helpers import authentication_required, contains_parameter, get
from ec2stack.controllers.cloudstack import requester
from flask import request


@authentication_required
def describe_instances():
    if contains_parameter('InstanceId.1'):
        instances = _describe_specific_instances()
    else:
        instances = _describe_all_instances()

    return _create_describe_instances_format_response(instances)


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


def _get_instances_from_response(response):
    instances = []
    response = response['listvirtualmachinesresponse']
    if response:
        for virtual_machine in response['virtualmachine']:
            instances.append(
                _cloudstack_virtual_machine_to_aws(virtual_machine)
            )

    return instances


def _cloudstack_virtual_machine_to_aws(response):
    instance = {
        'id': response['id'],
        'name': response['name'],
        'state': response['state'].upper(),
        'availability_zone': response['zonename'],
        'hypervisor': response['hypervisor'],
        'imageid': response['templateid'],
        'launch_time': response['created'],
        'instance_type': response['serviceofferingname'],
    }

    return instance


def _create_describe_instances_format_response(instances):
    response = {
        'template_name_or_list': 'describe_instances.xml',
        'response_type': 'DescribeInstancesResponse',
        'reservation_id': 'None',
        'instances': instances,
        'item_to_describe': 'instance'
    }

    return response
