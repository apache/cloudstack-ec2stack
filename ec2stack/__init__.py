#!/usr/bin/env python
# encoding: utf-8

"""This module creates the flask application.
"""

import os
import sys

from flask import Flask

from ec2stack.controllers import *
from ec2stack.core import DB
from ec2stack.models import User


def create_app(settings=None):
    """
    Creates a flask application.

    @param settings: Settings override object.
    @return: The flask application
    """
    app = Flask(__name__)

    if settings:
        app.config.from_object(settings)
    else:
        config_file = _load_config_file()
        app.config.from_pyfile(config_file)
        database_uri = _load_database()
        app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

    _valid_config_file(app)
    DB.init_app(app)

    default_controller = __import__(
        'ec2stack.controllers.' + 'default', None, None, 'DEFAULT'
    )
    default_controller = getattr(default_controller, 'DEFAULT')
    app.register_blueprint(default_controller)

    return app


def _load_config_file():
    """
    Checks that the users configuration file exists and returns its path.

    @return: The path to the users configuration file.
    """
    config_file = os.path.join(
        os.path.expanduser('~'),
        '.ec2stack/ec2stack.conf'
    )

    if not os.path.exists(config_file):
        sys.exit('No configuration found, please run ec2stack-configure')

    return config_file


def _valid_config_file(app):
    """
    Validates that the configuration file has all the required parameters.

    @param app: The flask application.
    """
    for config_item in ['EC2STACK_BIND_ADDRESS', 'EC2STACK_PORT',
                        'CLOUDSTACK_HOST', 'CLOUDSTACK_PORT',
                        'CLOUDSTACK_PROTOCOL', 'CLOUDSTACK_PATH',
                        'CLOUDSTACK_CUSTOM_DISK_OFFERING',
                        'CLOUDSTACK_DEFAULT_ZONE']:
        if config_item not in app.config:
            sys.exit('Configuration file is missing %s' % config_item)


def _load_database():
    """
    Checks that the users database exists and returns its uri.

    @return: The uri to the users database.
    """
    database_file = os.path.join(
        os.path.expanduser('~'),
        '.ec2stack/ec2stack.sqlite'
    )

    if not os.path.exists(database_file):
        sys.exit('No database found, please run ec2stack-configure')

    return 'sqlite:///' + database_file
