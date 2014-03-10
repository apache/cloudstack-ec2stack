#!/usr/bin/env python
# encoding: utf-8

"""This module contains functions for handling requests in relation to service
offerings.
"""

from ec2stack import errors
from ec2stack.providers import cloudstack


def get_service_offering(offering_name):
    """
    Get the service offering with the specified name.

    @param offering_name: The name of the service offering to get.
    @return: Response.
    """

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
