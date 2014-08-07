History
=======

0.6.1 (7-08-2014)
_________________

* Fix bug in VPC creation when ec2stack is configured with a basic zone

0.6.0 (20-07-2014)
__________________

* Added support for vpc operations
    * createVpc
    * deleteVpc
    * listVpc
* Clean test data
* Upgrade to Alpha

0.5.0 (9-07-2014)
_________________

* Add support for configuration profiles

    `$ ec2stack-configure --profile exampleprofile`

    `$ ec2stack --profile exampleprofile`

* Give user the ability to debug app

    `$ ec2stack --debug True`

0.4.0 (9-06-2014)
_________________

* Make api version used in responses dynamic


0.3.0 (8-06-2014)
_________________

* Added support for tag operations
    * createTags
    * deleteTags
    * listTags

0.2.0 (01-4-2014)
_________________

* Change Amazon API support from 2013-10-15 to 2014-02-01


0.1.0 (08-03-2014)
__________________

* ec2stack conception
