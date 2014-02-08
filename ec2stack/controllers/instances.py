#!/usr/bin/env python
# encoding: utf-8

from flask import render_template


def describe():
    instances = [
        {
            'id': '1',
            'state': 'running',
            'launch_time': 'YYYY-MM-DDTHH:MM:SS+0000',
            'hypervisor': 'dummy-hypervisor'
        },
        {
            'id': '2',
            'state': 'running',
            'launch_time': 'YYYY-MM-DDTHH:MM:SS+0000',
            'hypervisor': 'dummy-hypervisor'
        }
    ]

    return render_template(
        'instances/describe_instances.xml',
        instances=instances
    )
