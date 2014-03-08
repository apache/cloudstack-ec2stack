#!/usr/bin/env python
# encoding: utf-8

from base64 import b64decode

from ec2stack.providers import cloudstack
from ec2stack import helpers
from ec2stack.providers.cloudstack import requester
from ec2stack import errors


@helpers.authentication_required
def create_keypair():
    """


    @return:
    """
    helpers.require_parameters(['KeyName'])
    response = _create_keypair_request()
    return _create_keypair_response(response)


def _create_keypair_request():
    """


    @return:
    """
    args = {'command': 'createSSHKeyPair', 'name': helpers.get('KeyName')}

    response = requester.make_request(args)

    response = response['createsshkeypairresponse']

    return response


def _create_keypair_response(response):
    """

    @param response:
    @return:
    """
    if 'errortext' in response:
        errors.duplicate_keypair_name()
    else:
        response = response['keypair']
        return {
            'template_name_or_list': 'create_keypair.xml',
            'response_type': 'CreateKeyPairResponse',
            'response': response
        }


@helpers.authentication_required
def delete_keypair():
    """


    @return:
    """
    helpers.require_parameters(['KeyName'])
    _delete_keypair_request()
    return _delete_keypair_response()


def _delete_keypair_request():
    """


    @return:
    """
    args = {'command': 'deleteSSHKeyPair', 'name': helpers.get('KeyName')}

    response = requester.make_request(args)

    return response


def _delete_keypair_response():
    """


    @return:
    """
    return {
        'template_name_or_list': 'status.xml',
        'response_type': 'DeleteKeyPairResponse',
        'return': 'true'
    }


@helpers.authentication_required
def describe_keypairs():
    """


    @return:
    """
    args = {'command': 'listSSHKeyPairs'}
    response = cloudstack.describe_item(
        args, 'sshkeypair', errors.invalid_keypair_name, 'KeyName'
    )

    return _describe_keypair_response(
        response
    )


def _describe_keypair_response(response):
    """

    @param response:
    @return:
    """
    return {
        'template_name_or_list': 'keypairs.xml',
        'response_type': 'DescribeKeyPairsResponse',
        'response': response
    }


@helpers.authentication_required
def import_keypair():
    """


    @return:
    """
    helpers.require_parameters(['KeyName', 'PublicKeyMaterial'])
    response = _import_keypair_request()
    return _import_keypair_response(response)


def _import_keypair_request():
    """


    @return:
    """
    args = {'command': 'registerSSHKeyPair', 'name': helpers.get('KeyName'),
            'publickey': b64decode(helpers.get('PublicKeyMaterial'))}

    response = requester.make_request(args)
    response = response['registersshkeypairresponse']

    return response


def _import_keypair_response(response):
    """

    @param response:
    @return:
    """
    if 'errortext' in response:
        errors.duplicate_keypair_name()
    else:
        response = response['keypair']
        return {
            'template_name_or_list': 'create_keypair.xml',
            'response_type': 'ImportKeyPairResponse',
            'response': response
        }
