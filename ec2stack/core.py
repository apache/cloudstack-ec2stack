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
        valid_type = isinstance(model, self.__model__)
        if not valid_type and raise_error:
            raise ValueError('%s is not of type %s' % (model, self.__model__))
        return valid_type

    def save(self, model):
        self._isinstance(model)
        DB.session.add(model)
        DB.session.commit()
        return model

    def get(self, primarykey):
        return self.__model__.query.get(primarykey)

    def find(self, **kwargs):
        return self.__model__.query.filter_by(**kwargs)

    def first(self, **kwargs):
        return self.find(**kwargs).first()

    def create(self, **kwargs):
        return self.save(self.__model__(**kwargs))

    def delete(self, model):
        self._isinstance(model)
        DB.session.delete(model)
        DB.session.commit()
