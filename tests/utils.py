#!/usr/bin/env python
# encoding: utf-8
"""
    tests.utils
    ~~~~~~~~~~~

    test utilities
"""


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
