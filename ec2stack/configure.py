#!/usr/bin/env python
# encoding: utf-8

"""This module provides functions to generate an ec2stack configuration file.
"""

import os
import argparse

from alembic import command
from ConfigParser import SafeConfigParser
from alembic.config import Config as AlembicConfig


def main():
    """
    Entry point into the configuration application.

    """
    config_folder = _create_config_folder()
    _create_config_file(config_folder)
    _create_database()


def _create_config_folder():
    """
    Creates a folder to hold the user's configuration files.

    @return: Path of the configuration folder.
    """
    config_folder = os.path.join(os.path.expanduser('~'), '.ec2stack')
    if not os.path.exists(config_folder):
        os.makedirs(config_folder)
    os.chmod(config_folder, 0700)
    return config_folder


def _create_config_file(config_folder):
    """
    Reads in configuration items and writes them out to the configuration file.

    @param config_folder: Path of the configuration folder.
    """
    args = _generate_args()
    profile = args.pop('profile')
    advanced_network_enabled = args.pop('advanced')
    config_file_path = config_folder + '/ec2stack.conf'
    config = _modify_config_profile(config_file_path, profile, advanced_network_enabled)
    config_file = open(config_file_path, 'w+')
    config.write(config_file)


def _generate_args():
    """
    Generate command line arguments for ec2stack-configure.

    @return: args.
    """
    parser = argparse.ArgumentParser(
        'Command line utility for configuring ec2stack'
    )

    parser.add_argument(
        '-p',
        '--profile',
        required=False,
        help='The profile to configure, default is initial',
        default='initial'
    )

    parser.add_argument(
        '-a',
        '--advanced',
        required=False,
        help='Turn advanced network config on for application',
        default=False
    )

    args = parser.parse_args()

    return vars(args)


def _modify_config_profile(config_file, profile, advanced_network_enabled):
    """
    Modify configuration profile.

    @param config_file: current config file configuration.
    @param profile: the profile to set the attribute in.
    @return: configparser configuration.
    """
    config = SafeConfigParser()
    config.read(config_file)

    if not config.has_section(profile):
        config.add_section(profile)

    config = _set_mandatory_attributes_of_profile(config, profile)

    if advanced_network_enabled:
        config = _set_advanced_network_attributes_of_profile(config, profile)

    config = _set_optional_attributes_of_profile(config, profile)

    return config


def _set_mandatory_attributes_of_profile(config, profile):
    """
    Modify mandatory attributes of profile.

    @param config: current configparser configuration.
    @param profile: the profile to set the attribute in.
    @return: configparser configuration.
    """
    config = _set_attribute_of_profile(
        config, profile, 'ec2stack_bind_address', 'EC2Stack bind address', 'localhost'
    )
    config = _set_attribute_of_profile(
        config, profile, 'ec2stack_port', 'EC2Stack bind port', '5000'
    )
    config = _set_attribute_of_profile(
        config, profile, 'cloudstack_host', 'Cloudstack host', 'localhost'
    )
    config = _set_attribute_of_profile(
        config, profile, 'cloudstack_port', 'Cloudstack port', '8080'
    )
    config = _set_attribute_of_profile(
        config, profile, 'cloudstack_protocol', 'Cloudstack protocol', 'http'
    )
    config = _set_attribute_of_profile(
        config, profile, 'cloudstack_path', 'Cloudstack path', '/client/api'
    )
    config = _set_attribute_of_profile(
        config, profile, 'cloudstack_custom_disk_offering', 'Cloudstack custom disk offering name', 'Custom'
    )

    while True:
        config = _set_attribute_of_profile(
            config, profile, 'cloudstack_default_zone', 'Cloudstack default zone name', ''
        )
        if config.get(profile, 'cloudstack_default_zone') is not '':
            break

    return config


def _set_advanced_network_attributes_of_profile(config, profile):
    """
    Modify advanced network attributes of profile.

    @param config: current configparser configuration.
    @param profile: the profile to set the attribute in.
    @return: configparser configuration.
    """
    config = _set_attribute_of_profile(
        config, profile, 'vpc_offering_id', 'VPC offering id', ''
    )

    return config


def _set_optional_attributes_of_profile(config, profile):
    """
    Modify optional attributes of profile.

    @param config: current configparser configuration.
    @param profile: the profile to set the attribute in.
    @return: configparser configuration.
    """
    configure_instance_type_mapings = raw_input(
        'Do you wish to input instance type mappings? (Yes/No): '
    )

    if configure_instance_type_mapings.lower() in ['yes', 'y']:
        config = _read_user_instance_mappings(config, profile)

    configure_resource_type_mapings = raw_input(
        'Do you wish to input resource type to resource id mappings'
        + ' for tag support? (Yes/No): '
    )

    if configure_resource_type_mapings.lower() in ['yes', 'y']:
        config = _read_user_resource_type_mappings(config, profile)

    return config


def _read_user_instance_mappings(config, profile):
    """
    Add instance type mappings to profile.

    @param config: current configparser configuration.
    @param profile: the profile to set the attribute in.
    @return: configparser configuration.
    """
    instance_section = profile + "instancemap"
    if not config.has_section(instance_section):
        config.add_section(instance_section)

    while True:
        key = raw_input(
            'Insert the AWS EC2 instance type you wish to map: '
        )

        value = raw_input(
            'Insert the name of the instance type you wish to map this to: '
        )

        config.set(instance_section, key, value)

        add_more = raw_input(
            'Do you wish to add more mappings? (Yes/No): ')
        if add_more.lower() in ['no', 'n']:
            break

    return config


def _read_user_resource_type_mappings(config, profile):
    """
    Add resource type mappings to profile.

    @param config: current configparser configuration.
    @param profile: the profile to set the attribute in.
    @return: configparser configuration.
    """
    resource_section = profile + "resourcemap"
    if not config.has_section(resource_section):
        config.add_section(resource_section)

    while True:
        key = raw_input(
            'Insert the cloudstack resource id you wish to map: '
        )

        value = raw_input(
            'Insert the cloudstack resource type you wish to map this to: '
        )

        config.set(resource_section, key, value)

        add_more = raw_input(
            'Do you wish to add more mappings? (Yes/No): ')
        if add_more.lower() in ['no', 'n']:
            break

    return config


def _set_attribute_of_profile(config, profile, attribute, message, default):
    """
    Set attribute of profile

    @param config: current configparser configuration.
    @param profile: the profile to set the attribute in.
    @param attribute: the attribute to set.
    @param message: the message to prompt the user with.
    @param default: the default value to use if none is entered.
    @return: configparser configuration.
    """
    if config.has_option(profile, attribute):
        default = config.get(profile, attribute)

    attribute_value = _read_in_config_attribute_or_use_default(message, default)

    config.set(profile, attribute, attribute_value)
    return config


def _read_in_config_attribute_or_use_default(message, default):
    """
    Add resource type mappings to profile.

    @param message: the message to prompt the user with.
    @param default: the default value to use if none is entered.
    @return: configparser configuration.
    """
    attribute = raw_input(message + ' [' + default + ']: ')
    if attribute == '':
        attribute = default

    return attribute


def _create_database():
    """
    Creates/Updates the database.
    """
    directory = os.path.join(os.path.dirname(__file__), '../migrations')
    config = AlembicConfig(os.path.join(
        directory,
        'alembic.ini'
    ))
    config.set_main_option('script_location', directory)
    command.upgrade(config, 'head', sql=False, tag=None)
