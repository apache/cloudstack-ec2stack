#!/usr/bin/env python
# encoding: utf-8
"""
    tests
    ~~~~~

    tests package
"""

from unittest import TestCase
from ec2stack import create_app
from .utils import FlaskTestCaseMixin


class Ec2StackTestCase(TestCase):
    pass


class Ec2StackAppTestCase(FlaskTestCaseMixin, Ec2StackTestCase):

    def _create_app(self):
        return create_app()

    def setUp(self):
        super(Ec2StackTestCase, self).setUp()
        self.app = self._create_app()
        self.client = self.app.test_client()

    def tearDown(self):
        super(Ec2StackAppTestCase, self).tearDown()
