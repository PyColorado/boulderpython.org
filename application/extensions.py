# -*- coding: utf-8 -*-
"""
    extensions.py
    ~~~~~~~~~~~~~
    flask extension instatiations
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_caching import Cache
from flask_celery import Celery

# from flask_sendgrid import SendGrid


db = SQLAlchemy()
migrate = Migrate(db=db)
moment = Moment()
cache = Cache()
celery = Celery()
# mail = SendGrid()
