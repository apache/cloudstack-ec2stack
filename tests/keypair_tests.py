#!/usr/bin/env python
# encoding: utf-8

from base64 import b64encode

import mock

from . import Ec2StackAppTestCase


class KeyPairTestCase(Ec2StackAppTestCase):
    data = {
        'SignatureVersion': '2',
        'AWSAccessKeyId': 'ExampleAPIKey',
        'Version': '2013-10-15',
        'Timestamp': '2014-02-19T23:34:43.868347',
        'SignatureMethod': 'HmacSHA256',
        'KeyName': 'Test',
    }

    def test_create_keypair(self):
        data = self.data.copy()
        data['Action'] = 'CreateKeyPair'
        data['Signature'] = 'eXLhkDN95Qf5uYmBNm1kixVT/yEHjgVsnyBxtKO8cig='

        get = mock.Mock()
        text = get.return_value.text = '{ "createsshkeypairresponse" :  { "keypair" : {"name":"Test","fingerprint":"f1:85:d8:d6:54:3c:3e:41:49:52:82:1b:a6:4e:7e:31","privateKey":"-----BEGIN RSA PRIVATE KEY-----\\nMIICWwIBAAKBgQCLFWb+Y+zxkDMSTmLu7XzOIFccIe6/TWG0BLA53xOPyoRTM4j0\\n1cGF2m4VSQ8QLOXztqO22O+zOU5eOtps5kZKk0IHpVGiTeNEfovogVnQx4A3qcC+\\nwKHFvjidlT6Cdy8av6erBS18W2NEtkipPEN1Kyirf5EDCz8gMcqRFxvIIQIDAQAB\\nAoGAK8Dy4qp62s97UZH5S6LIdWv1G3ONUP898kzbR4lm9QBHuojm1+b692ns4aNX\\nKsaFHLNjM11xotcvUTOAjWuvxsDaiE8wAxJI8Zv40QjJ3YO9zbrsbYoysXKJCVLx\\nEDB+HWaAb6gRprffuxu50py54RwTyXmhsuuIFcpKn07p32UCQQD42dCvq9p2Qu4Y\\nLuVn88kukc7wE3u/phLBaGGxAOEYvXH19rByKgzNYcKeZkrOrqbFEd7YiH/rsJz5\\nuY1Jh/OPAkEAjxRMiy5G3SbToC8IOEsLPY0USyOmx1Domd6HEGDOT7OIUoP9gsSr\\nuH23C73IzBFstxxhU+MkjZIY2dEY8ULxTwJAbNUl9Y5dTtdatezcm6f81ociT9DV\\nkC2bikaSYw0VZPKFgqLO7D8DtlcI/KmUEexEN2/nXB/mgjeNj5Hc/smcdQJATEfK\\nNznI1gbpNLFedIStzXb1psmvFPxxxfb5kyXJWHyi5TsxYRJxar67ZCsebo2rpEQh\\nL5Qd3MxTK21rGtVRyQJAM4HcYNW/VbH0SrhbtkLoHabjPkb3H0g05THq1ZTohWa0\\n1UckpzFX46gc2as+ooHGH0KsA7prUqI9AOmAwc28yw==\\n-----END RSA PRIVATE KEY-----\\n"} }  }'
        status_code = get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assertOk(response)
        assert 'CreateKeyPairResponse' in response.data

    def test_duplicate_keypair(self):
        data = self.data.copy()
        data['Action'] = 'CreateKeyPair'
        data['Signature'] = 'eXLhkDN95Qf5uYmBNm1kixVT/yEHjgVsnyBxtKO8cig='

        get = mock.Mock()
        text = get.return_value.text = '{ "createsshkeypairresponse" : {"uuidList":[],"errorcode":431,"errortext":"A key pair with name \'Test\' already exists."} }'
        status_code = get.return_value.status_code = 431

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assertBadRequest(response)
        assert 'InvalidKeyPair.Duplicate' in response.data

    def test_delete_keypair(self):
        data = self.data.copy()
        data['Action'] = 'DeleteKeyPair'
        data['Signature'] = 'gCzuMB+xqD+yV3+vcQqKknpG6ohBPUGuuz1cl9c2gDk='

        get = mock.Mock()
        text = get.return_value.text = '{ "deletesshkeypairresponse" : { "success" : "true"}  }'
        status_code = get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assertOk(response)
        assert 'DeleteKeyPairResponse' in response.data

    def test_import_keypair(self):
        data = self.data.copy()
        data['Action'] = 'ImportKeyPair'
        data['PublicKeyMaterial'] = b64encode(
            'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCaqPfl99phOoszUD6n9xNKUtjqofhktvGxuhT2BgiTNi55FNfHAPyXyakQ86NbZPEQoRiDGyOI6BQVOmd+811Z+tFpB8EsY9t7tFAohid6G6bn7/Z78beXXMk9lcc7bnCVZaeZmAjHSTBHinlcWqB3P5IPJTASVektX8drPXXyTCEp5NlJdSTmfnQJAm9Ho5YMlHGAMyW8aIBKBrpwjx6RAYnPcIWm0JsvoSrPTeM9koziSRBROG06UT3FSslwuetcQvHsvIPHJ1IrwHljXQomOf7GLgSzbp6CzvlY6Leh9OQOcv70dYy5RcoEoVh+Lta5LpyiUL/ntW270M29lxpB')
        data['Signature'] = 'SY0RrsIDp4dXCl5Z2lF8imy+3sXDQrO49pHDOGQkmKs='

        get = mock.Mock()
        text = get.return_value.text = '{ "registersshkeypairresponse" :  { "keypair" : {"name":"Test22","fingerprint":"07:69:0e:64:f1:b5:f8:c1:10:25:55:73:1a:5c:39:1d"} }  }'
        status_code = get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assertOk(response)
        assert 'ImportKeyPairResponse' in response.data
