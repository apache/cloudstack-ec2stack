#!/usr/bin/env python
# encoding: utf-8

from ec2stack import helpers
from ec2stack.providers.cloudstack import requester


def describe_item(args, keyname, prefix):
    if helpers.contains_parameter_with_keyword(prefix):
        response = _describe_specific_item(args, keyname, prefix)
    else:
        response = _describe_items_request(args)

    return response


def _describe_specific_item(args, keyname, prefix):
    if args is None:
        args = {}

    keys = helpers.get_request_parameter_keys(prefix + '.')

    response = {}
    response[keyname] = []

    for key in keys:
        name = helpers.get(key)

        if 'Id' in key:
            args['id'] = name
        elif 'Name' in key:
            args['name'] = name

        request = _describe_item_request(args, keyname)
        response[keyname].append(request)

    return response


def _describe_item_request(args, keyname):
    request = _describe_items_request(args)
    request = request[keyname]

    for item in request:
        if 'id' in args and args['id'] == item['id']:
            return item
        elif 'name' in args and args['name'] == item['name']:
            return item

    # Todo throw exception here to handle not found case
    return None


def _describe_items_request(args):
    print "####################"
    print args
    response = requester.make_request(args)
    response = response[response.keys()[0]]

    return response
