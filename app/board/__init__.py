#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Blueprint

board_blueprint = Blueprint('board', __name__)

from . import views
