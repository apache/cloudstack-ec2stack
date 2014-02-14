#!/usr/bin/env python
# encoding: utf-8


def make_request(command, args, apikey, secretkey):
    signature = _generate_signature(command, args, apikey, secretkey)


def _generate_signature(command, args, apikey, secretkey):
