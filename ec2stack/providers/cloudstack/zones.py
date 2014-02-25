#!/usr/bin/env python
# encoding: utf-8

from ec2stack import errors
from ec2stack.providers.cloudstack import requester


def get_zones_id_by_name(name):
    args = {}
    args['name'] = name
    response = _describe_zones_request(args)

    if response:
        response = response['zone'][0]
    else:
        errors.invalid_zone_id()

    return response['id']


def _describe_zones_request(args=None):
    if args is None:
        args = {}

    args['command'] = 'listZones'

    response = requester.make_request(args)
    response = response['listzonesresponse']

    return response