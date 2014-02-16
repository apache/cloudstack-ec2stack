#!/usr/bin/env python
# encoding: utf-8

from flask import request

from ec2stack import helpers
from ec2stack.helpers import authentication_required
from ec2stack.core import Ec2stackError
from ec2stack.providers.cloudstack import requester


@authentication_required
def create_keypair():
    helpers.require_parameters(['KeyName'])
    response = _create_keypair_request()
    return _create_keypair_format_response(response)


def _create_keypair_request():
    args = {}
    args['command'] = 'createSSHKeyPair'
    args['name'] = helpers.get('KeyName', request.form)

    response = requester.make_request(args)

    response = response['createsshkeypairresponse']

    return response


def _create_keypair_format_response(response):
    if 'errortext' in response:
        keyname = helpers.get('KeyName', request.form)
        raise Ec2stackError(
            '400',
            'InvalidKeyPair.Duplicate',
            'The keypair \'%s\' already exists.' % keyname
        )
    else:
        response = response['keypair']
        return {
            'template_name_or_list': 'keypair.xml',
            'response_type': 'CreateKeyPairResponse',
            'key_name': response['name'],
            'key_fingerprint': response['fingerprint'],
            'key_material': response['privatekey']
        }
