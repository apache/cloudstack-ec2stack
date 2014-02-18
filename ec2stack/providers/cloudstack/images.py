#!/usr/bin/env python
# encoding: utf-8

from ec2stack.helpers import *
from ec2stack.providers.cloudstack import requester


cloudstack_attributes_to_aws = {
    'id': 'id',
    'name': 'name',
    'isready': 'state',
    'hypervisor': 'hypervisor',
    'displaytext': 'description'
}


@authentication_required
def describe_images():
    if contains_parameter('ImageId.1'):
        images = _describe_specific_images()
    else:
        images = _describe_all_images()

    return _create_describe_images_response(images)


def describe_image_attribute():
    require_parameters(['ImageId', 'Attribute'])
    image_id = get('ImageId', request.form)
    attribute = get('Attribute', request.form)

    response = _describe_image_by_id(image_id)
    image = _get_images_from_response(response, attribute)

    response = _create_describe_image_attribute_response(image, attribute)
    return response


def _describe_all_images():
    response = _describe_templates_request()
    images = _get_images_from_response(response)
    return images


def _describe_specific_images():
    root_image_id = 'ImageId.'
    current_image_num = 1
    current_image = root_image_id + str(current_image_num)
    images = []

    while contains_parameter(current_image):
        image_id = get(current_image, request.form)
        response = _describe_image_by_id(image_id)
        images = images + _get_images_from_response(response)
        current_image_num += 1
        current_image = root_image_id + str(current_image_num)

    return images


def _describe_image_by_id(image_id):
    args = {
        'id': image_id
    }

    return _describe_templates_request(args)


def _describe_templates_request(args=None):
    if not args:
        args = {}

    if 'templatefilter' not in args:
        args['templatefilter'] = 'executable'

    args['command'] = 'listTemplates'

    cloudstack_response = requester.make_request(args)

    return cloudstack_response


def _get_images_from_response(response, attribute=None):
    images = []
    response = response['listtemplatesresponse']
    if response:
        for template in response['template']:
            images.append(
                _cloudstack_template_to_aws_image(template, attribute)
            )

    return images


def _cloudstack_template_to_aws_image(response, attribute=None):
    image = {}
    if attribute is not None:
        if response[attribute] is not None:
            image[
                cloudstack_attributes_to_aws[attribute]
            ] = response[attribute]
    else:
        for cloudstack_attr, aws_attr in cloudstack_attributes_to_aws.iteritems():
            image[aws_attr] = response[cloudstack_attr]

    return image


def _create_describe_image_attribute_response(images, attribute):
    response = {
        'template_name_or_list': 'images.xml',
        'response_type': 'DescribeImagesResponse',
        'images': images,
    }

    return response


def _create_describe_images_response(images):
    response = {
        'template_name_or_list': 'images.xml',
        'response_type': 'DescribeImagesResponse',
        'images': images,
    }

    return response
