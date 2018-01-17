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
from application.extensions import db, cache, moment, celery, mail
from application.filters import autoversion, current_route
from application.models import *  # noqa
from application.tasks import *  # noqa
from application.routes import bp


def create_app(config=None):
    app = Flask(__name__)

    configure(app, config)
    register_blueprints(app)
    register_filters(app)

    return app


def configure(app, config_name):
    app.config.from_object(config[config_name or 'default'])
    app.config.from_envvar('FLASK_CONFIG', silent=True)

    db.init_app(app)
    cache.init_app(app)
    moment.init_app(app)
    celery.init_app(app)
    mail.init_app(app)


def register_blueprints(app):
    """Register all blueprint modules"""
    app.register_blueprint(bp)


def register_filters(app):
    @app.template_filter('convert_ms')
    def convert_ms(ms, format='%B %d, %Y %I:%M%p'):
        sec = ms / 1000.0

        if os.name == 'nt':
            # Windows has a "minimum allowed" timestamp: https://stackoverflow.com/a/45372194
            sec = max(sec, 86400)

        return dt.fromtimestamp(sec).strftime(format)

    @app.template_filter('autoversion')
    def autoversion_filter(filename):
        return autoversion(filename)

    app.jinja_env.globals.update(current_route=current_route)
