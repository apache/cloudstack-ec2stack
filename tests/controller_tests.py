#!/usr/bin/env python
# encoding: utf-8

from . import Ec2StackAppTestCase


class ControllerTestCase(Ec2StackAppTestCase):
    data = {
        'SignatureVersion': '2',
        'AWSAccessKeyId': 'ExampleAPIKey',
        'Version': '2013-10-15',
        'Timestamp': '2014-02-19T23:34:43.868347',
        'SignatureMethod': 'HmacSHA256',
        'KeyName': 'Test',
        'Signature': 'eXLhkDN95Qf5uYmBNm1kixVT/yEHjgVsnyBxtKO8cig=',
        'Action': 'CreateKeyPair'
    }

    def test_invalid_action(self):
        response = self.post(
            '/',
            data={}
        )

        self.assertBadRequest(response)

        assert 'InvalidAction' in response.data

    def test_authentication_required_parameters(self):
        data = self.data.copy()

        for key in data.iterkeys():
            if key not in ['Action', 'KeyName']:
                self._test_authentication_required_helper(key, data)

    def _test_authentication_required_helper(self, item, data):
        value = data.pop(item)
        response = self.post(
            '/',
            data=data
        )

        self.assertBadRequest(response)

        assert 'The request must contain the parameter ' + item \
            in response.data

        data[item] = value

    def test_invalid_signature_version(self):
        data = self.data.copy()
        data['SignatureVersion'] = '20'

        response = self.post(
            '/',
            data=data
        )

        self.assertBadRequest(response)

        assert 'SignatureVersion is invalid' in response.data

    def test_invalid_signature_method(self):
        data = self.data.copy()
        data['SignatureMethod'] = 'InvalidHmac'

        response = self.post(
            '/',
            data=data
        )

        self.assertBadRequest(response)

        assert 'SignatureMethod is invalid' in response.data

    def test_failure_to_find_secretkey(self):
        data = self.data.copy()
        data['AWSAccessKeyId'] = 'InvalidAWSAccessKeyId'
        response = self.post(
            '/',
            data=data
        )

        self.assertStatusCode(response, 401)

        assert 'Unable to find a secret key' in response.data

    def test_invalid_signature(self):
        data = self.data.copy()
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
        assert 'ExampleAPIKey2' in response.data
        assert 'ExampleSecretKey2' in response.data

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
        assert 'The given AWSAccessKeyId was not found' in response.data
