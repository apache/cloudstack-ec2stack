#!/usr/bin/env python
# encoding: utf-8

from . import Ec2StackAppTestCase

class ControllerTestCase(Ec2StackAppTestCase):
    def test_invalid_action(self):
        response = self.post(
            '/',
            data  = {}
        )
        assert 'InvalidAction' in response.data

    def test_authentication_required_parameters(self):
        data = {
            'Action': 'CreateKeyPair',
            'AWSAccessKeyId': 'ExampleAPIKey',
            'Signature': '7puh9l03gKeTGmIpZwlKaFzSnW68fBFTKeT83HLINkE=',
            'SignatureMethod': 'HmacSHA256',
            'SignatureVersion': '2',
            'Timestamp': '2014-02-19T18:04:06.029852',
            'Version': '2013-10-15'
        }

        for key in data.iterkeys():
            if key != 'Action':
                self._test_authentication_required_helper(key, data)

    def _test_authentication_required_helper(self, item, data):
        value = data.pop(item)
        response = self.post(
            '/',
            data = data
        )

        assert 'The request must contain the parameter ' + item  \
            in response.data

        data[item] = value
