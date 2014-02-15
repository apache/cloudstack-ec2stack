#!/usr/bin/env python
# encoding: utf-8

from ec2stack import helpers
from flask import request
from ec2stack.helpers import authentication_required
from ec2stack.controllers.cloudstack import requester


def _get_templates(args=None):
    if not args:
        args = {}

    if 'templatefilter' not in args:
        args['templatefilter'] = 'executable'

    args['command'] =  'listTemplates'
    args['apikey'] = helpers.get('AWSAccessKeyId', request.form)
    user = helpers.get_secretkey()
    
    cloudstack_response = requester.make_request(args, user)

    return cloudstack_response


def _cloudstack_template_to_aws(cloudstack_response):
    translate_image_status = {
        'True': 'Available',
        'False': 'Unavailable'
    }

    return {
        'id': cloudstack_response['id'],
        'name': cloudstack_response['name'],
        'state': translate_image_status[str(cloudstack_response['isready'])]
    }


@authentication_required
def describe_images():
    templates = _get_templates()
    items = []

    if templates['listtemplatesresponse']:
        for template in templates['listtemplatesresponse']['template']:
            items.append(
                _cloudstack_template_to_aws(template)
            )

    return {
        'template_name_or_list': 'describe_items_response.xml',
        'response_type': 'DescribeImagesResponse',
        'items': items,
        'item_to_describe': 'image'
    }
