#!/usr/bin/env python
# encoding: utf-8

from flask import request

from ec2stack import helpers
from ec2stack.helpers import authentication_required
from ec2stack.core import Ec2stackError
from ec2stack.providers.cloudstack import requester


@authentication_required
def create_security_group():
    helpers.require_parameters(['GroupName', 'GroupDescription'])
    response = _create_security_group_request()
    return _create_security_group_response(response)


def _create_security_group_request():
    args = {}
    args['command'] = 'createSecurityGroup'
    args['name'] = helpers.get('GroupName', request.form)
    args['description'] = helpers.get('GroupDescription', request.form)

    response = requester.make_request(args)

    response = response['createsecuritygroupresponse']

    return response


def _create_security_group_response(response):
    if 'errortext' in response:
        groupname = helpers.get('GroupName', request.form)
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


def delete_security_group():
    response = _delete_security_group_request()
    return _delete_security_group_response(response)


def _delete_security_group_request():
    args = {}

    if helpers.contains_parameter('GroupName'):
        args['name'] = helpers.get('GroupName', request.form)

    elif helpers.contains_parameter('GroupId'):
        args['id'] = helpers.get('GroupId', request.form)

    else:
        helpers.missing_paramater('GroupName')

    args['command'] = 'deleteSecurityGroup'

    response = requester.make_request(args)

    return response


def _delete_security_group_response(response):
    return {
        'template_name_or_list': 'delete_security_group.xml',
        'response_type': 'DeleteSecurityGroupResponse',
        'return': 'true'
    }
