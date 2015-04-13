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
