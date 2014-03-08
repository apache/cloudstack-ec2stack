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

Please see the Software User Manual_ located on the Wiki.

.. _User Software Manual: https://github.com/imduffy15/ec2stack/wiki/Software-User-Manual
