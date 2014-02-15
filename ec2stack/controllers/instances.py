#!/usr/bin/env python
# encoding: utf-8

from ec2stack import helpers
from flask import request
from ec2stack.helpers import authentication_required
from ec2stack.controllers.cloudstack import requester


def _get_virtual_machines(args=None):
    if not args:
        args = {}

    args['command'] = 'listVirtualMachines'
    args['apikey'] = helpers.get('AWSAccessKeyId', request.form)
    user = helpers.get_secretkey()

    cloudstack_response = requester.make_request(args, user)

    return cloudstack_response


def _cloudstack_virtual_machine_to_aws(cloudstack_response):
    return {
        'id': cloudstack_response['id'],
        'name': cloudstack_response['name'],
        'state': translate_image_status[str(cloudstack_response['isready'])]
    }


@authentication_required
def describe_instances():
    virtual_machines = _get_virtual_machines()
    items = []

    if virtual_machines['listvirtualmachinesresponse']:
        for virtual_machine in virtual_machines['listvirtualmachinesresponse']['virtualmachine']:
            items.append(
                _cloudstack_template_to_aws(virtual_machine)
            )

    return {
        'template_name_or_list': 'describe_items_response.xml',
        'response_type': 'DescribeInstancesResponse',
        'reservation_id': 'dummy_request_id',
        'owner_id': 'dummy_owner_id',
        'items': items,
        'item_to_describe': 'instance'
    }
