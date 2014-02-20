#!/usr/bin/env python
# encoding: utf-8

from factory import Factory

from ec2stack.models import *


def create_sql_model_function(class_to_create, *args, **kwargs):
    entity = class_to_create(**kwargs)
    DB.session.add(entity)
    DB.session.commit()
    return entity


Factory.set_creation_function(create_sql_model_function)


class UserFactory(Factory):
    FACTORY_FOR = User
    apikey = "ExampleAPIKey"
    secretkey = "ExampleSecretKey"
