#!/usr/bin/env python
# encoding: utf-8

from flask import render_template


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

    return render_template(
        'describe_items_response.xml',
        response_type='DescribeImagesResponse',
        items=items,
        request_id='dummy_request_id',
        item_to_describe='image'
    )
