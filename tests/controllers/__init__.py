#!/usr/bin/env python
# encoding: utf-8
"""
    tests.api
    ~~~~~~~~~

    api tests package
"""


from .. import Ec2StackAppTestCase


class Ec2StackControllerTestCase(Ec2StackAppTestCase):

    def setUp(self):
        super(Ec2StackControllerTestCase, self).setUp()
