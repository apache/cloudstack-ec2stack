#!/usr/bin/env python
# encoding: utf-8
#
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#  
#    http://www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.
#

"""This module contains functions for handling requests in relation to images.
"""

from ec2stack import helpers, errors
from ec2stack.providers import cloudstack


@helpers.authentication_required
def describe_image_attribute():
    """
    Describes an image attribute.

    @return: Response.
    """
    image_id = helpers.get('ImageId')
    attribute = helpers.get('Attribute')

    supported_attribute_map = {
        'description': 'displaytext'
    }

    if attribute not in supported_attribute_map.iterkeys():
        errors.invalid_parameter_value(
            'The specified attribute is not valid, please specify a valid ' +
            'image attribute.'
        )

    response = describe_image_by_id(image_id)
    return _describe_image_attribute_response(
        response, attribute, supported_attribute_map)


def _describe_image_attribute_response(response, attribute, attr_map):
    """
    Generates a response for a describe image attribute request.

    @param response: Response from Cloudstack.
    @param attribute: Attribute to Describe.
    @param attr_map: Map of attributes from EC2 to Cloudstack.
    @return: Response.
    """
    return {
        'template_name_or_list': 'image_attribute.xml',
        'response_type': 'DescribeImageAttributeResponse',
        'id': response['id'],
        'attribute': attribute,
        'value': response[attr_map[attribute]]
    }


@helpers.authentication_required
def describe_images():
    """
    Describe a specific image or all images.

    @return: Response.
    """
    args = {'templatefilter': 'executable', 'command': 'listTemplates'}
    response = cloudstack.describe_item(
        args, 'template', errors.invalid_image_id, 'ImageId'
    )

    return _describe_images_response(
        response
    )


def describe_image_by_id(image_id):
    """
    Describe an image by Id.

    @param image_id: Id of the image.
    @return: Response.
    """
    args = {
        'id': image_id,
        'templatefilter': 'executable',
        'command': 'listTemplates'}
    response = cloudstack.describe_item_request(
        args, 'template', errors.invalid_image_id
    )
    return response


def _describe_images_response(response):
    """
    Generates a response for a describe images request.

    @param response: Response from Cloudstack.
    @return: Response.
    """
    return {
        'template_name_or_list': 'images.xml',
        'response_type': 'DescribeImagesResponse',
        'response': response
    }
