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
manual instructs how to install and use the EC2Stack from a developer's perspective.

1 Introduction
==============

1.1 Intended readership
------------------------

This document covers the use for the following users of EC2Stack:

- The Developer.

1.2 Applicability
-----------------

This software user manual applies to EC2Stack, version 0.5.

1.3 Purpose
-----------

The purpose of the software user manual is to assist:

- Developers on extending or modifying EC2Stack.

1.4 How to use this document
----------------------------

Section 2 includes information for a developer. This covers installation
for development purposes, git repository location, test execution and
the automated vagrant development environment.

2 Developer Information
=======================

2.1 The code base
-----------------

The latest version of the EC2Stack code base can be found on github at
https://github.com/apache/cloudstack-ec2stack

To clone the repository execute the following command:

```
$ git clone git@github.com:apache/cloudstack-ec2stack.git
```

2.2 Installation for development purposes
-----------------------------------------

For developing EC2Stack it is recommended to run it in development mode.
To do so install it using the following command:

```
$ python setup.py develop
```

EC2Stack will still need to be configured, this can be done so by
executing ec2stack-configure as outlined in section 2 of this document.

You can start gstack in debug mode using the optional -d or --debug flag

$ ec2stack -d True

2.3 Test Execution
------------------

To run the included tests the following software is required:

-   pep8
-   pylint
-   nose
-   mock
-   coverage
-   factory-boy==1.3.0

These can be installed via the Python Package Index:

```
$ pip install pep8 pylint nose mock coverage factory-boy==1.3.0
```

Tests can be executed from the root of the code base as follows:

### 2.3.1 Style Check

```
$ pep8 --ignore=E501 *.py ec2stack
```

### 2.3.2 Lint

```
$ pylint --rcfile=pylint.rc *.py ec2stack
```

### 2.3.3 Unit Tests

```
$ nosetests --with-coverage --cover-erase --cover-package=ec2stack
--cover-html
```

A HTML base coverage report will be placed in ./cover

2.4 Vagrant Development Environment
-----------------------------------

Within the code base there is a VagrantFile and Puppet Manifests.
Assuming you have vagrant installed and configured you can execute
vagrant up.

This will bring up a new virtual machine configure with all necessary
tools for development and the code base located at /vagrant``
