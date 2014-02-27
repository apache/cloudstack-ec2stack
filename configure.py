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
    ec2stack_address = raw_input('EC2Stack bind address [0.0.0.0]: ')
    if ec2stack_address == '':
        ec2stack_address = '0.0.0.0'

    ec2stack_port = raw_input('EC2Stack bind port [5000]: ')
    if ec2stack_port == '':
        ec2stack_port = '5000'

    cloudstack_host = raw_input('Cloudstack host [localhost]: ')
    if cloudstack_host == '':
        cloudstack_host = 'localhost'

    cloudstack_port = raw_input('Cloudstack port [8080]: ')
    if cloudstack_port == '':
        cloudstack_port = '8080'

    cloudstack_protocol = raw_input('Cloudstack protocol [http]: ')
    if cloudstack_protocol == '':
        cloudstack_protocol = 'http'

    cloudstack_path = raw_input('Cloudstack Path [/client/api]: ')
    if cloudstack_path == '':
        cloudstack_path = '/client/api'

    config_file = open(config_folder + '/ec2stack.conf', 'w+')
    config_file.write('EC2STACK_BIND_ADDRESS = \'%s\'\n' % ec2stack_address)
    config_file.write('EC2STACK_PORT = \'%s\'\n' % ec2stack_port)
    config_file.write('CLOUDSTACK_HOST = \'%s\'\n' % cloudstack_host)
    config_file.write('CLOUDSTACK_PORT = \'%s\'\n' % cloudstack_port)
    config_file.write('CLOUDSTACK_PROTOCOL = \'%s\'\n' % cloudstack_protocol)
    config_file.write('CLOUDSTACK_PATH = \'%s\'\n' % cloudstack_path)
    config_file.close()


def _create_database():
    directory = os.path.join(os.path.dirname(__file__), 'migrations')
    config = AlembicConfig(os.path.join(
        directory,
        'alembic.ini'
    ))
    config.set_main_option('script_location', directory)
    command.upgrade(config, 'head', sql=False, tag=None)
