#!/usr/bin/env python
# encoding: utf-8

from ec2stack.core import Service
from ec2stack.models import User


class UsersService(Service):
    __model__ = User
