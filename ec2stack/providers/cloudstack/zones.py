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
