#!/usr/bin/env python
# encoding: utf-8

from ec2stack.core import Ec2stackError


def invalid_snapshot_id():
    raise Ec2stackError(
        '400',
        'InvalidSnapshot.NotFound',
        'The specified Snapshot Id does not exist.'
    )


def invalid_image_id():
    raise Ec2stackError(
        '400',
        'InvalidAMIID.NotFound',
        'The specified AMI Id does not exist.'
    )


def invalid_instance_id():
    raise Ec2stackError(
        '400',
        'InvalidInstanceId.NotFound',
        'The specified Instance Id does not exist.'
    )


def invalid_zone():
    raise Ec2stackError(
        '400',
        'InvalidZone.NotFound',
        'The specified Availability Zone does not exist.'
    )


def invalid_volume_id():
    raise Ec2stackError(
        '400',
        'InvalidVolume.NotFound',
        'The specified Volume Id does not exist.'
    )


def invalid_disk_offering_name():
    raise Ec2stackError(
        '400',
        'InvalidDiskOffering.NotFound',
        'The specified Disk offering does not exist.'
    )


def invalid_service_offering_name():
    raise Ec2stackError(
        '400',
        'InvalidServiceOffering.NotFound',
        'The specified Service offering does not exist.'
    )


def invalid_keypair_name():
    raise Ec2stackError(
        '400',
        'InvalidKeyPair.NotFound',
        'The specified KeyPair does not exist'
    )


def duplicate_keypair_name():
    raise Ec2stackError(
        '400',
        'InvalidKeyPair.Duplicate',
        'The keypair already exists.'
    )


def duplicate_security_group():
    raise Ec2stackError(
        '400',
        'InvalidGroup.Duplicate',
        'The security group already exists.'
    )


def invalid_security_group():
    raise Ec2stackError(
        '400',
        'InvalidGroup.NotFound',
        'The specified security group does not exist.'
    )


def invalid_permission():
    raise Ec2stackError(
        '400',
        'InvalidPermission.NotFound',
        'The specified permission does not exist in specified security group'
    )


def missing_paramater(parameter):
    raise Ec2stackError(
        '400',
        'MissingParameter',
        'The request must contain the parameter %s' % parameter
    )


def invalid_paramater_value(message):
    raise Ec2stackError(
        '400',
        'InvalidParameterValue',
        message
    )
