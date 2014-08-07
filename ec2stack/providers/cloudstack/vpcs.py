#!/usr/bin/env python
# encoding: utf-8

"""This module contains functions for handling requests in relation to vpcs.
"""

import uuid

from flask import current_app

from ec2stack import errors
from ec2stack import helpers
from ec2stack.providers import cloudstack
from ec2stack.providers.cloudstack import requester, zones


@helpers.authentication_required
def create_vpc():
    """
    Create a vpc.

    @return: Response.
    """
    response = _create_vpc_request()
    return _create_vpc_response(response)


def _create_vpc_request():
    """
    Request to create a vpc.

    @return: Response.
    """
    args = {'command': 'createVPC'}
    name = uuid.uuid1()
    args['name'] = name
    args['displaytext'] = name
    args['zoneid'] = zones.get_zone(
        current_app.config['CLOUDSTACK_DEFAULT_ZONE'])['id']

    if 'VPC_OFFERING_ID' in current_app.config:
        args['vpcofferingid'] = current_app.config['VPC_OFFERING_ID']
    else:
        errors.invalid_request(
            str('VPC_OFFERING_ID') + " not found in configuration, " +
            "please run ec2stack-configure -a True")

    args['cidr'] = helpers.get('CidrBlock')

    response = requester.make_request_async(args)

    return response


def _create_vpc_response(response):
    """
    Generates a response for create vpc request.

    @param response: Response from Cloudstack.
    @return: Response.
    """
    if 'errortext' in response:
        errors.invalid_vpc_range()
    else:
        response = response['vpc']
        return {
            'template_name_or_list': 'create_vpc.xml',
            'response_type': 'CreateVpcResponse',
            'response': response
        }


@helpers.authentication_required
def delete_vpc():
    """
    Delete a vpc.

    @return: Response.
    """
    helpers.require_parameters(['VpcId'])
    _delete_vpc_request()
    return _delete_vpc_response()


def _delete_vpc_request():
    """
    Request to delete a vpc.

    @return: Response.
    """
    args = {'command': 'deleteVPC', 'id': helpers.get('VpcId')}

    response = requester.make_request_async(args)

    return response


def _delete_vpc_response():
    """
    Generates a response for delete vpc request.

    @return: Response.
    """
    return {
        'template_name_or_list': 'status.xml',
        'response_type': 'DeleteVpcResponse',
        'return': 'true'
    }


@helpers.authentication_required
def describe_vpcs():
    """
    Describes a specific vpc or all vpcs.

    @return: Response.
    """
    args = {'command': 'listVPCs'}
    response = cloudstack.describe_item(
        args, 'vpc', errors.invalid_vpc_id, 'VpcId'
    )

    return _describe_vpc_response(
        response
    )


def _describe_vpc_response(response):
    """
    Generates a response for describe vpc request.

    @param response: Response from Cloudstack.
    @return: Response.
    """
    return {
        'template_name_or_list': 'vpcs.xml',
        'response_type': 'DescribeVpcsResponse',
        'response': response
    }
