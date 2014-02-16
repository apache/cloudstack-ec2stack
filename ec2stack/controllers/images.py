#!/usr/bin/env python
# encoding: utf-8

from ec2stack.helpers import authentication_required
from ec2stack.controllers.cloudstack import requester


@authentication_required
def describe_images():
    images = _describe_all_images()
    return _describe_images_format_response(images)


def _describe_all_images():
    response = _describe_templates_request()
    images = _get_images_from_response(response)
    return images


def _describe_templates_request(args=None):
    if not args:
        args = {}

    if 'templatefilter' not in args:
        args['templatefilter'] = 'executable'

    args['command'] = 'listTemplates'

    cloudstack_response = requester.make_request(args)

    return cloudstack_response


def _get_images_from_response(response):
    images = []
    response = response['listtemplatesresponse']
    if response:
        for template in response['template']:
            images.append(
                _cloudstack_template_to_aws_image(template)
            )

    return images


def _cloudstack_template_to_aws_image(cloudstack_response):
    translate_image_status = {
        'True': 'Available',
        'False': 'Unavailable'
    }

    image = {
        'id': cloudstack_response['id'],
        'name': cloudstack_response['name'],
        'state': translate_image_status[str(cloudstack_response['isready'])]
    }

    return image


def _describe_images_format_response(images):
    response = {
        'template_name_or_list': 'describe_images.xml',
        'response_type': 'DescribeImagesResponse',
        'images': images,
        'item_to_describe': 'image'
    }

    return response
