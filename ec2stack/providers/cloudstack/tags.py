#!/usr/bin/env python
# encoding: utf-8

"""This module contains functions for handling requests in relation to tags.
"""

from ec2stack import helpers
from ec2stack.providers import cloudstack
from ec2stack.providers.cloudstack import requester


@helpers.authentication_required
def create_tags():
    """
    Create a tag.

    @return: Response.
    """
    _create_tag_request()
    return _create_tag_response()


def _create_tag_request():
    """
    Request to create a tag.

    @return: Response.
    """

    args = {
        'command': 'createTags',
        'name': helpers.get('ResourceId')
    }

    keys = helpers.get_request_parameter_keys('Key')
    values = helpers.get_request_parameter_keys('value')

    for index in range(len(keys)):
        args['tags[' + index + '].key'] = keys[index]
        args['tags[' + index + '].value'] = values[index]

    response = requester.make_request(args)

    response = response['createtagsresponse']

    return response


def _create_tag_response():
    """
    Generates a response for a create tag request.

    @return: Response.
    """
    return {
        'template_name_or_list': 'status.xml',
        'response_type': 'CreateTagsResponse',
        'return': 'true'
    }


@helpers.authentication_required
def describe_tags():
    """
    Describe all tags.

    @return: Response.
    """
    args = {'command': 'listTags'}
    response = requester.make_request(args)
    response = cloudstack.describe_item(
        args, 'tag', {}, 'TagId'
    )

    return _describe_tags_response(
        response
    )


def _describe_tags_response(response):
    """
    Generates a response for a describe tags request.

    @param response: Response from Cloudstack.
    @return: Response.
    """
    return {
        'template_name_or_list': 'tags.xml',
        'response_type': 'DescribeTagsResponse',
        'response': response
    }
