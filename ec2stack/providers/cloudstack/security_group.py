#!/usr/bin/env python
# encoding: utf-8

from ec2stack import helpers, errors
from ec2stack.core import Ec2stackError
from ec2stack.providers.cloudstack import requester


@helpers.authentication_required
def create_security_group():
    helpers.require_parameters(['GroupName', 'GroupDescription'])
    response = _create_security_group_request()
    return _create_security_group_response(response)


def _create_security_group_request():
    args = {}
    args['command'] = 'createSecurityGroup'
    args['name'] = helpers.get('GroupName')
    args['description'] = helpers.get('GroupDescription')

    response = requester.make_request(args)

    response = response['createsecuritygroupresponse']

    return response


def _create_security_group_response(response):
    if 'errortext' in response:
        errors.duplicate_security_group()
    else:
        response = response['securitygroup']
        return {
            'template_name_or_list': 'create_security_group.xml',
            'response_type': 'CreateSecurityGroupResponse',
            'id': response['id'],
            'return': 'true'
        }


@helpers.authentication_required
def delete_security_group():
    _delete_security_group_request()
    return _delete_security_group_response()


def _delete_security_group_request():
    args = {}

    helpers.require_atleast_one_parameter(['GroupName', 'GroupId'])

    if helpers.contains_parameter('GroupName'):
        args['name'] = helpers.get('GroupName')

    elif helpers.contains_parameter('GroupId'):
        args['id'] = helpers.get('GroupId')

    args['command'] = 'deleteSecurityGroup'

    response = requester.make_request(args)

    return response


def _delete_security_group_response():
    return {
        'template_name_or_list': 'status.xml',
        'response_type': 'DeleteSecurityGroupResponse',
        'return': 'true'
    }


@helpers.authentication_required
def authenticate_security_group_ingress():
    response = _authenticate_security_group_request('ingress')
    return _authenticate_security_group_response(response)


@helpers.authentication_required
def authenticate_security_group_egress():
    response = _authenticate_security_group_request('egress')
    return _authenticate_security_group_response(response)


def _authenticate_security_group_request(rule_type):
    args = _parse_security_group_request()

    if rule_type == 'egress':
        args['command'] = 'authorizeSecurityGroupEgress'
    elif rule_type == 'ingress':
        args['command'] = 'authorizeSecurityGroupIngress'

    response = requester.make_request_async(args)

    return response


def _authenticate_security_group_response(response):
    if 'errortext' in response:
        if 'Failed to authorize security group' in response['errortext']:
            cidrlist = str(helpers.get('CidrIp'))
            protocol = str(helpers.get('IpProtocol'))
            from_port = str(helpers.get('FromPort'))
            to_port = str(helpers.get('toPort'))
            raise Ec2stackError(
                '400',
                'InvalidPermission.Duplicate',
                'the specified rule "peer: ' + cidrlist + ', ' + protocol +
                ', from port: ' + from_port + ', to port: ' + to_port +
                ', ALLOW" already exists'
            )
        elif 'Unable to find security group' in response['errortext']:
            errors.invalid_security_group()

        errors.invalid_paramater_value(response['errortext'])
    else:
        return {
            'template_name_or_list': 'status.xml',
            'response_type': 'AuthorizeSecurityGroupIngressResponse',
            'return': 'true'
        }


@helpers.authentication_required
def revoke_security_group_ingress():
    response = _revoke_security_group_request('ingress')
    return _authenticate_security_group_response(response)


@helpers.authentication_required
def revoke_security_group_egress():
    response = _revoke_security_group_request('egress')
    return _authenticate_security_group_response(response)


def _revoke_security_group_request(rule_type):
    args = {}

    rules = _parse_security_group_request()

    if rule_type == 'ingress':
        args['command'] = 'revokeSecurityGroupIngress'
        args['id'] = _find_rule(rules, 'ingressrule')
    elif rule_type == 'egress':
        args['command'] = 'revokeSecurityGroupEgress'
        args['id'] = _find_rule(rules, 'egressrule')

    response = requester.make_request_async(args)

    return response


def _revoke_security_group_response(response):
    if 'errortext' in response:
        errors.invalid_paramater_value(response['errortext'])
    else:
        return {
            'template_name_or_list': 'status.xml',
            'response_type': 'AuthorizeSecurityGroupIngressResponse',
            'return': 'true'
        }


def _find_rule(rule, rule_type):
    security_group = _get_security_group(rule)

    found_rules = security_group[rule_type]

    for found_rule in found_rules:
        if _compare_rules(rule, found_rule):
            return found_rule['ruleid']

    errors.invalid_permission()


def _compare_rules(left, right):
    protocol_match = str(left['protocol']) == str(right['protocol'])
    cidr_match = str(left['cidrlist']) == str(right['cidr'])

    if 'startport' in left and 'startport' in right:
        startport_match = str(left['startport']) == str(right['startport'])
    elif 'icmptype' in left and 'icmptype' in right:
        startport_match = str(left['icmptype']) == str(right['icmptype'])
    else:
        startport_match = False

    if 'endport' in left and 'endport' in right:
        endport_match = str(left['endport']) == str(right['endport'])
    elif 'icmpcode' in left and 'icmpcode' in right:
        endport_match = str(left['icmpcode']) == str(right['icmpcode'])
    else:
        endport_match = False

    return protocol_match and cidr_match and startport_match and endport_match


def _get_security_group(rule):
    response = _describe_security_groups_request(rule)

    if 'count' in response:
        for security_group in response['securitygroup']:
            if 'securityGroupId' in rule and security_group['id'] == rule[
                    'securityGroupId']:
                return security_group
            elif 'securityGroupName' in rule and security_group['name'] == rule[
                    'securityGroupName']:
                return security_group

    errors.invalid_security_group()


def _describe_security_groups_request(args=None):
    if args is None:
        args = {}

    args['command'] = 'listSecurityGroups'

    response = requester.make_request(args)
    response = response['listsecuritygroupsresponse']

    return response


def _parse_security_group_request(args=None):
    if args is None:
        args = {}

    helpers.require_atleast_one_parameter(['GroupName', 'GroupId'])

    if helpers.contains_parameter('GroupName'):
        args['securityGroupName'] = helpers.get('GroupName')
    elif helpers.contains_parameter('GroupId'):
        args['securityGroupId'] = helpers.get('GroupId')

    if helpers.contains_key_with_keyword('IpPermissions'):
        raise Ec2stackError(
            '400',
            'InvalidParameterCombination',
            'The parameter \'ipPermissions\' may not'
            'be used in combination with \'ipProtocol\''
        )
    else:
        helpers.require_parameters(['IpProtocol'])

        args['protocol'] = helpers.get('IpProtocol')

        helpers.require_parameters(['FromPort', 'ToPort', 'CidrIp'])

        if args['protocol'] in ['icmp']:
            args['icmptype'] = helpers.get('FromPort')
            args['icmpcode'] = helpers.get('ToPort')
        else:
            args['startport'] = helpers.get('FromPort')
            args['endport'] = helpers.get('ToPort')

        if helpers.get('CidrIp') is None:
            args['cidrlist'] = '0.0.0.0/0'
        else:
            args['cidrlist'] = helpers.get('CidrIp')

        return args
