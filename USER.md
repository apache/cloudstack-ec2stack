<!---
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
--->
Abstract
========

This document is the Software Manual for EC2Stack. The Software user
manual instructs how to install and use the EC2Stack from a user's perspective.

Glossary
========

Amazon EC2 - A web service that provides resizable compute capacity in
the cloud.

Apache Cloudstack - Open source cloud computing software for creating,
managing, and deploying infrastructure cloud services.

Puppet: - IT automation software that helps system administrators manage
infrastructure throughout its lifecycle, from provisioning and
configuration to orchestration and reporting.

Python package index - Official third-party software repository for the
Python Programming language.

Vagrant - Tool for building complete development environments.

1 Introduction
==============

1.1 Intended readership
------------------------

This document covers the use for the following users of EC2Stack:

- The User.

1.2 Applicability
-----------------

This software user manual applies to EC2Stack, version 0.7.

1.3 Purpose
-----------

The purpose of the software user manual is to assist:

- Users installing and configuring EC2Stack.

1.4 How to use this document
----------------------------

Section 2 includes an overview of EC2Stack from a user perspective. This
covers installation of EC2Stack, its configuration and starting it.

Section 3 includes information for a developer. This covers installation
for development purposes, git repository location, test execution and
the automated vagrant development environment.

2 User Information
==================

2.1 Overview
------------

EC2Stack implements an API layer that sits on top of the Apache
Cloudstack API. This API layer attempts to handle requests designed for
the Amazon Web Services (AWS) Elastic Compute (EC2) API. It achieves
this by retrieving EC2 requests, converting them to Apache Cloudstack
requests and parsing the Apache Cloudstack responses into EC2 responses.

2.2 Required dependencies
-------------------------

In order to run EC2Stack your machine will need Python 2.7 installed.
EC2Stack will run best on a Linux or BSD based operating system.

2.3 Installing the software
---------------------------

EC2Stack is available on the python package index (pip). If your machine
has pip installed you can install EC2Stack by executing:

```
$ pip install ec2stack
```

Alternatively, you may install EC2Stack via a tar.gz archive:
```
$ wget https://pypi.python.org/packages/source/e/ec2stack/ec2stack-0.1.tar.gz
```

```
$ tar xf ec2stack-0.1.tar.gz && cd ec2stack-0.1.tar.gz
```

```
$ python setup.py install
```

2.4 Configuration
-----------------

Before you can start EC2Stack it must be configured. To so do run:

```
$ ec2stack-configure
```

You can configure a profile of your choice with the optional -p or --profile flag

```
$ ec2stack-configure -p exampleprofile
```

If you don't specify a profile, ec2stack-configure will default to initial

You can configure an advanced profile with

```
$ ec2stack-configure -a True
```

Launching ec2stack-configure will prompt you for various configuration options.

```
EC2Stack bind address [0.0.0.0]:
```

Binds EC2Stack to the supplied IP address. If left unset EC2Stack will
bind to all IP addresses assigned to the machine.

```
EC2Stack bind port [5000]:
```

Binds EC2stack to the supplied port. If left unset EC2Stack will port to
port 5000.

```
Cloudstack host [localhost]:
```

This is the hostname of the Apache Cloudstack server you wish to run
EC2Stack on-top off. If left unset EC2Stack will use localhost.

```
Cloudstack port [8080]:
```

This is the port of the Apache Cloudstack server you wish to run
EC2Stack on-top off. If left unset EC2Stack will use 8080.

```
Cloudstack protocol [http]:
```

This is the protocol EC2Stack should use for connecting to the specified
Apache Cloudstack API. If left unset EC2Stack will use http.

```
Cloudstack path [/client/api]:
```

This is the path of the Apache Cloudstack API that EC2Stack should
query. If left unset EC2Stack will use /client/api

```
Cloudstack custom disk offering name [Custom]:
```

This is the name of a disk offering configured on your Apache Cloudstack
server that allows for custom disk sizes to set by the user. If left
unset EC2Stack will use Custom.

```
Cloudstack default zone name:
```

This is the zone you wish EC2Stack to use on your Apache Cloudstack
infrastructure should the end user not of set a zone within their
request. This field is required.

```
Do you wish to input instance type mappings? (Yes/No): y

Insert the AWS EC2 instance type you wish to map: m1.small

Insert the name of the instance type you wish to map this to: micro
```

This allows you to map EC2 instance types to Apache Cloudstack service
offerings.

```
Do you wish to input resource type mappings for tag support? (Yes/No): y

Insert the Cloudstack resource id you wish to map: examplevirtualmachineid

Insert the Cloudstack resource type you wish to map this to: UserVm
```

This allows you to use tag related actions. 

2.5 Running
-----------

To run EC2stack execute the following command:

```
$ ec2stack
```

You can launch ec2stack using a configuration profile created earlier using the optional -p or --profile flag

```
$ ec2stack -p exampleprofile
```

EC2Stack will start up and bind to the supplied IP address and port.

2.6 Initial user registration
-----------------------------

Before EC2Stack can handle user requests the user must register their
API Key and Secret Key.

To register a secert key execute ec2stack-register:

```
$ ec2stack-register ec2stack_server_address api_key secret_key
```

To remove a secret key execute ec2stack-remove:

```
$ ec2stack-remove ec2stack_server_address api_key secret_key
```
