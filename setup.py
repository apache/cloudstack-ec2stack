#!/usr/bin/env python
# encoding: utf-8
#
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.
#

import os

from setuptools import setup


def read_file(name):
    filepath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        name
    )
    data = open(filepath)
    try:
        return data.read()
    except IOError:
        print "could not read %r" % name
        data.close()


PROJECT = 'ec2stack'
VERSION = '1.0.0'
URL = 'https://git-wip-us.apache.org/repos/asf?p=cloudstack-ec2stack.git'
AUTHOR = 'Apache Software Foundation'
AUTHOR_EMAIL = 'dev@cloudstack.apache.org'
DESC = "EC2 compatibility interface for Apache Cloudstack"
LONG_DESC = read_file('README.rst')
REQUIRES = [
    'Flask-SQLAlchemy', 'flask', 'requests', 'alembic'
]

setup(
    name=PROJECT,
    version=VERSION,
    description=DESC,
    long_description=LONG_DESC,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license='Apache License (2.0)',
    package_data={'ec2stack': ['templates/*.xml'],
                  'migrations': ['*.mako', 'versions/*']},
    packages=['ec2stack',
              'ec2stack.controllers',
              'ec2stack.providers',
              'ec2stack.models',
              'ec2stack.models.users',
              'ec2stack.providers.cloudstack',
              'migrations'],
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIRES,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2.7',
    ],
    entry_points="""
        [console_scripts]
        ec2stack = ec2stack.__main__:main
        ec2stack-configure = ec2stack.configure:main
        ec2stack-register = ec2stack.secretkey_manager:register
        ec2stack-remove = ec2stack.secretkey_manager:remove
    """
)
