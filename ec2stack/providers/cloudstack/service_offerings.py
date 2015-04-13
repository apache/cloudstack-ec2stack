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
