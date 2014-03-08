#!/usr/bin/env python
# encoding: utf-8

from ec2stack.providers import cloudstack

from ec2stack import helpers, errors


@helpers.authentication_required
def describe_zones():
    """


    @return:
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

    @param response:
    @return:
    """
    return {
        'template_name_or_list': 'zones.xml',
        'response_type': 'DescribeAvailabilityZonesResponse',
        'response': response
    }


def get_zone(zone_name):
    """

    @param zone_name:
    @return:
    """
    args = {'name': zone_name, 'command': 'listZones'}
    response = cloudstack.describe_item_request(
        args, 'zone', errors.invalid_zone
    )

    return response
