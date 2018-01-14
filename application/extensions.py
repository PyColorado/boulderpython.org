# -*- coding: utf-8 -*-
"""
    extensions.py
    ~~~~~~~~~~~~~
    flask extension instatiations
"""

from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_caching import Cache


db = SQLAlchemy()
moment = Moment()
cache = Cache()
