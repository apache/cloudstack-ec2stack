Apache CloudStack EC2stack
==========================

**An EC2 Compatibility Interface For Apache CloudStack**

.. image:: https://badge.fury.io/py/ec2stack.png
    :target: https://pypi.python.org/pypi/ec2stack
.. image:: https://api.travis-ci.org/apache/cloudstack-ec2stack.png?branch=master
    :target: https://travis-ci.org/apache/cloudstack-ec2stack

Description
-----------

Apache [CloudStack](http://cloudstack.apache.org) is an open source software designed to deploy and manage large networks of virtual machines, as highly available, highly scalable Infrastructure as a Service (IaaS) cloud computing platform.

ec2stack takes Amazon EC2 API requests, maps these requests to the appropriate CloudStack API calls and parses the responses as required. This allows utilities created for the Amazon EC2 API to be used against Apache CloudStack.

Easy setup with [Docker](http://docker.com)
-------------------------------------------

The easiest way to run ec2stack is to use a docker container. Pull the image from docker hub.

    $ docker pull runseb/ec2stack

Run an interactive container and configure ec2stack for your CloudStack endpoint.
Be careful to use 0.0.0.0 as the address for ec2stack server.


    $ docker run -t -i ec2stack ec2stack-configure

Commit the configured container into a new image specific to your cloud.

    $ docker commit <container id> ec2stack:yourcloud

Run an container with the ec2stack command

    $ docker run -d -p 5000:5000 ec2stack:yourcloud ec2stack

Register a user


    $ curl -d AWSSecretKey=yoursecretkey -d AWSAccessKeyId=yourapikey -d Action=RegisterSecretKey http://localhost:5000

You now just need to configure your aws cli and use the local ec2stack point:

    $ aws ec2 describe-images --endpoint=http://localhost:5000

Usage
-----

**IMPORTANT**: Please note that the current version of ec2stack only supports AWS Signature Version 2 and therefore will NOT work with the current AWS CLI unless you explicitly tell it to use Version 2.  You can set the signature version for your default AWS CLI profile with:

    $ aws configure set default.ec2.signature_version v2

If you are using named profiles then you can set the version for the specific profile with:

    $ aws configure set profile.<your profile name>.ec2.signature_version v2

Both of the above commands will update your *~/.aws/config* file.

For usage information please see the [User Guide](https://github.com/apache/cloudstack-ec2stack/USER.md).
