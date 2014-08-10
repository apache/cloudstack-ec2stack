#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint

from ec2stack.helpers import get, error_response, \
    successful_response, require_parameters
from ec2stack.core import Ec2stackError
from ec2stack.services import USERS
from ec2stack.providers.cloudstack import images, instances, keypairs, \
    passwords, security_groups, zones, volumes, tags, vpcs, snapshots


DEFAULT = Blueprint('default', __name__)


@DEFAULT.route('/', methods=['POST'])
def index():
    """
    URL entry point. Parses the Action parameter and executes the associated
    functions to generate a response.

    @return: Response.
    """
    try:
        response_data = _get_action(get('Action'))()
        return successful_response(**response_data)
    except Ec2stackError as err:
        return error_response(err.code, err.error, err.message)


def _get_action(action):
    """
    Finds the associated function for each action.

    @param action: Action to be looked up.
    @return: Function associated with specified action.
    @raise Ec2stackError: Action is not found.
    """
    actions = {
        'AttachVolume': volumes.attach_volume,
        'AuthorizeSecurityGroupEgress':
        security_groups.authenticate_security_group_egress,
        'AuthorizeSecurityGroupIngress':
        security_groups.authenticate_security_group_ingress,
        'CreateKeyPair': keypairs.create_keypair,
        'CreateSecurityGroup': security_groups.create_security_group,
        'CreateSnapshot': snapshots.create_snapshot,
        'CreateTags': tags.create_tags,
        'CreateVolume': volumes.create_volume,
        'CreateVpc': vpcs.create_vpc,
        'DeleteKeyPair': keypairs.delete_keypair,
        'DeleteSecurityGroup': security_groups.delete_security_group,
        'DeleteSnapshot': snapshots.delete_snapshot,
        'DeleteTags': tags.delete_tags,
        'DeleteVolume': volumes.delete_volume,
        'DeleteVpc': vpcs.delete_vpc,
        'DescribeAvailabilityZones': zones.describe_zones,
        'DescribeImageAttribute': images.describe_image_attribute,
        'DescribeImages': images.describe_images,
        'DescribeInstanceAttribute': instances.describe_instance_attribute,
        'DescribeInstances': instances.describe_instances,
        'DescribeKeyPairs': keypairs.describe_keypairs,
        'DescribeSecurityGroups': security_groups.describe_security_groups,
        'DescribeSnapshots': snapshots.describe_snapshots,
        'DescribeTags': tags.describe_tags,
        'DescribeVolumes': volumes.describe_volumes,
        'DescribeVpcs': vpcs.describe_vpcs,
        'DetachVolume': volumes.detach_volume,
        'GetPasswordData': passwords.get_password_data,
        'ImportKeyPair': keypairs.import_keypair,
        'RebootInstances': instances.reboot_instance,
        'RegisterSecretKey': register_secret_key,
        'RemoveSecretKey': remove_secret_key,
        'RevokeSecurityGroupEgress':
        security_groups.revoke_security_group_egress,
        'RevokeSecurityGroupIngress':
        security_groups.revoke_security_group_ingress,
        'RunInstances': instances.run_instance,
        'StartInstances': instances.start_instance,
        'StopInstances': instances.stop_instance,
        'TerminateInstances': instances.terminate_instance,
    }

    if action in actions:
        return actions[action]
    else:
        raise Ec2stackError(
            '400',
            'InvalidAction',
            'The action %s is not valid for this web service' % action
        )


def register_secret_key():
    """
    Register a user's API key and secret key.

    @return: Response.
    @raise Ec2stackError: API key already registered.
    """
    require_parameters({'AWSAccessKeyId', 'AWSSecretKey'})
    found_user = USERS.get(get('AWSAccessKeyId'))
    if found_user is None:
        USERS.create(
            apikey=get('AWSAccessKeyId'),
            secretkey=get('AWSSecretKey')
        )
        return {
            'template_name_or_list': 'secretkey.xml',
            'response_type': 'RegisterSecretKeyResponse',
            'AWSAccessKeyId': get('AWSAccessKeyId'),
            'AWSSecretKey': get('AWSSecretKey'),
            'Message': 'Successfully Registered!'
        }
    else:
        raise Ec2stackError(
            '400',
            'DuplicateUser',
            'The given AWSAccessKeyId is already registered'
        )


def remove_secret_key():
    """
    Remove a user's API key and secret key

    @return: Response.
    @raise Ec2stackError: API key doesn't exist.
    """
    require_parameters({'AWSAccessKeyId', 'AWSSecretKey'})
    accesskey = get('AWSAccessKeyId')
    secretkey = get('AWSSecretKey')

    found_user = USERS.get(accesskey)
    if found_user is not None and found_user.secretkey == secretkey:
        USERS.delete(found_user)
        return {
            'template_name_or_list': 'secretkey.xml',
            'response_type': 'RemoveSecretKeyResponse',
            'AWSAccessKeyId': get('AWSAccessKeyId'),
            'AWSSecretKey': get('AWSSecretKey'),
            'Message': 'Successfully removed!'
        }
    else:
        raise Ec2stackError(
            '400',
            'NoSuchUser',
            'The no matching AWSAccessKeyId and AWSSecretKey was not found'
        )


@DEFAULT.app_errorhandler(404)
def not_found(err):
    """
    Generates a 404 not found page.

    @param err: Error information.
    @return: Response.
    """
    return error_response('404', 'NotFound', 'Page not found')


@DEFAULT.app_errorhandler(400)
def bad_request(err):
    """
    Generates a 400 bad request page.

    @param err: Error information.
    @return: Response.
    """
    return error_response('400', 'BadRequest', 'Bad Request')
