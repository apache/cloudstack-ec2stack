#!/usr/bin/env python
# encoding: utf-8

from ec2stack.core import Ec2stackError


def invalid_snapshot_id():
    raise Ec2stackError(
        '400',
        'InvalidSnapshot.NotFound',
        'The specified Snapshot Id does not exist.'
    )


def invalid_zone_id():
    raise Ec2stackError(
        '400',
        'InvalidZone.NotFound',
        'The specified Availability Zone Id does not exist.'
    )


def invalid_volume_id():
    raise Ec2stackError(
        '400',
        'InvalidVolume.NotFound',
        'The specified Volume Id does not exist.'
    )
