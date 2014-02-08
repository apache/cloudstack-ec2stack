*** Currently a work in progress ***

==================
Cloudstack EC2 API
==================

.. image:: https://api.travis-ci.org/imduffy15/ec2stack.png?branch=master

Description
-----------

Apache Cloudstack is open source software designed to deploy and manage large networks of virtual machines, as highly available, highly scalable Infrastructure as a Service(laaS) cloud computing platform. Apache Cloudstack is used by a number of service providers to offer public cloud services, and by many companies to provide an on-premises (private) cloud offering.

Users can manage their Apache Cloudstack cloud with an easy to use web interface, command line tools and/or a full featured RESTful API.

Amazon web services(AWS) is a collection of “web services” that together make up Amazon’s cloud computing platform. The service is there to provide a large compute capacity much faster and cheaper than building a physical server farm. One of the most popular services offered is their elastic compute cloud service, better known as Amazon EC2. This service allows users to rent virtual machines in which they can run their own applications. Amazon’s EC2 service was one of the first cloud computing services brought out and as such the API Amazon exposed for the configuration and management of their virtual machines became a de facto standard for many cloud based utilities.

Bridging Apache Cloudstack with existing public cloud providers APIs is needed in order to help users work across clouds. Our project’s aim is to create an application that will sit above the Apache Cloudstack API. The application will take in common Amazon EC2 like API requests, execute the necessary Cloudstack Calls and parse the responses as required. This would allow utilities created for the Amazon EC2 API to be used against Apache Cloudstack. This effectively gives users their own private Amazon EC2-like Infrastructure.

Usage
-----

Configuration
''''''''''''''

When you install ec2stack a default global configuration file is placed into /etc/ec2stack.conf or the site-package directory for ec2stack if you are running it within a virtualenv.

You can override any global configuration options with a user configuration file. Simply create ~/.ec2stack with the options you wish to change.

+------------------+--------------------------------------+
| Option           | Description                          |
+==================+======================================+
| EC2STACK_HOST    | Address for ec2stack to listen on    |
+------------------+--------------------------------------+
| EC2STACK_PORT    | Port for ec2stack to bind to         |
+------------------+--------------------------------------+

Development
'''''''''''

Cloning the repository
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    git clone https://github.com/imduffy15/cloudstack-ec2api

Development Environment
~~~~~~~~~~~~~~~~~~~~~~~

For ease of development a VagrantFile and Puppet Manifest is included which will provision a virtual machine with all required tools installed.

Assuming you have Vagrant and Virtualbox installed executing ``vagrant up`` from the root of the codebase will result in a virtual machine being provisioned.

When the virtual machine has booted you can login to it using ``vagrant ssh``

From here you can setup a new virtualenv, install ec2stack and launch it:

.. code-block:: bash

    mkvirtualenv ec2stack
    cd /vagrant
    python setup.py develop
    ec2stack-configure
    ec2stack


