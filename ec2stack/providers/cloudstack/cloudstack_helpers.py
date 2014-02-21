#!/usr/bin/env python
# encoding: utf-8

from ec2stack.helpers import *
from ec2stack.providers.cloudstack import translator


def describe_item_by_id(item_id, request_function):
    args = {
        'id': item_id
    }

    response = request_function(args)

    if 'errortext' in response:
        raise Ec2stackError(
            '400',
            'InvalidItemId.Malformed',
            'The specified Item ID is not valid'
        )

    return response


def get_items_from_response(response, item_type,
                            cloudstack_item_attributes_to_aws):
    items = []

    if response:
        for cloudstack_item in response[item_type]:
            items.append(
                translator.cloudstack_item_to_aws(
                    cloudstack_item,
                    cloudstack_item_attributes_to_aws
                )
            )

    return items
