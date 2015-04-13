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

from unittest import TestCase

from . import settings
from ec2stack.core import DB
from ec2stack import create_app
from .factories import UserFactory
from .utils import FlaskTestCaseMixin


class Ec2StackTestCase(TestCase):
    pass


class Ec2StackAppTestCase(FlaskTestCaseMixin, Ec2StackTestCase):

    def _create_app(self):
        return create_app(settings=settings)

    def _create_fixtures(self):
        self.user = UserFactory()

    def setUp(self):
        super(Ec2StackAppTestCase, self).setUp()
        self.app = self._create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        DB.create_all()
        self._create_fixtures()

    def tearDown(self):
        super(Ec2StackAppTestCase, self).tearDown()
        DB.drop_all()
        self.app_context.pop()
