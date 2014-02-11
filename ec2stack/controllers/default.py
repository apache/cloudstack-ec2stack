#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, Response, request

from ..helpers import get, error_response, successful_response,\
    require_parameters
from ..core import Ec2stackError
from ..services import USERS
from . import images, instances


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
        'DescribeImages': images.describe,
        'DescribeInstances': instances.describe,
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
            'response_type': 'RemoveSecretKeyResponse',
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
    found_user = USERS.get(get('AWSAccessKeyId', request.form))
    if found_user is not None:
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
            'The given AWSAccessKeyId was not found'
        )


@DEFAULT.app_errorhandler(404)
def not_found(err):
    return Response('Not Found', status=404, mimetype='text/html')


@DEFAULT.app_errorhandler(400)
def bad_request(err):
    return Response('Bad Request', status=404, mimetype='text/html')
