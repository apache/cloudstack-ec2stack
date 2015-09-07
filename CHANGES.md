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
History
=======

Under development 0.8.1
-----------------------

0.8.0 (26-08-2015)
------------------

* First release under Apache CloudStack project

0.7.1 (20-08-2014)
------------------

* Add support for gp2 ec2 instances

0.7.0 (11-08-2014)
------------------

* Added support for snapshot operations
    * createSnapshot
    * deleteSnapshot
    * listSnapshots

0.6.1 (7-08-2014)
-----------------

* Fix bug in VPC creation when ec2stack is configured with a basic zone

0.6.0 (20-07-2014)
------------------

* Added support for vpc operations
    * createVpc
    * deleteVpc
    * listVpc
* Clean test data
* Upgrade to Alpha

0.5.0 (9-07-2014)
-----------------

* Add support for configuration profiles

    $ ec2stack-configure --profile exampleprofile

    $ ec2stack --profile exampleprofile

* Give user the ability to debug app

    $ ec2stack --debug True

0.4.0 (9-06-2014)
-----------------

* Make api version used in responses dynamic

0.3.0 (8-06-2014)
-----------------

* Added support for tag operations
    * createTags
    * deleteTags
    * listTags

0.2.0 (01-4-2014)
-----------------

* Change Amazon API support from 2013-10-15 to 2014-02-01

0.1.0 (08-03-2014)
------------------

* ec2stack conception
