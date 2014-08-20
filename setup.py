#!/usr/bin/env python
# encoding: utf-8

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
VERSION = '0.7.1'
URL = 'http://github.com/imduffy15/ec2stack'
AUTHOR = 'Darren Brogan, Ian Duffy'
AUTHOR_EMAIL = 'brogand2@mail.dcu.ie, duffyi3@mail.dcu.ie'
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
