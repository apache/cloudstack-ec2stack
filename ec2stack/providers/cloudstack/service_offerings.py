#!/usr/bin/env python
# encoding: utf-8

from ec2stack import errors
from ec2stack.providers import cloudstack


def get_service_offering(offering_name):
    args = {'name': offering_name, 'command': 'listServiceOfferings'}
    response = cloudstack.describe_item_request(
        args, 'serviceoffering', errors.invalid_service_offering_name
    )

    return response
