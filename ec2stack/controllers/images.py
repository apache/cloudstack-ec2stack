#!/usr/bin/env python
# encoding: utf-8

from ec2stack.helpers import authentication_required
from ec2stack.controllers.cloudstack import requester


cloudstack_attributes_to_aws = {
    'id': 'id',
    'name': 'name',
    'isready': 'state',
    'hypervisor': 'hypervisor',
    'displaytext': 'description'
}


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


def _cloudstack_template_to_aws_image(response):
    image = {}
    for cloudstack_attr, aws_attr in cloudstack_attributes_to_aws.iteritems():
        image[aws_attr] = response[cloudstack_attr]

    return image


def _describe_images_format_response(images):
    response = {
        'template_name_or_list': 'images.xml',
        'response_type': 'DescribeImagesResponse',
        'images': images,
    }

    return response
