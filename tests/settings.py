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

EC2STACK_BIND_ADDRESS = '0.0.0.0'
EC2STACK_PORT = '5000'
CLOUDSTACK_HOST = 'api.exoscale.ch'
CLOUDSTACK_PORT = '443'
CLOUDSTACK_PROTOCOL = 'https'
CLOUDSTACK_PATH = '/compute'
CLOUDSTACK_CUSTOM_DISK_OFFERING = 'Custom'
CLOUDSTACK_DEFAULT_ZONE = 'CH-GV2'
VPC_OFFERING_ID = "OFFERINGID"

INSTANCE_TYPE_MAP = {'m1.small': 'micro'}
RESOURCE_TYPE_MAP = {'exampleresourceid': 'UserVm'}

DEBUG = False
TESTING = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
