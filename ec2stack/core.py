#!/usr/bin/env python
# encoding: utf-8

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

        @param model:
        @param raise_error:
        @return: @raise ValueError:
        """
        valid_type = isinstance(model, self.__model__)
        if not valid_type and raise_error:
            raise ValueError('%s is not of type %s' % (model, self.__model__))
        return valid_type

    def save(self, model):
        """

        @param model:
        @return:
        """
        self._isinstance(model)
        DB.session.add(model)
        DB.session.commit()
        return model

    def get(self, primarykey):
        """

        @param primarykey:
        @return:
        """
        return self.__model__.query.get(primarykey)

    def create(self, **kwargs):
        """

        @param kwargs:
        @return:
        """
        return self.save(self.__model__(**kwargs))

    def delete(self, model):
        """

        @param model:
        """
        self._isinstance(model)
        DB.session.delete(model)
        DB.session.commit()
