#!/usr/bin/env python
# encoding: utf-8

from ec2stack.helpers import authentication_required


@authentication_required
def describe():
    items = [
        {
            'id': '1',
            'name': 'dummy-image-1',
            'state': 'available'
        },
        {
            'id': '2',
            'name': 'dummy-image-2',
            'state': 'available'
        }
    ]

    return {
        'template_name_or_list': 'describe_items_response.xml',
        'response_type': 'DescribeImagesResponse',
        'items': items,
        'item_to_describe': 'image'
    }
