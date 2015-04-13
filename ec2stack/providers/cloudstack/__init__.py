#!/usr/bin/env python
# encoding: utf-8
#
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#  
#    http://www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.
#

"""This module contains helper functions used across the package namespace.
"""

from ec2stack import helpers
from ec2stack.providers.cloudstack import requester


def describe_item(args, keyname, not_found, prefix):
    """
    Describe a specific item or all items.

    @param args: Arguments involved in the request.
    @param keyname: Keyname of the Cloudstack response.
    @param not_found: Function to if the item is not found.
    @param prefix: Parameter prefix.
    @return: Response.
    """
    if helpers.contains_parameter_with_keyword(prefix):
        response = _describe_specific_item(args, keyname, not_found, prefix)
    else:
        response = describe_items_request(args, {})

    return response


def _describe_specific_item(args, keyname, not_found, prefix):
    """
    Describe a specific item based on args['id'] or args['name'].

    @param args: Arguments involved in the request.
    @param keyname: Keyname of the Cloudstack response.
    @param not_found: Function to call if the item is not found.
    @param prefix: Parameter prefix.
    @return: Response.
    """
    keys = helpers.get_request_parameter_keys(prefix)

    response = {keyname: []}

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
    """
    Executes the request and searches the Cloudstack response for the item.

    @param args: Arguments involved in the request.
    @param keyname: Keyname of the Cloudstack response.
    @param not_found: Function to call if the item is not found.
    @return: Response.
    """
    request = describe_items_request(args, not_found)
    request = request[keyname]

    for item in request:
        if 'id' in args and args['id'].lower() == item['id'].lower():
            return item
        elif 'name' in args and args['name'].lower() == item['name'].lower():
            return item

    return not_found()


def describe_items_request(args, not_found):
    """
    Executes the request.

    @param args: Request payload.
    @param not_found: Function to call on empty response from Cloudstack.
    @return: Response.
    """
    args['listAll'] = 'true'
    response = requester.make_request(args)
    response = response[response.keys()[0]]

    if 'count' in response:
        return response
    elif callable(not_found):
        return not_found()
    else:
        return not_found
