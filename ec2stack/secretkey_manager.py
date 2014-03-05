#!/usr/bin/env python
# encoding: utf-8

import argparse
import requests

from xml.dom.minidom import parseString as xmlparse


def _generate_args(description):
    parser = argparse.ArgumentParser(
        description=description
    )

    parser.add_argument(
        'ec2stack_server_address',
        help='The address of the ec2stack server http://localhost:5000'
    )

    parser.add_argument(
        'AWSAccessKeyId',
        help='Your Cloudstack API Key'
    )

    parser.add_argument(
        'AWSSecretKey',
        help='Your Cloudstack Secret Key'
    )

    args = parser.parse_args()

    return vars(args)


def register():
    args = _generate_args(
        'Command line utility for registering a secret key with ec2stack'
    )
    args['Action'] = 'RegisterSecretKey'
    _execute_request(args)


def remove():
    args = _generate_args(
        'Command line utility for removing a secret key from ec2stack'
    )
    args['Action'] = 'RemoveSecretKey'
    _execute_request(args)


def _execute_request(args):
    host = args.pop('ec2stack_server_address')
    response = requests.post(host, args)
    response = xmlparse(response.text)
    message = response.getElementsByTagName('Message')[0].firstChild.nodeValue
    print message
