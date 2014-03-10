#!/usr/bin/env python
# encoding: utf-8

"""This module contains functions for handling requests in relation to zones.
"""

from ec2stack.providers import cloudstack

from ec2stack import helpers, errors


@helpers.authentication_required
def describe_zones():
    """
    Describe a specific zone or all zones.

    @return: Response.
    """
    args = {'command': 'listZones'}
    response = cloudstack.describe_item(
        args, 'zone', errors.invalid_zone, 'ZoneName'
    )

    return _describe_zones_response(
        response
    )


def _describe_zones_response(response):
    """
    Generates a response for a describe zones request.

    @param response: Response from Cloudstack.
    @return: Response.
    """
    return {
        'template_name_or_list': 'zones.xml',
        'response_type': 'DescribeAvailabilityZonesResponse',
        'response': response
    }


def get_zone(zone_name):
    """
    Get the zone with the specified name.

    @param zone_name: The name of the zone to get.
    @return: Response.
    """
    args = {'name': zone_name, 'command': 'listZones'}
    response = cloudstack.describe_item_request(
        args, 'zone', errors.invalid_zone
    )

    return response
