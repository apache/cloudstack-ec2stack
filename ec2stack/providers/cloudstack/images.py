#!/usr/bin/env python
# encoding: utf-8

from ec2stack import helpers
from ec2stack.providers.cloudstack import requester


@helpers.authentication_required
def describe_images():
    if helpers.contains_parameter('ImageId.1'):
        images = _describe_specific_images()
    else:
        images = _describe_all_images()

    return _describe_images_response(images)


def _describe_all_images():
    response = _describe_templates_request()
    return response


def _describe_specific_images():
    image_ids_keys = helpers.get_request_parameter_keys('ImageId.')

    response = {}
    response['template'] = []

    for image_id_key in image_ids_keys:
        image_id = helpers.get(image_id_key)
        image_response = describe_image_by_id(image_id)
        response['template'].append(image_response)

    return response


def describe_image_by_id(image_id):
    args = {}
    args['id'] = image_id
    response = _describe_templates_request(args)
    response = response['template'][0]

    return response


def _describe_templates_request(args=None):
    if not args:
        args = {}

    if 'templatefilter' not in args:
        args['templatefilter'] = 'executable'

    args['command'] = 'listTemplates'

    cloudstack_response = requester.make_request(args)
    cloudstack_response = cloudstack_response['listtemplatesresponse']

    return cloudstack_response


def _describe_images_response(response):
    return {
        'template_name_or_list': 'images.xml',
        'response_type': 'DescribeImagesResponse',
        'response': response
    }


@helpers.authentication_required
def describe_image_attribute():
    image_id = helpers.get('ImageId')

    response = describe_image_by_id(image_id)

    return _describe_image_attribute_response(response)


def _describe_image_attribute_response(response):
    attribute = helpers.get('Attribute')

    return {
        'template_name_or_list': 'image_attribute.xml',
        'response_type': 'DescribeImageAttributeResponse',
        'attribute': attribute,
        'id': response['id'],
        'value': response[attribute]
    }
