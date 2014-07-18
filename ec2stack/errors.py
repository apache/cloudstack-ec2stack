#!/usr/bin/env python
# encoding: utf-8

"""This module contains functions for error reporting.
"""

from ec2stack.core import Ec2stackError


def invalid_snapshot_id():
    """
    Invalid snapshot Id.

    @raise Ec2stackError: Defining a bad request and message.
    """
    raise Ec2stackError(
        '400',
        'InvalidSnapshot.NotFound',
        'The specified Snapshot Id does not exist.'
    )


def invalid_image_id():
    """
    Invalid Image Id Error.

    @raise Ec2stackError: Defining a bad request and message.
    """
    raise Ec2stackError(
        '400',
        'InvalidAMIID.NotFound',
        'The specified AMI Id does not exist.'
    )


def invalid_instance_id():
    """
    Invalid Instance Id.

    @raise Ec2stackError: Defining a bad request and message.
    """
    raise Ec2stackError(
        '400',
        'InvalidInstanceId.NotFound',
        'The specified Instance Id does not exist.'
    )


def invalid_zone():
    """
    Invalid Zone.

    @raise Ec2stackError: Defining a bad request and message.
    """
    raise Ec2stackError(
        '400',
        'InvalidZone.NotFound',
        'The specified Availability Zone does not exist.'
    )


def invalid_volume_id():
    """
    Invalid volume Id.

    @raise Ec2stackError: Defining a bad request and message.
    """
    raise Ec2stackError(
        '400',
        'InvalidVolume.NotFound',
        'The specified Volume Id does not exist.'
    )


def invalid_volume_attached():
    """
    Invalid volume, volume is already attached.

    @raise Ec2stackError: Defining a bad request and message.
    """
    raise Ec2stackError(
        '400',
        'InvalidVolume.Attached',
        'The specified Volume is already attached.'
    )


def invalid_volume_detached():
    """
    Invalid volume, volume is already detached.

    @raise Ec2stackError: Defining a bad request and message.
    """
    raise Ec2stackError(
        '400',
        'InvalidVolume.Detached',
        'The specified Volume isn\'t attached.'
    )


def invalid_disk_offering_name():
    """
    Invalid disk offering id.

    @raise Ec2stackError: Defining a bad request and message.
    """
    raise Ec2stackError(
        '400',
        'InvalidDiskOffering.NotFound',
        'The specified Disk offering does not exist.'
    )


def invalid_service_offering_name():
    """
    Invalid Service Offering name.

    @raise Ec2stackError: Defining a bad request and message.
    """
    raise Ec2stackError(
        '400',
        'InvalidServiceOffering.NotFound',
        'The specified Service offering does not exist.'
    )


def invalid_keypair_name():
    """
    Invalid key pair name.

    @raise Ec2stackError: Defining a bad request and message.
    """
    raise Ec2stackError(
        '400',
        'InvalidKeyPair.NotFound',
        'The specified KeyPair does not exist'
    )


def duplicate_keypair_name():
    """
    Duplicate key pair name.

    @raise Ec2stackError: Defining a bad request and message.
    """
    raise Ec2stackError(
        '400',
        'InvalidKeyPair.Duplicate',
        'The keypair already exists.'
    )


def invalid_resource_id():
    """
    Resource with this ID does not exist.

    @raise Ec2stackError: Defining a bad request and message.
    """
    raise Ec2stackError(
        '400',
        'InvalidID',
        'The specified ID for the resource you are trying to tag is not valid.'
    )


def invalid_vpc_range():
    """
    Invalid cidr block.

    @raise Ec2stackError: Defining a bad request and message.
    """
    raise Ec2stackError(
        '400',
        'InvalidVpcRange',
        'The specified CIDR block range is not valid.'
    )


def invalid_vpc_id():
    """
    VPC with this ID does not exist.

    @raise Ec2stackError: Defining a bad request and message.
    """
    raise Ec2stackError(
        '400',
        'InvalidVpcID.NotFound',
        'The specified VPC does not exist.'
    )


def duplicate_security_group():
    """
    Duplicate Security Group.

    @raise Ec2stackError: Defining a bad request and message.
    """
    raise Ec2stackError(
        '400',
        'InvalidGroup.Duplicate',
        'The security group already exists.'
    )


def invalid_security_group():
    """
    Invalid Security Group.

    @raise Ec2stackError: Defining a bad request and message.
    """
    raise Ec2stackError(
        '400',
        'InvalidGroup.NotFound',
        'The specified security group does not exist.'
    )


def invalid_permission():
    """
    Invalid Permission.

    @raise Ec2stackError: Defining a bad request and message.
    """
    raise Ec2stackError(
        '400',
        'InvalidPermission.NotFound',
        'The specified permission does not exist in specified security group'
    )


def invalid_request(message):
    """
    Invalid Request.

    @raise Ec2stackError: Defining a bad request and message.
    """
    raise Ec2stackError(
        '400',
        'InvalidRequest',
        message
    )


def missing_parameter(parameter):
    """
    Missing Parameter.

    @param parameter: Parameter that is missing.
    @raise Ec2stackError: Defining a bad request and message.
    """
    raise Ec2stackError(
        '400',
        'MissingParameter',
        'The request must contain the parameter %s' % parameter
    )


def invalid_parameter_value(message):
    """
    Invalid Paramater Value.

    @param message: Error message to use.
    @raise Ec2stackError: Defining a bad request and message.
    """
    raise Ec2stackError(
        '400',
        'InvalidParameterValue',
        message
    )


def apikey_not_found(apikey):
    raise Ec2stackError(
        '401',
        'AuthFailure',
        'Unable to find a secret key for %s, please ensure you registered'
        % apikey
    )


def authentication_failure():
    raise Ec2stackError(
        '401',
        'AuthFailure',
        'AWS was not able to validate the provided access credentials.'
    )
