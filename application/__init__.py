# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~
    flask application entrypoint
"""
import os
import copy

import pytz
from flask import Flask
from flask_talisman import Talisman, GOOGLE_CSP_POLICY
import bugsnag.flask
import dotenv

dotenv.load_dotenv()
from config import config
from application.extensions import db, migrate, cache, moment, celery
from application.filters import autoversion, current_route, markdown
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
    selected_config = config[config_name or "default"]
    app.config.from_object(selected_config)
    app.config.from_envvar("FLASK_CONFIG", silent=True)

    db.init_app(app)
    migrate.init_app(app)
    cache.init_app(app)
    moment.init_app(app)
    celery.init_app(app)

    if app.config["SSL_ENABLE"]:
        # Force https
        csp = copy.deepcopy(GOOGLE_CSP_POLICY)
        csp["style-src"] += " 'unsafe-inline'"
        csp["style-src"] += " platform.twitter.com"
        csp["style-src"] += " *.twimg.com"
        csp["frame-src"] += " *.twitter.com"
        csp["script-src"] += " *.google.com"
        csp["script-src"] += " platform.twitter.com"
        csp["script-src"] += " cdnjs.cloudflare.com"
        csp["script-src"] += " cdn.syndication.twimg.com"
        csp["script-src"] += " *.gstatic.com"
        csp["script-src"] += " 'unsafe-inline' 'unsafe-eval'"
        csp["default-src"] += " *.google-analytics.com"
        csp["img-src"] = csp["default-src"]
        csp["img-src"] += " *.twitter.com"
        csp["img-src"] += " *.twimg.com"
        csp["img-src"] += " data:"

        Talisman(app, content_security_policy=csp)

    if app.config["BUGSNAG_API_KEY"]:
        # Configure Bugsnag
        bugsnag.configure(api_key=app.config["BUGSNAG_API_KEY"], auto_capture_sessions=True)

        bugsnag.flask.handle_exceptions(app)


def register_blueprints(app):
    """Register all blueprint modules"""
    app.register_blueprint(bp)


def register_filters(app):
    @app.template_filter("convert_ms")
    def convert_ms(ms, offset=0, format="%B %d, %Y %I:%M%p"):
        sec = ms / 1000.0

        if os.name == "nt":
            # Windows has a "minimum allowed" timestamp: https://stackoverflow.com/a/45372194
            sec = max(sec, 86400)

        timestamp = dt.fromtimestamp(sec, tz=pytz.UTC)

        if offset:
            offset_in_min = offset // 1000 // 60
            timestamp = timestamp.astimezone(pytz.FixedOffset(offset_in_min))

        return timestamp.strftime(format)

    @app.template_filter("autoversion")
    def autoversion_filter(filename):
        return autoversion(filename)

    @app.template_filter("markdown")
    def markdown_filter(value):
        return markdown(value)

    app.jinja_env.globals.update(current_route=current_route)
