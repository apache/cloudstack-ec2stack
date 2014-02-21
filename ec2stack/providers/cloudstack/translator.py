#!/usr/bin/env python
# encoding: utf-8

cloudstack_attributes_to_aws = {
    'id': 'id',
    'name': 'name',
    'state': 'state',
    'hypervisor': 'hypervisor',
    'displaytext': 'description',
    'zonename': 'availability_zone',
}


def cloudstack_item_to_aws(cloudstack_item, cloudstack_item_attributes_to_aws):
    item = {}

    attributes_to_aws_mapping = dict(cloudstack_attributes_to_aws.items() +
                                     cloudstack_item_attributes_to_aws.items())

    for cloudstack_attr, aws_attr in attributes_to_aws_mapping.iteritems():
        if cloudstack_attr in cloudstack_item:
            item[aws_attr] = cloudstack_item[cloudstack_attr]

    return item


def cloudstack_item_attribute_to_aws(
        cloudstack_item, cloudstack_item_attributes_to_aws, attribute):

    attributes_to_aws_mapping = dict(cloudstack_attributes_to_aws.items() +
                                     cloudstack_item_attributes_to_aws.items())

    item = {}

    if cloudstack_item[attribute] is not None:
        item[
            attributes_to_aws_mapping[attribute]
        ] = cloudstack_item[attribute]

    return item
