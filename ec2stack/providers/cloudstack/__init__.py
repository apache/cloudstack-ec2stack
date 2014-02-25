#!/usr/bin/env python
# encoding: utf-8

from ec2stack import helpers
from ec2stack.providers.cloudstack import requester


def describe_item(args, keyname, not_found, prefix):
    if helpers.contains_parameter_with_keyword(prefix):
        response = _describe_specific_item(args, keyname, not_found, prefix)
    else:
        response = _describe_items_request(args, not_found)

    return response


def _describe_specific_item(args, keyname, not_found, prefix):
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

        request = describe_item_request(args, keyname, not_found)
        response[keyname].append(request)

    return response


def describe_item_request(args, keyname, not_found):
    request = _describe_items_request(args, not_found)
    request = request[keyname]

    for item in request:
        if 'id' in args and args['id'] == item['id']:
            return item
        elif 'name' in args and args['name'] == item['name']:
            return item

    return not_found()


def _describe_items_request(args, not_found):
    response = requester.make_request(args)
    response = response[response.keys()[0]]

    if 'count' in response:
        return response
    else:
        return not_found()
