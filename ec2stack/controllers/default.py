#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, Response, request

from ..helpers import get, error_response, successful_response
from ..core import Ec2stackError
from . import images, instances


DEFAULT = Blueprint('default', __name__)


@DEFAULT.route('/', methods=['POST'])
def index():
    try:
        response_content = _get_action(get('Action', request.form))()
        return successful_response(response_content)
    except Ec2stackError as err:
        return error_response(err.error, err.message)


def _get_action(action):
    actions = {
        'DescribeImages': images.describe,
        'DescribeInstances': instances.describe
    }

    if action in actions:
        return actions[action]
    else:
        raise Ec2stackError(
            'InvalidAction',
            'The action %s is not valid for this web service' % (action)
        )


@DEFAULT.app_errorhandler(404)
def not_found(err):
    return Response('Not Found', status=404, mimetype='text/html')


@DEFAULT.app_errorhandler(400)
def bad_request(err):
    return Response('Bad Request', status=404, mimetype='text/html')
