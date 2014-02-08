#!/usr/bin/env python
# encoding: utf-8

from flask import render_template


def describe():
    images = [
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
        'images/describe_images.xml',
        images=images
    )
