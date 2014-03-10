#!/usr/bin/env python
# encoding: utf-8

"""This module contains functions for handling requests in relation to disk
offerings.
"""

from ec2stack import errors
from ec2stack.providers import cloudstack


def get_disk_offering(disk_name):
    """
    Get the disk offering with the specified name.

    @param disk_name: Name of the disk offering to get.
    @return: Response.
    """
    args = {'name': disk_name, 'command': 'listDiskOfferings'}
    response = cloudstack.describe_item_request(
        args, 'diskoffering', errors.invalid_disk_offering_name
    )

    return response
