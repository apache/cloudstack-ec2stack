#!/usr/bin/env python
# encoding: utf-8

from ec2stack.helpers import authentication_required


def _get_virtual_machines(args=None):
    if not args:
        args = {}

    command = 'listVirtualMachines'

    '''Get genuine response here using listVirtualMachines
       None response for now'''
    cloudstack_response = {}

    return cloudstack_response


def _cloudstack_virtual_machine_to_aws(cloudstack_response):
    instance = [
        {
            'id': '1',
            'state': 'running',
            'launch_time': 'YYYY-MM-DDTHH:MM:SS+0000',
            'hypervisor': 'dummy-hypervisor'
        }
    ]

    return instance


@authentication_required
def describe_instances():
    virtual_machines = {}
    items = _cloudstack_virtual_machine_to_aws(virtual_machines)

    return {
        'template_name_or_list': 'describe_items_response.xml',
        'response_type': 'DescribeInstancesResponse',
        'reservation_id': 'dummy_request_id',
        'owner_id': 'dummy_owner_id',
        'items': items,
        'item_to_describe': 'instance'
    }
