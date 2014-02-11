#!/usr/bin/env python
# encoding: utf-8

from ..helpers import authentication_required


@authentication_required
def describe():
    items = [
        {
            'id': '1',
            'state': 'running',
            'launch_time': 'YYYY-MM-DDTHH:MM:SS+0000',
            'hypervisor': 'dummy-hypervisor'
        },
        {
            'id': '2',
            'state': 'running',
            'launch_time': 'YYYY-MM-DDTHH:MM:SS+0000',
            'hypervisor': 'dummy-hypervisor'
        }
    ]

    return {
        'template_name_or_list': 'describe_items_response.xml',
        'response_type': 'DescribeInstancesResponse',
        'reservation_id': 'dummy_request_id',
        'owner_id': 'dummy_owner_id',
        'items': items,
        'item_to_describe': 'instance'
    }
