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

"""This module creates the user model.
"""

from ec2stack.core import DB


class User(DB.Model):
    __tablename__ = 'users'
    apikey = DB.Column(DB.String(255), primary_key=True)
    secretkey = DB.Column(DB.String(255), unique=True)

    def __init__(self, apikey, secretkey):
        """
        Create's a new user.

        @param apikey: apikey associated with the user.
        @param secretkey: secret key associated with the user.
        """
        self.apikey = apikey
        self.secretkey = secretkey
