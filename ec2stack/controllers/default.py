#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, request

from ec2stack.helpers import get, error_response, \
    successful_response, require_parameters
from ec2stack.core import Ec2stackError
from ec2stack.services import USERS
from ec2stack.providers.cloudstack import images, instances, keypair, \
    password, security_group, volume


DEFAULT = Blueprint('default', __name__)


@DEFAULT.route('/', methods=['POST'])
def index():
    try:
        response_data = _get_action(get('Action', request.form))()
        return successful_response(**response_data)
    except Ec2stackError as err:
        return error_response(err.code, err.error, err.message)


def _get_action(action):
    actions = {
        'CreateKeyPair': keypair.create_keypair,
        'CreateSecurityGroup': security_group.create_security_group,
        'CreateVolume': volume.create_volume,
        'DeleteKeyPair': keypair.delete_keypair,
        'DeleteSecurityGroup': security_group.delete_security_group,
        'DeleteVolume': volume.delete_volume,
        'DescribeImageAttribute': images.describe_image_attribute,
        'DescribeImages': images.describe_images,
        'DescribeInstanceAttribute': instances.describe_instance_attribute,
        'DescribeInstances': instances.describe_instances,
        'DescribeVolumes': volume.describe_volumes,
        'GetPasswordData': password.get_password_data,
        'ImportKeyPair': keypair.import_keypair,
        'RegisterSecretKey': registerSecretKey,
        'RemoveSecretKey': removeSecretKey
    }

    if action in actions:
        return actions[action]
    else:
        raise Ec2stackError(
            '400',
            'InvalidAction',
            'The action %s is not valid for this web service' % (action)
        )


def registerSecretKey():
    require_parameters({'AWSAccessKeyId', 'AWSSecretKey'})
    found_user = USERS.get(get('AWSAccessKeyId', request.form))
    if found_user is None:
        USERS.create(
            apikey=get('AWSAccessKeyId', request.form),
            secretkey=get('AWSSecretKey', request.form)
        )
        return {
            'template_name_or_list': 'secretkey.xml',
            'response_type': 'RegisterSecretKeyResponse',
            'apikey': get('AWSAccessKeyId', request.form),
            'secretkey': get('AWSSecretKey', request.form),
        }
    else:
        raise Ec2stackError(
            '400',
            'DuplicateUser',
            'The given AWSAccessKeyId is already registered'
        )


def removeSecretKey():
    require_parameters({'AWSAccessKeyId', 'AWSSecretKey'})
    accesskey = get('AWSAccessKeyId', request.form)
    secretkey = get('AWSSecretKey', request.form)

    found_user = USERS.get(accesskey)
    if found_user is not None and found_user.secretkey == secretkey:
        USERS.delete(found_user)
        return {
            'template_name_or_list': 'secretkey.xml',
            'response_type': 'RemoveSecretKeyResponse',
            'apikey': get('AWSAccessKeyId', request.form),
            'secretkey': get('AWSSecretKey', request.form),
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
