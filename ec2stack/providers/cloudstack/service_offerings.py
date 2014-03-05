#!/usr/bin/env python
# encoding: utf-8

from ec2stack import errors
from ec2stack.providers import cloudstack


def get_service_offering(offering_name):
    # We cannot use describe_item_request because there is a bug in
    # Cloudstack 4.0.0 which causes listServiceOfferings to return
    # an Empty response if a name is given.

    args = {'command': 'listServiceOfferings'}
    service_offerings = cloudstack.describe_items_request(
        args, errors.invalid_service_offering_name
    )
    for service_offering in service_offerings['serviceoffering']:
        if service_offering['name'].lower() == offering_name.lower():
            return service_offering

    errors.invalid_service_offering_name()
