#!/usr/bin/env python
# encoding: utf-8

from . import Ec2StackAppTestCase

from ec2stack.helpers import generate_signature, read_file

import mock

class ControllerTestCase(Ec2StackAppTestCase):
    def test_invalid_action(self):
        data = self.get_example_data()
        data['Action'] = 'InvalidAction'

        response = self.post(
            '/',
            data={}
        )

        self.assertBadRequest(response)
        assert 'not valid for this web service' in response.data

    def test_authentication_required_parameters(self):
        data = self.get_example_data()

        for key in data.iterkeys():
            self._test_authentication_required_helper(key, data)

    def _test_authentication_required_helper(self, item, data):
        value = data.pop(item)
        response = self.post(
            '/',
            data=data
        )

        self.assertBadRequest(response)
        data[item] = value

    def test_invalid_signature_version(self):
        data = self.get_example_data()
        data['SignatureVersion'] = '20'

        response = self.post(
            '/',
            data=data
        )

        self.assertBadRequest(response)
        assert 'SignatureVersion is invalid' in response.data

    def test_invalid_signature_method(self):
        data = self.get_example_data()
        data['SignatureMethod'] = 'InvalidHmac'

        response = self.post(
            '/',
            data=data
        )

        self.assertBadRequest(response)
        assert 'SignatureMethod is invalid' in response.data

    def test_failure_to_find_secretkey(self):
        data = self.get_example_data()
        data['AWSAccessKeyId'] = 'InvalidAWSAccessKeyId'
        response = self.post(
            '/',
            data=data
        )

        self.assertStatusCode(response, 401)
        assert 'Unable to find a secret key' in response.data

    def test_invalid_signature(self):
        data = self.get_example_data()
        data['Signature'] = 'InvalidSignature'
        response = self.post(
            '/',
            data=data
        )

        self.assertStatusCode(response, 401)

        assert 'AWS was not able to validate the provided access credentials.' \
            in response.data

    def test_duplicate_register_secretkey(self):
        data = {
            'Action': 'RegisterSecretKey',
            'AWSAccessKeyId': 'ExampleAPIKey',
            'AWSSecretKey': 'ExampleSecretKey'
        }

        response = self.post(
            '/',
            data=data
        )

        self.assertBadRequest(response)

        assert 'The given AWSAccessKeyId is already registered' \
            in response.data

    def test_successful_register_secretkey(self):
        data = {
            'Action': 'RegisterSecretKey',
            'AWSAccessKeyId': 'ExampleAPIKey2',
            'AWSSecretKey': 'ExampleSecretKey2'
        }

        response = self.post(
            '/',
            data=data
        )

        self.assertOk(response)

        assert 'RegisterSecretKeyResponse' in response.data

    def test_successful_delete_secretkey(self):
        data = {
            'Action': 'RemoveSecretKey',
            'AWSAccessKeyId': 'ExampleAPIKey',
            'AWSSecretKey': 'ExampleSecretKey'
        }

        response = self.post(
            '/',
            data=data
        )

        self.assertOk(response)
        assert 'RemoveSecretKeyResponse' in response.data

    def test_not_found_delete_secretkey(self):
        data = {
            'Action': 'RemoveSecretKey',
            'AWSAccessKeyId': 'NonExistingExampleAPIKey',
            'AWSSecretKey': 'NonExistingExampleSecretKey'
        }

        response = self.post(
            '/',
            data=data
        )

        self.assertBadRequest(response)
        assert 'The no matching AWSAccessKeyId' in response.data

    def test_not_found(self):
        response = self.post(
            '/example-not-found-url',
        )

        self.assertNotFound(response)

    def test_bad_request_on_provider_error(self):
        data = self.get_example_data()
        data['Action'] = 'CreateKeyPair'
        data['KeyName'] = 'Test'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        get = mock.Mock()
        status_code = get.return_value.status_code = 401

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assertBadRequest(response)
