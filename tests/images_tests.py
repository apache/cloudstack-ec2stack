#!/usr/bin/env python
# encoding: utf-8

import mock

from ec2stack.helpers import read_file, generate_signature
from . import Ec2StackAppTestCase


class ImagesTestCase(Ec2StackAppTestCase):
    def test_describe_images(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeImages'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        get = mock.Mock()
        text = get.return_value.text = read_file(
            'tests/data/valid_describe_images.json'
        )
        status_code = get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assertOk(response)
        assert 'DescribeImagesResponse' in response.data

    def test_describe_specific_images(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeImages'
        data['ImageId.1'] = 'a32d70ee-95e4-11e3-b2e4-d19c9d3e5e1d'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        get = mock.Mock()
        text = get.return_value.text = read_file(
            'tests/data/valid_describe_images.json'
        )
        status_code = get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        self.assertOk(response)
        assert 'DescribeImagesResponse' in response.data


    def test_describe_image_attribute(self):
        data = self.get_example_data()
        data['Action'] = 'DescribeImageAttribute'
        data['ImageId'] = 'a32d70ee-95e4-11e3-b2e4-d19c9d3e5e1d'
        data['Attribute'] = 'isready'
        data['Signature'] = generate_signature(data, 'POST', 'localhost')

        get = mock.Mock()
        text = get.return_value.text = read_file(
            'tests/data/valid_describe_image_attribute.json'
        )
        status_code = get.return_value.status_code = 200

        with mock.patch('requests.get', get):
            response = self.post(
                '/',
                data=data
            )

        print response.data

        self.assertOk(response)
        assert 'DescribeImageAttributeResponse' in response.data
