#!/usr/bin/env python
# encoding: utf-8

"""This module contains functions for handling requests in relation to volumes
"""

import uuid

from flask import current_app

from ec2stack import errors
from ec2stack import helpers
from ec2stack.providers import cloudstack
from ec2stack.providers.cloudstack import requester, disk_offerings, zones


@helpers.authentication_required
def attach_volume():
    """
    Attach a volume to the specified instance.

    @return: Response.
    """
    helpers.require_parameters(['VolumeId', 'InstanceId', 'Device'])
    response = _attach_volume_request()
    return _attach_volume_response(response)


def _attach_volume_request():
    """
    Request to attach a volume.

    @return: Response.
    """
    args = {}

    volume_id = helpers.get('VolumeId')
    instance_id = helpers.get('InstanceId')
    device = helpers.get('Device')

    args['id'] = volume_id
    args['command'] = 'attachVolume'
    args['virtualmachineid'] = instance_id
    args['device'] = device

    response = requester.make_request_async(args)

    return response


def _attach_volume_response(response):
    """
    Generates a response for attach volume request.

    @param response: Response from Cloudstack.
    @return: Response.
    """
    if 'errortext' in response:
        if 'specify a volume that is not attached' in response['errortext']:
            errors.invalid_volume_attached()
        elif 'Invalid parameter virtualmachineid' in response['errortext']:
            errors.invalid_instance_id()
        elif 'Invalid parameter id' in response['errortext']:
            errors.invalid_volume_id()
        else:
            errors.invalid_request(response['errortext'])

    response = response['volume']
    return {
        'template_name_or_list': 'volume_attachment.xml',
        'response_type': 'AttachVolumeResponse',
        'response': response
    }


@helpers.authentication_required
def create_volume():
    """
    Create a volume.

    @return: Response.
    """
    response = _create_volume_request()
    return _create_volume_response(response)


def _create_volume_request():
    """
    Request to create a volume.

    @return: Response.
    """
    args = {}

    if helpers.contains_parameter('SnapshotId'):
        args['snapshotid'] = helpers.get('SnapshotId')

    else:
        helpers.require_parameters(['Size'])
        args['size'] = helpers.get('Size')
        args['diskofferingid'] = disk_offerings.get_disk_offering(
            current_app.config['CLOUDSTACK_CUSTOM_DISK_OFFERING']
        )['id']

    zone_name = helpers.get('AvailabilityZone')
    zone_id = zones.get_zone(zone_name)['id']

    args['zoneid'] = zone_id
    args['command'] = 'createVolume'
    args['name'] = uuid.uuid1()

    response = requester.make_request_async(args)

    return response


def _create_volume_response(response):
    """
    Generates a response for create volume request.

    @param response: Response from Cloudstack.
    @return: Response.
    """
    if 'errortext' in response:
        if 'unable to find a snapshot with id' in response['errortext']:
            errors.invalid_snapshot_id()
        else:
            errors.invalid_request(response['errortext'])

    response = response['volume']
    return {
        'template_name_or_list': 'create_volume.xml',
        'response_type': 'CreateVolumeResponse',
        'response': response
    }


@helpers.authentication_required
def delete_volume():
    """
    Delete a volume.

    @return: Response
    """
    helpers.require_parameters(['VolumeId'])
    response = _delete_volume_request()

    return _delete_volume_response(response)


def _delete_volume_request():
    """
    Request to delete a volume.

    @return: Response.
    """
    args = {'id': helpers.get('VolumeId'), 'command': 'deleteVolume'}

    response = requester.make_request(args)
    response = response['deletevolumeresponse']

    return response


def _delete_volume_response(response):
    """
    Generates a response for delete volume request.

    @param response: Response from Cloudstack.
    @return: Response.
    """
    if 'errortext' in response:
        if 'Unable to aquire volume' in response['errortext']:
            errors.invalid_volume_id()
        else:
            errors.invalid_request(response['errortext'])

    return {
        'template_name_or_list': 'status.xml',
        'response_type': 'DeleteVolumeResponse',
        'return': 'true'
    }


@helpers.authentication_required
def describe_volumes():
    """
    Describes a specific volume or all volumes.

    @return: Response.
    """
    args = {'command': 'listVolumes'}
    response = cloudstack.describe_item(
        args, 'volume', errors.invalid_volume_id, 'VolumeId'
    )

    return _describe_volumes_response(
        response
    )


def _describe_volumes_response(response):
    """
    Generates a response for describe volumes request.

    @param response: Response from Cloudstack.
    @return: Response.
    """
    return {
        'template_name_or_list': 'volumes.xml',
        'response_type': 'DescribeVolumesResponse',
        'response': response,
    }


@helpers.authentication_required
def detach_volume():
    """
    Detach a specified volume.

    @return: Response.
    """
    helpers.require_parameters(['VolumeId'])
    response = _detach_volume_request()
    return _detach_volume_response(response)


def _detach_volume_request():
    """
    Request to detach a volume.

    @return: Response.
    """
    args = {}

    volume_id = helpers.get('VolumeId')

    if helpers.contains_parameter('InstanceId'):
        args['virtualmachineid'] = helpers.get('InstanceId')
    if helpers.contains_parameter('Device'):
        args['deviceid'] = helpers.get('Device')

    args['id'] = volume_id
    args['command'] = 'detachVolume'

    response = requester.make_request_async(args)

    return response


def _detach_volume_response(response):
    """
    Generates a response for detach volume request.

    @param response: Response from Cloudstack.
    @return: Response.
    """
    if 'errortext' in response:
        if 'specified volume is not attached' in response['errortext']:
            errors.invalid_volume_detached()
        elif 'Invalid parameter virtualmachineid' in response['errortext']:
            errors.invalid_instance_id()
        elif 'Invalid parameter id' in response['errortext']:
            errors.invalid_volume_id()
        else:
            errors.invalid_request(response['errortext'])

    response = response['volume']
    return {
        'template_name_or_list': 'volume_attachment.xml',
        'response_type': 'DetachVolumeResponse',
        'response': response
    }
