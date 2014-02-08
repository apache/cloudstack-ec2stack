#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, render_template


IMAGES = Blueprint('images', __name__)


def describe():
    return render_template("describe_images.xml")
