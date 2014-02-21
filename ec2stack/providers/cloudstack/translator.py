#!/usr/bin/env python
# encoding: utf-8

cloudstack_attributes_to_aws = {
    'id': 'id',
    'name': 'name',
    'state': 'state',
    'hypervisor': 'hypervisor',
    'displaytext': 'description',
    'zonename': 'availability_zone',
    'displaytext': 'description',
}

def cloudstack_item_to_aws(cloudstack_item, cloudstack_item_attributes_to_aws):
    item = {}

    '''

        Add general cloudstack attributes map to cloudstack attributes map 
        specific to item (passed in as arg)

        If there is a duplicate the second dictionary takes preference and
        ovverrides the first dictionaries value

    '''

    attributes_to_aws_mapping = dict(cloudstack_attributes_to_aws.items() + 
            cloudstack_item_attributes_to_aws.items())
 
    for cloudstack_attr, aws_attr in attributes_to_aws_mapping.iteritems():
        if cloudstack_attr in cloudstack_item:
            item[aws_attr] = cloudstack_item[cloudstack_attr]


    return item


def cloudstack_item_attribute_to_aws(attribute):
    item = {}

    if response[attribute] is not None:
        item[
            cloudstack_attributes_to_aws[attribute]
        ] = response[attribute]
        item['id'] = item['id']

    return item
