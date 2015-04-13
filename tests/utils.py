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

class FlaskTestCaseMixin(object):

    @staticmethod
    def _html_data(kwargs):
        if not kwargs.get('content_type'):
            kwargs['content_type'] = 'application/x-www-form-urlencoded'
        return kwargs

    @staticmethod
    def _request(method, *args, **kwargs):
        return method(*args, **kwargs)

    def post(self, *args, **kwargs):
        return (
            self._request(self.client.post, *args, **self._html_data(kwargs))
        )

    def assert_status_code(self, response, status_code):
        self.assertEquals(status_code, response.status_code)
        return response

    def assert_ok(self, response):
        return self.assert_status_code(response, 200)

    def assert_bad_request(self, response):
        return self.assert_status_code(response, 400)

    def assert_not_found(self, response):
        return self.assert_status_code(response, 404)

    @staticmethod
    def get_example_data():
        data = {
            'SignatureVersion': '2',
            'AWSAccessKeyId': 'ExampleAPIKey',
            'Version': '2013-10-15',
            'Timestamp': '2014-02-19T23:34:43.868347',
            'SignatureMethod': 'HmacSHA256',
            'Signature': 'g7HMf6RY4oCeaBaea0zlObjVX43NEH8yv3pclvu+Ibo=',
            'Action': 'CreateKeyPair'
        }
        return data
