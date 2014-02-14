#!/usr/bin/env python
# encoding: utf-8

from ec2stack.helpers import authentication_required


def _get_templates(args=None):
    if not args:
        args = {}

    command = 'listTemplates'

    '''Get genuine response here using listTemplates
       None response for now'''
    cloudstack_response = {}

    return cloudstack_response


def _cloudstack_template_to_aws(cloudstack_response):
    translate_image_status = {
        'True': 'Available',
        'False': 'Unavailable'
    }

    template = [
        {
            'id': '1',
            'name': 'dummy-image-1',
            'state': 'available'
        }
    ]

    return template


@authentication_required
def describe_images():

    templates = {}

    items = _cloudstack_template_to_aws(templates)
    print('---------------\n')

    return {
        'template_name_or_list': 'describe_items_response.xml',
        'response_type': 'DescribeImagesResponse',
        'items': items,
        'item_to_describe': 'image'
    }
