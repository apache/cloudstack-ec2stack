#!/usr/bin/env python
# encoding: utf-8

from ec2stack import helpers, errors
from ec2stack.providers import cloudstack


@helpers.authentication_required
def describe_images():
    args = {'templatefilter': 'executable', 'command': 'listTemplates'}
    response = cloudstack.describe_item(
        args, 'template', errors.invalid_image_id, 'ImageId'
    )

    return _describe_images_response(
        response
    )


def _describe_images_response(response):
    return {
        'template_name_or_list': 'images.xml',
        'response_type': 'DescribeImagesResponse',
        'response': response
    }


@helpers.authentication_required
def describe_image_attribute():
    image_id = helpers.get('ImageId')
    attribute = helpers.get('Attribute')

    supported_attribute_map = {
        'description': 'displaytext'
    }

    if attribute not in supported_attribute_map.iterkeys():
        errors.invalid_paramater_value(
            'The specified attribute is not valid, please specify a valid ' +
            'image attribute.'
        )

    response = describe_image_by_id(image_id)
    return _describe_image_attribute_response(
        response, attribute, supported_attribute_map)


def _describe_image_attribute_response(response, attribute, attr_map):
    return {
        'template_name_or_list': 'image_attribute.xml',
        'response_type': 'DescribeImageAttributeResponse',
        'id': response['id'],
        'attribute': attribute,
        'value': response[attr_map[attribute]]
    }


def describe_image_by_id(image_id):
    args = {
        'id': image_id,
        'templatefilter': 'executable',
        'command': 'listTemplates'}
    response = cloudstack.describe_item_request(
        args, 'template', errors.invalid_image_id
    )
    return response
