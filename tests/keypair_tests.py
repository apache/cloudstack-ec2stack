#!/usr/bin/env python
# encoding: utf-8

import mock

from . import Ec2StackAppTestCase


class KeyPairTestCase(Ec2StackAppTestCase):
    def test_create_keypair(self):
        get = mock.Mock()
        text = get.return_value.text = '{ "createsshkeypairresponse" :  { "keypair" : {"name":"Test22","fingerprint":"f1:85:d8:d6:54:3c:3e:41:49:52:82:1b:a6:4e:7e:31","privateKey":"-----BEGIN RSA PRIVATE KEY-----\\nMIICWwIBAAKBgQCLFWb+Y+zxkDMSTmLu7XzOIFccIe6/TWG0BLA53xOPyoRTM4j0\\n1cGF2m4VSQ8QLOXztqO22O+zOU5eOtps5kZKk0IHpVGiTeNEfovogVnQx4A3qcC+\\nwKHFvjidlT6Cdy8av6erBS18W2NEtkipPEN1Kyirf5EDCz8gMcqRFxvIIQIDAQAB\\nAoGAK8Dy4qp62s97UZH5S6LIdWv1G3ONUP898kzbR4lm9QBHuojm1+b692ns4aNX\\nKsaFHLNjM11xotcvUTOAjWuvxsDaiE8wAxJI8Zv40QjJ3YO9zbrsbYoysXKJCVLx\\nEDB+HWaAb6gRprffuxu50py54RwTyXmhsuuIFcpKn07p32UCQQD42dCvq9p2Qu4Y\\nLuVn88kukc7wE3u/phLBaGGxAOEYvXH19rByKgzNYcKeZkrOrqbFEd7YiH/rsJz5\\nuY1Jh/OPAkEAjxRMiy5G3SbToC8IOEsLPY0USyOmx1Domd6HEGDOT7OIUoP9gsSr\\nuH23C73IzBFstxxhU+MkjZIY2dEY8ULxTwJAbNUl9Y5dTtdatezcm6f81ociT9DV\\nkC2bikaSYw0VZPKFgqLO7D8DtlcI/KmUEexEN2/nXB/mgjeNj5Hc/smcdQJATEfK\\nNznI1gbpNLFedIStzXb1psmvFPxxxfb5kyXJWHyi5TsxYRJxar67ZCsebo2rpEQh\\nL5Qd3MxTK21rGtVRyQJAM4HcYNW/VbH0SrhbtkLoHabjPkb3H0g05THq1ZTohWa0\\n1UckpzFX46gc2as+ooHGH0KsA7prUqI9AOmAwc28yw==\\n-----END RSA PRIVATE KEY-----\\n"} }  }'

        status_code = get.return_value.status_code = 200

        with mock.patch('requests.get', get):
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

            response = self.post(
                '/',
                data=data
            )

            print response.data

            self.assertOk(response)
