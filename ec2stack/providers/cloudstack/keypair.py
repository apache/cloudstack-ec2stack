#!/usr/bin/env python
# encoding: utf-8

from base64 import b64decode

from flask import request

from ec2stack import helpers
from ec2stack.core import Ec2stackError
from ec2stack.providers.cloudstack import requester


@helpers.authentication_required
def create_keypair():
    helpers.require_parameters(['KeyName'])
    response = _create_keypair_request()
    return _create_keypair_response(response)


def _create_keypair_request():
    args = {}
    args['command'] = 'createSSHKeyPair'
    args['name'] = helpers.get('KeyName', request.form)

    response = requester.make_request(args)

    response = response['createsshkeypairresponse']

    return response


def _create_keypair_response(response):
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
            'template_name_or_list': 'create_keypair.xml',
            'response_type': 'CreateKeyPairResponse',
            'response': response
        }


@helpers.authentication_required
def delete_keypair():
    helpers.require_parameters(['KeyName'])
    response = _delete_keypair_request()
    return _delete_keypair_response(response)


def _delete_keypair_request():
    args = {}
    args['command'] = 'deleteSSHKeyPair'
    args['name'] = helpers.get('KeyName', request.form)

    response = requester.make_request(args)

    return response


def _delete_keypair_response(response):
    return {
        'template_name_or_list': 'status.xml',
        'response_type': 'DeleteKeyPairResponse',
        'return': 'true'
    }


@helpers.authentication_required
def import_keypair():
    helpers.require_parameters(['KeyName', 'PublicKeyMaterial'])
    response = _import_keypair_request()
    return _import_keypair_response(response)


def _import_keypair_request():
    args = {}
    args['command'] = 'registerSSHKeyPair'
    args['name'] = helpers.get('KeyName', request.form)
    args['publickey'] = b64decode(
        helpers.get('PublicKeyMaterial', request.form))

    response = requester.make_request(args)
    response = response['registersshkeypairresponse']

    return response


def _import_keypair_response(response):
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
            'template_name_or_list': 'create_keypair.xml',
            'response_type': 'ImportKeyPairResponse',
            'response': response
        }
