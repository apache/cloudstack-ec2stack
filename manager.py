#!/usr/bin/env python
# encoding: utf-8

from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager

from ec2stack import create_app
from ec2stack.core import DB


APP = create_app()

MIGRATE = Migrate(APP, DB)
MANAGER = Manager(APP)
MANAGER.add_command('db', MigrateCommand)

if __name__ == "__main__":
    MANAGER.run()
