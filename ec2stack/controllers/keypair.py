#!/usr/bin/env python
# encoding: utf-8

from ec2stack import helpers
from flask import request
from ec2stack.helpers import authentication_required
from ec2stack.controllers.cloudstack import requester

## TODO Add error handling, split up into functions.


@authentication_required
def create_keypair():
    args = {}
    args['command'] = 'createSSHKeyPair',
    args['name'] = helpers.get('KeyName', request.form)

    cloudstack_response = requester.make_request(args)

    cloudstack_response = cloudstack_response['createsshkeypairresponse'][
        'keypair']

    return {
        'template_name_or_list': 'keypair.xml',
        'response_type': 'CreateKeyPairResponse',
        'key_name': cloudstack_response['name'],
        'key_fingerprint': cloudstack_response['fingerprint'],
        'key_material': cloudstack_response['privatekey'].strip()
    }
