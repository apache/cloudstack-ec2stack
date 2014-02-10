#!/usr/bin/env python
# encoding: utf-8

import os
from glob import glob
from setuptools import setup


def read_file(name):
    data = open(name)
    try:
        return data.read()
    except IOError:
        print "could not read %r" % name
        data.close()

PROJECT = 'ec2stack'
VERSION = '0.1'
URL = 'http://nopping.github.io/ec2stack'
AUTHOR = 'Darren Brogan, Ian Duffy'
AUTHOR_EMAIL = 'brogand2@mail.dcu.ie, duffyi3@mail.dcu.ie'
DESC = "EC2 compatible interface for Apache Cloudstack"
LONG_DESC = read_file('README.rst')
REQUIRES = [
    'Flask', 'Flask-Migrate', 'Flask-Script', 'Flask-SQLAlchemy'
]
DATA_FILES = []
if os.getenv('VIRTUAL_ENV', False):
    DATA_FILES.append(('conf', glob('conf/*.conf')))
else:
    DATA_FILES.append(('/etc/ec2stack', glob('conf/*.conf')))


setup(
    name=PROJECT,
    version=VERSION,
    description=DESC,
    long_description=LONG_DESC,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license='Apache',
    packages=['ec2stack'],
    include_package_data=True,
    zip_safe=False,
    data_files=DATA_FILES,
    install_requires=REQUIRES,
    classifiers=[
        "Programming Language :: Python",
    ],
    entry_points="""
        [console_scripts]
        ec2stack = ec2stack.__main__:main
        ec2stack-configure = configure:main
    """,
)
