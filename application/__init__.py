# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~
    flask application entrypoint
"""

import os
from datetime import datetime as dt

from flask import Flask

from config import config
# from .utils import configure
from .extensions import db, cache, moment
from .filters import autoversion, current_route


app = Flask(__name__)


def configure(config_name='default'):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    if os.environ.get('APP_CONFIG'):
        app.config.from_envvar('APP_CONFIG')

configure()
db.init_app(app)
cache.init_app(app)
moment.init_app(app)


@app.template_filter('convert_ms')
def convert_ms(ms, format='%B %d, %Y %-I:%M%p'):
    return dt.fromtimestamp(ms / 1000.00).strftime(format)


@app.template_filter('autoversion')
def autoversion_filter(filename):
    return autoversion(filename)


app.jinja_env.globals.update(current_route=current_route)


from .routes import *  # noqa
from .models import *  # noqa
