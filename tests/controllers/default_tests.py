#!/usr/bin/env python
# encoding: utf-8
"""
    tests.api.product_tests
    ~~~~~~~~~~~~~~~~~~~~~~~

    api product tests module
"""

from . import Ec2StackControllerTestCase


class DefaultControllerTestCase(Ec2StackControllerTestCase):
    def example_test(self):
        r = self.post(
            '/',
            data={
                'Action': 'DescribeImages'
            }
        )
        self.assertOk(r)
