#!/usr/bin/env python
# encoding: utf-8

from flask import request, abort

from ec2stack.helpers import authentication_required, get, \
    contains_parameter, missing_paramater, require_one_paramater, require_parameters
from ec2stack.core import Ec2stackError
from ec2stack.providers.cloudstack import requester


@authentication_required
def create_security_group():
    require_parameters(['GroupName', 'GroupDescription'])
    response = _create_security_group_request()
    return _create_security_group_response(response)


def _create_security_group_request():
    args = {}
    args['command'] = 'createSecurityGroup'
    args['name'] = get('GroupName', request.form)
    args['description'] = get('GroupDescription', request.form)

    response = requester.make_request(args)

    response = response['createsecuritygroupresponse']

    return response


def _create_security_group_response(response):
    if 'errortext' in response:
        groupname = get('GroupName', request.form)
        raise Ec2stackError(
            '400',
            'InvalidGroupName.Duplicate',
            'The groupname \'%s\' already exists.' % groupname
        )
    else:
        response = response['securitygroup']
        return {
            'template_name_or_list': 'create_security_group.xml',
            'response_type': 'CreateSecurityGroupResponse',
            'id': response['id'],
            'return': 'true'
        }


@authentication_required
def delete_security_group():
    response = _delete_security_group_request()
    return _delete_security_group_response(response)


def _delete_security_group_request():
    args = {}

    if contains_parameter('GroupName'):
        args['name'] = get('GroupName', request.form)

    elif contains_parameter('GroupId'):
        args['id'] = get('GroupId', request.form)

    else:
        missing_paramater('GroupName')

    args['command'] = 'deleteSecurityGroup'

    response = requester.make_request(args)

    return response


def _delete_security_group_response(response):
    return {
        'template_name_or_list': 'delete_item.xml',
        'response_type': 'DeleteSecurityGroupResponse',
        'return': 'true'
    }


@authentication_required
def authenticate_security_group_ingress():
    require_one_paramater(['GroupName', 'GroupId'])
    _authenticate_security_group_request()
    return abort(400)
    #return _authenticate_security_group_response(response)


def _authenticate_security_group_request(args=None):
    if not args:
        args = {}

    args['command'] = 'authorizeSecurityGroupIngress'

    if contains_parameter('GroupName'):
        args['securityGroupName'] = get('GroupName', request.form)
    elif contains_parameter('GroupId'):
        args['securityGroupId'] = get('GroupId', request.form)

    args['protocol'] = get('IpPermissions.1.IpProtocol', request.form)
    args['startPort'] = get('FromPort', request.form)
    args['endPort'] = get('ToPort', request.form)
    args['cidrlist'] = get('CidrIp', request.form)

    response = requester.make_request_async(args)

    response = response['securitygroup']

    return response
