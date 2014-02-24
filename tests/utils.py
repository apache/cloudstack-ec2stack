#!/usr/bin/env python
# encoding: utf-8
"""
    tests.utils
    ~~~~~~~~~~~

    test utilities
"""


class FlaskTestCaseMixin(object):
    def _html_data(self, kwargs):
        if not kwargs.get('content_type'):
            kwargs['content_type'] = 'application/x-www-form-urlencoded'
        return kwargs

    def _request(self, method, *args, **kwargs):
        return method(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self._request(self.client.get, *args, **kwargs)

    def post(self, *args, **kwargs):
        return (
            self._request(self.client.post, *args, **self._html_data(kwargs))
        )

    def put(self, *args, **kwargs):
        return self._request(self.client.put, *args, **self._html_data(kwargs))

    def delete(self, *args, **kwargs):
        return self._request(self.client.delete, *args, **kwargs)

    def assertStatusCode(self, response, status_code):
        self.assertEquals(status_code, response.status_code)
        return response

    def assertOk(self, response):
        return self.assertStatusCode(response, 200)

    def assertBadRequest(self, response):
        return self.assertStatusCode(response, 400)

    def assertForbidden(self, response):
        return self.assertStatusCode(response, 403)

    def assertNotFound(self, response):
        return self.assertStatusCode(response, 404)

    def get_example_data(self):
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
