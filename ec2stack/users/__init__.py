#!/usr/bin/env python
# encoding: utf-8

from ..core import Service
from .models import User


class UsersService(Service):
    __model__ = User
