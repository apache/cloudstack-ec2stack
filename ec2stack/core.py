#!/usr/bin/env python
# encoding: utf-8
#
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.
#

"""This module provides core classes.
"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class Ec2stackError(Exception):

    def __init__(self, code, error, message):
        self.code = code
        self.error = error
        self.message = message


class Service(object):
    __model__ = None

    def _isinstance(self, model, raise_error=True):
        """
        Checks if the given model is an instance of the service.

        @param model: Model to be checked.
        @param raise_error: ValueError if model isn't the correct type.
        @return: Bool @raise ValueError: stating not of correct type.
        """
        valid_type = isinstance(model, self.__model__)
        if not valid_type and raise_error:
            raise ValueError('%s is not of type %s' % (model, self.__model__))
        return valid_type

    def save(self, model):
        """
        Saves the given Model.

        @param model: The model to be saved.
        @return: The saved model.
        """
        self._isinstance(model)
        DB.session.add(model)
        DB.session.commit()
        return model

    def get(self, primarykey):
        """
        Get the model via primarykey.

        @param primarykey: primarykey of the model you want.
        @return: Found model.
        """
        return self.__model__.query.get(primarykey)

    def create(self, **kwargs):
        """
        Creates a new object.

        @param kwargs: Parameters for the model.
        @return: Created model.
        """
        return self.save(self.__model__(**kwargs))

    def delete(self, model):
        """
        Deletes the given model.

        @param model: Model to be deleted.
        """
        self._isinstance(model)
        DB.session.delete(model)
        DB.session.commit()
