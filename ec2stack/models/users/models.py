#!/usr/bin/env python
# encoding: utf-8

from ec2stack.core import DB


class User(DB.Model):
    __tablename__ = 'users'
    apikey = DB.Column(DB.String(255), primary_key=True)
    secretkey = DB.Column(DB.String(255), unique=True)

    def __init__(self, apikey, secretkey):
        """

        @param apikey:
        @param secretkey:
        """
        self.apikey = apikey
        self.secretkey = secretkey
