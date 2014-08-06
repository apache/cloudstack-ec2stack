#!/usr/bin/env python
# encoding: utf-8

"""This module contains functions for handling requests in relation to snapshots.
"""

import uuid

from flask import current_app

from ec2stack import errors
from ec2stack import helpers
from ec2stack.providers import cloudstack
from ec2stack.providers.cloudstack import requester, zones


@helpers.authentication_required
def create_snapshot():
    """
    Create a snapshot.

    @return: Response.
    """
    response = _create_snapshot_request()
    return _create_snapshot_response(response)


def _create_snapshot_request():
    """
    Request to create a snapshot.

    @return: Response.
    """
    args = {'command': 'createSnapshot'}

    response = requester.make_request_async(args)

    return response


def _create_snapshot_response(response):
    """
    Generates a response for create snapshot request.

    @param response: Response from Cloudstack.
    @return: Response.
    """

    response = response['snapshot']
    return {
        'template_name_or_list': 'create_snapshot.xml',
        'response_type': 'CreateSnapshotResponse',
        'response': response
    }


@helpers.authentication_required
def delete_snapshot():
    """
    Delete a snapshot.

    @return: Response.
    """
    helpers.require_parameters(['SnapshotId'])
    _delete_snapshot_request()
    return _delete_snapshot_response()


def _delete_snapshot_request():
    """
    Request to delete a snapshot.

    @return: Response.
    """
    args = {'command': 'deleteSnapshot', 'id': helpers.get('SnapshotId')}

    response = requester.make_request_async(args)

    return response


def _delete_snapshot_response():
    """
    Generates a response for delete snapshot request.

    @return: Response.
    """
    return {
        'template_name_or_list': 'status.xml',
        'response_type': 'DeleteSnapshotResponse',
        'return': 'true'
    }


@helpers.authentication_required
def describe_snapshots():
    """
    Describes a specific snapshot or all snapshots.

    @return: Response.
    """
    args = {'command': 'listSnapshots'}
    response = cloudstack.describe_item(
        args, 'snapshot', errors.invalid_snapshot_id, 'SnapshotId'
    )

    return _describe_snapshot_response(
        response
    )


def _describe_snapshot_response(response):
    """
    Generates a response for describe snapshot request.

    @param response: Response from Cloudstack.
    @return: Response.
    """
    return {
        'template_name_or_list': 'snapshots.xml',
        'response_type': 'DescribeSnapshotsResponse',
        'response': response
    }
