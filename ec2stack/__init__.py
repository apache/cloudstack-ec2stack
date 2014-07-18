#!/usr/bin/env python
# encoding: utf-8

"""This module creates the flask application.
"""

import os
import sys
import argparse

from flask import Flask
from ConfigParser import SafeConfigParser

from ec2stack.controllers import *
from ec2stack.core import DB
from ec2stack.models import User


def create_app(settings=None):
    """
    Creates a flask application.

    @param settings: Settings override object.
    @return: The flask application.
    """
    app = Flask(__name__)

    if settings:
        app.config.from_object(settings)
    else:
        args = _generate_args()
        profile = args.pop('profile')
        app.config['DEBUG'] = args.pop('debug')
        config_file = _load_config_file()
        database_uri = _load_database()
        _config_from_config_profile(config_file, profile, app)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

    DB.init_app(app)

    default_controller = __import__(
        'ec2stack.controllers.' + 'default', None, None, 'DEFAULT'
    )
    default_controller = getattr(default_controller, 'DEFAULT')
    app.register_blueprint(default_controller)

    return app


def _generate_args():
    """
    Generate command line arguments for ec2stack-configure.

    @return: args.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-p',
        '--profile',
        required=False,
        help='The profile to run ec2stack with, default is initial',
        default='initial'
    )

    parser.add_argument(
        '-d',
        '--debug',
        required=False,
        help='Turn debug on for application',
        default=False
    )

    args = parser.parse_args()

    return vars(args)


def _load_config_file():
    """
    Checks that the user's configuration file exists and returns its path.

    @return: The path to the user's configuration file.
    """
    config_file = os.path.join(
        os.path.expanduser('~'),
        '.ec2stack/ec2stack.conf'
    )

    if not os.path.exists(config_file):
        sys.exit('No configuration found, please run ec2stack-configure')

    return config_file


def _config_from_config_profile(config_file, profile, app):
    """
    Configures ec2stack app based on configuration profile.

    @param config_file: current config file configuration.
    @param profile: the profile to set the attribute in.
    """
    config = SafeConfigParser()
    config.read(config_file)

    if not config.has_section(profile):
        sys.exit('No profile matching ' + profile
                 + ' found in configuration, please run ec2stack-configure -p '
                 + profile)

    for attribute in config.options(profile):
        app.config[attribute.upper()] = config.get(profile, attribute)

    instance_type_map = {}
    instance_section = profile + "instancemap"
    if config.has_section(instance_section):
        for attribute in config.options(instance_section):
            instance_type_map[attribute] = config.get(instance_section, attribute)

    app.config['INSTANCE_TYPE_MAP'] = instance_type_map

    resource_type_map = {}
    resource_section = profile + "resourcemap"
    if config.has_section(resource_section):
        for attribute in config.options(resource_section):
            resource_type_map[attribute] = config.get(resource_section, attribute)

    app.config['RESOURCE_TYPE_MAP '] = resource_type_map


def _load_database():
    """
    Checks that the user's database exists and returns its uri.

    @return: The uri to the user's database.
    """
    database_file = os.path.join(
        os.path.expanduser('~'),
        '.ec2stack/ec2stack.sqlite'
    )

    if not os.path.exists(database_file):
        sys.exit('No database found, please run ec2stack-configure')

    return 'sqlite:///' + database_file
