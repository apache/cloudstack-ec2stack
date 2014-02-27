#!/usr/bin/env python
# encoding: utf-8

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
