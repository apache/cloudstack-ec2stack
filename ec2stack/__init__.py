#!/usr/bin/env python
# encoding: utf-8

import os
import sys

from flask import Flask

from ec2stack.controllers import *
from ec2stack.core import DB
from ec2stack.models import User


def create_app():
    app = Flask(__name__)

    _load_config_file(app)
    _load_database(app)

    default_controller = __import__(
        'ec2stack.controllers.' + 'default', None, None, 'DEFAULT'
    )
    default_controller = getattr(default_controller, 'DEFAULT')
    app.register_blueprint(default_controller)

    return app


def _load_config_file(app):
    config_file = os.path.join(
        os.path.expanduser('~'),
        '.ec2stack/ec2stack.conf'
    )

    if not os.path.exists(config_file):
        sys.exit('No configuration found, please run ec2stack-configure')

    app.config.from_pyfile(config_file)

    for config_item in ['EC2STACK_BIND_ADDRESS', 'EC2STACK_PORT',
                        'CLOUDSTACK_HOST', 'CLOUDSTACK_PORT',
                        'CLOUDSTACK_PROTOCOL', 'CLOUDSTACK_PATH']:
        if config_item not in app.config:
            sys.exit('Configuration file is missing %s' % config_item)


def _load_database(app):
    database_file = os.path.join(
        os.path.expanduser('~'),
        '.ec2stack/ec2stack.sqlite'
    )

    if not os.path.exists(database_file):
        sys.exit('No database found, please run ec2stack-configure')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_file
    DB.init_app(app)
