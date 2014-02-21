#!/usr/bin/env python
# encoding: utf-8

import uuid

from flask import request

from ec2stack import helpers
from ec2stack.helpers import authentication_required
from ec2stack.providers.cloudstack import requester, translator, \
        disk_offerings, cloudstack_helpers


cloudstack_volume_attributes_to_aws = {
    'id': 'volumeId',
    'virtualmachineid': 'instanceId',
    'created': 'createTime'
}


@authentication_required
def describe_volumes():
    response = _describe_all_volumes()
    return describe_volumes_response(response)


@authentication_required
def delete_volume():
    helpers.require_parameters(['VolumeId'])
    response = _delete_volume_request()
    return delete_volume_response(response)


@authentication_required
def create_volume():
    helpers.require_one_paramater(['SnapshotId', 'Size'])

    if helpers.contains_parameter('SnapshotId'):
        args['snapshotid'] = helpers.get('SnapshotId', request.form)
    else:
        args['size'] = helpers.get('Size', request.form)
        args['diskofferingid'] = \
            disk_offerings.get_disk_offerings_id_by_name('Custom')
            
    response = _create_volume_request()
    return create_volume_response(response)


@authentication_required
def attach_volume():
    helpers.require_parameters(['VolumeId', 'InstanceId'])
    response = _attach_volume_request()
    return attach_volume_response(response)


def _describe_all_volumes():
    response = _describe_volumes_request()
    volumes = cloudstack_helpers.get_items_from_response(
        response, 'volume', cloudstack_volume_attributes_to_aws)
    return volumes


def _describe_volumes_request():
    args = {}
    args['command'] = 'listVolumes'

    response = requester.make_request(args)
    response = response['listvolumesresponse']

    return response


def _create_volume_request():
    args = {}
    args['zoneid'] = helpers.get('AvailabilityZone', request.form)
    args['command'] = 'createVolume'
    args['name'] = uuid.uuid4()

    response = requester.make_request(args)

    response = response['createvolumeresponse']

    return response


def _attach_volume_request():
    args = {}
    args['command'] = 'attachVolume'
    args['id'] = helpers.get('VolumeId', request.form)
    args['virtualmachineid'] = helpers.get('InstanceId', request.form)

    response = requester.make_request(args)
    response = response['attachvolumeresponse']

    return response


def _delete_volume_request():
    args = {}
    args['command'] = 'deleteVolume'
    args['id'] = helpers.get('VolumeId', request.form)

    response = requester.make_request(args)

    return response


def attach_volume_response(response):
    return {
        'template_name_or_list': 'attach_volume.xml',
        'response_type': 'AttachVolumeResponse',
        'volume_id': response['id'],
        'instance_id': response['virtualmachineid'],
        'device': response['deviceid'],
        'status': response['state'],
        'attach_time': response['created']
    }


def describe_volumes_response(volumes):
    response = {
        'template_name_or_list': 'volumes.xml',
        'response_type': 'DescribeVolumesResponse',
        'volumes': volumes,
    }

    return response


def create_volume_response(response):
    response = {
        'template_name_or_list': 'create_volume.xml',
        'response_type': 'CreateVolumeResponse',
        'id': response['id'],
        'status': 'creating',
        'volumeType': 'standard',
        'zone': helpers.get('AvailabilityZone', request.form),
        'size': helpers.get('Size', request.form)
    }

    return response


def delete_volume_response(response):
    return {
        'template_name_or_list': 'delete_item.xml',
        'response_type': 'DeleteVolumeResponse',
        'return': 'true'
    }
