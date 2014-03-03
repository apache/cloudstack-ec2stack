#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint

from ec2stack.helpers import get, error_response, \
    successful_response, require_parameters
from ec2stack.core import Ec2stackError
from ec2stack.services import USERS
from ec2stack.providers.cloudstack import images, instances, keypairs, \
    passwords, security_groups, zones, volumes


DEFAULT = Blueprint('default', __name__)


@DEFAULT.route('/', methods=['POST'])
def index():
    try:
        response_data = _get_action(get('Action'))()
        return successful_response(**response_data)
    except Ec2stackError as err:
        return error_response(err.code, err.error, err.message)


def _get_action(action):
    actions = {
        'AttachVolume': volumes.attach_volume,
        'AuthorizeSecurityGroupEgress':
        security_groups.authenticate_security_group_egress,
        'AuthorizeSecurityGroupIngress':
        security_groups.authenticate_security_group_ingress,
        'CreateKeyPair': keypairs.create_keypair,
        'CreateSecurityGroup': security_groups.create_security_group,
        'CreateVolume': volumes.create_volume,
        'DeleteKeyPair': keypairs.delete_keypair,
        'DeleteSecurityGroup': security_groups.delete_security_group,
        'DeleteVolume': volumes.delete_volume,
        'DescribeAvailabilityZones': zones.describe_zones,
        'DescribeImageAttribute': images.describe_image_attribute,
        'DescribeImages': images.describe_images,
        'DescribeInstanceAttribute': instances.describe_instance_attribute,
        'DescribeInstances': instances.describe_instances,
        'DescribeKeyPairs': keypairs.describe_keypairs,
        'DescribeSecurityGroups': security_groups.describe_security_groups,
        'DescribeVolumes': volumes.describe_volumes,
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
            'apikey': get('AWSAccessKeyId'),
            'secretkey': get('AWSSecretKey'),
        }
    else:
        raise Ec2stackError(
            '400',
            'DuplicateUser',
            'The given AWSAccessKeyId is already registered'
        )


def remove_secret_key():
    require_parameters({'AWSAccessKeyId', 'AWSSecretKey'})
    accesskey = get('AWSAccessKeyId')
    secretkey = get('AWSSecretKey')

    found_user = USERS.get(accesskey)
    if found_user is not None and found_user.secretkey == secretkey:
        USERS.delete(found_user)
        return {
            'template_name_or_list': 'secretkey.xml',
            'response_type': 'RemoveSecretKeyResponse',
            'apikey': get('AWSAccessKeyId'),
            'secretkey': get('AWSSecretKey'),
        }
    else:
        raise Ec2stackError(
            '400',
            'NoSuchUser',
            'The no matching AWSAccessKeyId and AWSSecretKey was not found'
        )


@DEFAULT.app_errorhandler(404)
def not_found(err):
    return error_response('404', 'NotFound', 'Page not found')


@DEFAULT.app_errorhandler(400)
def bad_request(err):
    return error_response('400', 'BadRequest', 'Bad Request')
