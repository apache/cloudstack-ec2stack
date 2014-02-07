#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, Response, request

from ..helpers import get, authentication_required, error_response
from ..core import Ec2stackError


DEFAULT = Blueprint('default', __name__)


@DEFAULT.route('/', methods=['POST'])
@authentication_required
def index():
    print 'hello'
    try:
        print _get_action(get('Action', request.form))()
        return Response('EC2STACK', status=200, mimetype='text/html')
    except Ec2stackError as err:
        return error_response(err.error, err.message)


def _get_action(action):
    actions = {
        'HelloWorld': hello_world,
    }

    if action in actions:
        return actions[action]
    else:
        raise Ec2stackError(
            'InvalidAction',
            'The action %s is not valid for this web service' % (action)
        )


def hello_world():
    return 'Hello World'


@DEFAULT.app_errorhandler(404)
def not_found(err):
    return Response('Not Found', status=404, mimetype='text/html')


@DEFAULT.app_errorhandler(400)
def bad_request(err):
    return Response('Bad Request', status=404, mimetype='text/html')
