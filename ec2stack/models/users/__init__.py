#!/usr/bin/env python
# encoding: utf-8

"""This module creates a user service.
"""

from ec2stack.core import Service
from ec2stack.models.users.models import User


class UsersService(Service):
    __model__ = User
