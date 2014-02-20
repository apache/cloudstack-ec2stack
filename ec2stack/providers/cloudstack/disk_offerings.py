#!/usr/bin/env python
# encoding: utf-8

from flask import request

from ec2stack import helpers
from ec2stack.helpers import authentication_required
from ec2stack.providers.cloudstack import requester


def get_disk_offerings_id_by_name(name):
    args = {}
    args['name'] = name
    response = _describe_disk_offerings_request(args)
    response = response['diskoffering'][0]
    return response['id']


def _describe_disk_offerings_request(args=None):
    args['command'] = 'listDiskOfferings'

    response = requester.make_request(args)
    response = response['listdiskofferingsresponse']

    return response