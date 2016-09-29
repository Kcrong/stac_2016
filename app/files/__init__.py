#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Blueprint

file_blueprint = Blueprint('file', __name__)

from . import views
