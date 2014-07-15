#!/usr/bin/env python
# encoding: utf-8

"""This module contains functions for handling requests in relation to keypairs.
"""

from base64 import b64decode

from ec2stack import errors
from ec2stack import helpers
from ec2stack.providers import cloudstack
from ec2stack.providers.cloudstack import requester


@helpers.authentication_required
def create_keypair():
    """
    Create a keypair.

    @return: Response.
    """
    helpers.require_parameters(['KeyName'])
    response = _create_keypair_request()
    return _create_keypair_response(response)


def _create_keypair_request():
    """
    Request to create a keypair.

    @return: Response.
    """
    args = {'command': 'createSSHKeyPair', 'name': helpers.get('KeyName')}

    response = requester.make_request(args)

    response = response['createsshkeypairresponse']

    return response


def _create_keypair_response(response):
    """
    Generates a response for create keypair request.

    @param response: Response from Cloudstack.
    @return: Response.
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
    Delete a keypair.

    @return: Response.
    """
    helpers.require_parameters(['KeyName'])
    _delete_keypair_request()
    return _delete_keypair_response()


def _delete_keypair_request():
    """
    Request to delete a keypair.

    @return: Response.
    """
    args = {'command': 'deleteSSHKeyPair', 'name': helpers.get('KeyName')}

    response = requester.make_request(args)

    return response


def _delete_keypair_response():
    """
    Generates a response for delete keypair request.

    @return: Response.
    """
    return {
        'template_name_or_list': 'status.xml',
        'response_type': 'DeleteKeyPairResponse',
        'return': 'true'
    }


@helpers.authentication_required
def describe_keypairs():
    """
    Describes a specific keypair or all keypairs.

    @return: Response.
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
    Generates a response for describe keypair request.

    @param response: Response from Cloudstack.
    @return: Response.
    """
    return {
        'template_name_or_list': 'keypairs.xml',
        'response_type': 'DescribeKeyPairsResponse',
        'response': response
    }


@helpers.authentication_required
def import_keypair():
    """
    Imports a keypair.

    @return: Response.
    """
    helpers.require_parameters(['KeyName', 'PublicKeyMaterial'])
    response = _import_keypair_request()
    return _import_keypair_response(response)


def _import_keypair_request():
    """
    Request to import a keypair.

    @return: Response.
    """
    args = {'command': 'registerSSHKeyPair', 'name': helpers.get('KeyName'),
            'publickey': b64decode(helpers.get('PublicKeyMaterial'))}

    response = requester.make_request(args)
    response = response['registersshkeypairresponse']

    return response


def _import_keypair_response(response):
    """
    Generates a response for import keypair request.

    @param response: Response from Cloudstack.
    @return: Response.
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
