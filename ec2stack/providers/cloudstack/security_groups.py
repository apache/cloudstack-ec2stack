#!/usr/bin/env python
# encoding: utf-8

"""This module contains functions for handling requests in relation to security
groups
"""

from ec2stack import helpers, errors
from ec2stack.providers import cloudstack
from ec2stack.core import Ec2stackError
from ec2stack.providers.cloudstack import requester


@helpers.authentication_required
def authenticate_security_group_egress():
    """
    Add egress rules to a security group.

    @return: Response.
    """
    rule_type = 'egress'
    response = _authenticate_security_group_request(rule_type)
    return _authenticate_security_group_response(response, rule_type)


def _authenticate_security_group_request(rule_type):
    """
    Request to add an egress rule to a security group.

    @param rule_type: The type of rule to add.
    @return: Response.
    """
    args = _parse_security_group_request()

    if rule_type == 'egress':
        args['command'] = 'authorizeSecurityGroupEgress'
    elif rule_type == 'ingress':
        args['command'] = 'authorizeSecurityGroupIngress'

    response = requester.make_request_async(args)

    return response


def _authenticate_security_group_response(response, rule_type):
    """
    Generate a response for authenticate security group request.

    @param response: Cloudstack response.
    @param rule_type: The type of rule to add.
    @raise Ec2stackError: If authorize security group fails.
    @return: Response
    """
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
        else:
            errors.invalid_request(response['errortext'])
    else:
        if rule_type == 'ingress':
            rule_type = 'AuthorizeSecurityGroupIngressResponse'
        elif rule_type == 'egress':
            rule_type = 'AuthorizeSecurityGroupEgressResponse'

        return {
            'template_name_or_list': 'status.xml',
            'response_type': rule_type,
            'return': 'true'
        }


@helpers.authentication_required
def create_security_group():
    """
    Create a security group.

    @return: Response.
    """
    helpers.require_parameters(['GroupName', 'GroupDescription'])
    response = _create_security_group_request()
    return _create_security_group_response(response)


def _create_security_group_request():
    """
    Request to create a security group.

    @return: response.
    """
    args = {'command': 'createSecurityGroup', 'name': helpers.get('GroupName'),
            'description': helpers.get('GroupDescription')}

    response = requester.make_request(args)

    response = response['createsecuritygroupresponse']

    return response


def _create_security_group_response(response):
    """
    Generate a response for create security group request.
    @param response: Cloudstack response.
    @return: Response.
    """
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
    """
    Deletes a specified security group.

    @return: Response.
    """
    _delete_security_group_request()
    return _delete_security_group_response()


def _delete_security_group_request():
    """
    Request to delete a security group.

    @return: Response.
    """
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
    """
    Generate a response for delete security group request.

    @return: response
    """
    return {
        'template_name_or_list': 'status.xml',
        'response_type': 'DeleteSecurityGroupResponse',
        'return': 'true'
    }


@helpers.authentication_required
def describe_security_groups():
    """
    Describe one or more security groups.

    @return: Response
    """
    args = {'command': 'listSecurityGroups'}

    response = cloudstack.describe_item(
        args, 'securitygroup', errors.invalid_security_group, 'Group'
    )

    return _describe_security_groups_response(
        response
    )


def _describe_security_groups_response(response):
    """
    Generates a response for describe security group request.

    @param response: Cloudstack response.
    @return: Response.
    """
    return {
        'template_name_or_list': 'securitygroups.xml',
        'response_type': 'DescribeSecurityGroupsResponse',
        'response': response
    }


@helpers.authentication_required
def authenticate_security_group_ingress():
    """
    Add one or more ingress rules to a security group.

    @return: Response.
    """
    rule_type = 'ingress'
    response = _authenticate_security_group_request(rule_type)
    return _authenticate_security_group_response(response, rule_type)


@helpers.authentication_required
def revoke_security_group_ingress():
    """
    Removes one or more ingress rules from a security group.

    @return: Response.
    """
    rule_type = 'ingress'
    _revoke_security_group_request(rule_type)
    return _revoke_security_group_response(rule_type)


@helpers.authentication_required
def revoke_security_group_egress():
    """
    Removes one or more egress rules from a security group.

    @return: Response.
    """
    rule_type = 'egress'
    _revoke_security_group_request(rule_type)
    return _revoke_security_group_response(rule_type)


def _revoke_security_group_request(rule_type):
    """
    Request to remove rule from security group

    @param rule_type: The type of rule to remove.
    @return: Response.
    """
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


def _revoke_security_group_response(rule_type):
    """
    Generate a response for revoke security group requests.

    @param rule_type: The type of rule
    @return: Response.
    """
    if rule_type == 'ingress':
        rule_type = 'RevokeSecurityGroupIngressResponse'
    elif rule_type == 'egress':
        rule_type = 'RevokeSecurityGroupEgressResponse'
    return {
        'template_name_or_list': 'status.xml',
        'response_type': rule_type,
        'return': 'true'
    }


def _find_rule(rule, rule_type):
    """
    Searches a Cloudstack response for a rule and returns its Id.

    @param rule: Rule to be found.
    @param rule_type: Type of rule.
    @return: Id of the rule.
    """
    security_group = _get_security_group(rule)

    if rule_type in security_group:
        found_rules = security_group[rule_type]

        for found_rule in found_rules:
            if _compare_rules(rule, found_rule):
                return found_rule['ruleid']

    errors.invalid_permission()


def _compare_rules(left, right):
    """
    Compares two rules to see if they are the same.

    @param left: rule to be compared.
    @param right: rule to compare with.
    @return: Boolean
    """
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


def _get_security_group(args):
    """
    Get the security group with the specified name.

    @param args: Arguments to pass to request.
    @return: Response.
    """
    args['command'] = 'listSecurityGroups'
    response = cloudstack.describe_item_request(
        args, 'securitygroup', errors.invalid_security_group
    )

    return response


def _parse_security_group_request(args=None):
    """
    Parse the request parameters into a Cloudstack request payload.

    @param args: Arguments to include in the request.
    @return: Request payload.
    """
    if args is None:
        args = {}

    helpers.require_atleast_one_parameter(['GroupName', 'GroupId'])

    if helpers.contains_parameter('GroupName'):
        args['securityGroupName'] = helpers.get('GroupName')
        args['name'] = helpers.get('GroupName')
    elif helpers.contains_parameter('GroupId'):
        args['securityGroupId'] = helpers.get('GroupId')
        args['id'] = helpers.get('GroupId')

    helpers.require_parameters(['IpProtocol'])

    args['protocol'] = helpers.get('IpProtocol')

    helpers.require_parameters(['FromPort', 'ToPort'])

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
