#!/usr/bin/env python
# encoding: utf-8

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
