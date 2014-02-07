#!/usr/bin/env python
# encoding: utf-8

import os

from alembic import command
from alembic.config import Config as AlembicConfig


def main():
    config_folder = _create_config_folder()
    _create_config_file(config_folder)
    _create_database()


def _create_config_folder():
    config_folder = os.path.join(os.path.expanduser('~'), '.ec2stack')
    if not os.path.exists(config_folder):
        os.makedirs(config_folder)

    return config_folder


def _create_config_file(config_folder):
    host = raw_input('EC2Stack bind address [0.0.0.0]: ')
    port = raw_input('EC2Stack bind port [5000]: ')

    config_file = open(config_folder + '/ec2stack.conf', 'w+')
    if host != '':
        config_file.write("EC2STACK_HOST = '%s'\n" % (host))
    if port != '':
        config_file.write("EC2STACK_PORT = '%s'\n" % (port))
    config_file.close()


def _create_database():
    directory = os.path.join(os.path.dirname(__file__), 'migrations')
    config = AlembicConfig(os.path.join(
        directory,
        'alembic.ini'
    ))
    config.set_main_option('script_location', directory)
    command.upgrade(config, 'head', sql=False, tag=None)
