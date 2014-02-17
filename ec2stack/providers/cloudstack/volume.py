#!/usr/bin/env python
# encoding: utf-8

from flask import request

from ec2stack import helpers
from ec2stack.helpers import authentication_required
from ec2stack.providers.cloudstack import requester


@authentication_required
def delete_volume():
    helpers.require_parameters(['VolumeId'])
    response = _delete_security_group_request()
    return _delete_security_group_response(response)


def _delete_security_group_request():
    args = {}
    args['command'] = 'deleteVolume'
    args['id'] = helpers.get('VolumeId', request.form)

    response = requester.make_request(args)

    return response


def _delete_security_group_response(response):
    return {
        'template_name_or_list': 'delete_item.xml',
        'response_type': 'DeleteVolumeResponse',
        'return': 'true'
    }
