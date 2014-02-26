#!/usr/bin/env python
# encoding: utf-8

from ec2stack.providers import cloudstack

from ec2stack import helpers, errors


@helpers.authentication_required
def describe_zones():
    args = {}
    args['command'] = 'listZones'
    response = cloudstack.describe_item(
        args, 'zone', errors.invalid_zone, 'ZoneName'
    )

    return _describe_zones_response(
        response
    )


def describe_zone_by_name(zone_name):
    args = {}
    args['name'] = zone_name
    args['command'] = 'listZones'
    response = cloudstack.describe_item_request(
        args, 'zone', errors.invalid_zone
    )
    return response


def _describe_zones_response(response):
    return {
        'template_name_or_list': 'zones.xml',
        'response_type': 'DescribeAvailabilityZonesResponse',
        'response': response
    }


def get_zones_id(name):
    zone = describe_zone_by_name(name)
    return zone['id']
