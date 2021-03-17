# -*- coding: utf-8 -*-
"""
    config.py
    ~~~~~~~~~
    base application config
"""

import os, pathlib
from uuid import uuid4


class BaseConfig:
    SITE_NAME = os.environ.get("SITE_NAME", "boulderpython.org")
    SITE_ADMIN = os.environ.get("SITE_ADMIN", "hi@boulderpython.com")
    SECRET_KEY = os.environ.get("SECRET_KEY", "shhh_its_secret")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql+psycopg2://localhost/boulderpython")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CELERY_BROKER_URL = os.environ.get("CLOUDAMQP_URL", "amqp://localhost//")
    CELERY_RESULT_BACKEND = os.environ.get("CLOUDAMQP_URL", "rpc")

    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", None)
    SENDGRID_DEFAULT_FROM = "Boulder Python <hi@boulderpython.org>"

    MEETUP_GROUP = os.environ.get("MEETUP_GROUP", "BoulderPython")

    MAILCHIMP_USERNAME = os.environ.get("MAILCHIMP_USERNAME", None)
    MAILCHIMP_API_KEY = os.environ.get("MAILCHIMP_API_KEY", None)
    MAILCHIMP_LIST_ID = os.environ.get("MAILCHIMP_LIST_ID", None)

    BUGSNAG_API_KEY = os.environ.get("BUGSNAG_API_KEY", None)

    TRELLO_API_KEY = os.environ.get("TRELLO_API_KEY", None)
    TRELLO_API_TOKEN = os.environ.get("TRELLO_API_TOKEN", None)

    TRELLO_ASSIGNEE = os.environ.get("TRELLO_ASSIGNEE", None)
    TRELLO_HOOK = os.environ.get("TRELLO_HOOK", "https://www.boulderpython.org/trello/hook")

    # These parameters were added begrudgingly to gain access to the Trello card emails using
    # browser emulation.  See tasks.extract_card_email
    TRELLO_USERNAME = os.environ.get("TRELLO_USERNAME", "hi@boulderpython.org")
    TRELLO_PASSWORD = os.environ.get("TRELLO_PASSWORD", None)

    # this is public anyway (used in their URLs)
    TRELLO_BOARD = "wm8hatnW"

    # Order is important here!!  When initializing a new board, lists will be arranged according
    # to the order they're listed here.
    DEFAULT_TRELLO_LISTS = [
        {"name": "HOWDOESTHISWORK", "default_caption": "How Does this Work?"},
        {"name": "NEW", "default_caption": "New"},
        {"name": "REVIEW", "default_caption": "In Review"},
        {"name": "SCHEDULED", "default_caption": "Scheduled"},
    ]

    DEFAULT_TRELLO_LABELS = {
        "FORMAT": {
            "IN-DEPTH": {"default_color": "blue", "default_caption": "In Depth (20-30 minutes)"},
            "LIGHTNING": {"default_color": "sky", "default_caption": "Lightning Talk (5-10 minutes)"},
            "DEMO": {"default_color": "lime", "default_caption": "Short Demo (15-20 minutes)"},
            "BEGINNER": {"default_color": "pink", "default_caption": "Beginner Track (20 minutes)"},
        },
        "AUDIENCE": {
            "BEGINNER": {"default_color": "green", "default_caption": "Beginner"},
            "INTERMEDIATE": {"default_color": "yellow", "default_caption": "Intermediate"},
            "ADVANCED": {"default_color": "red", "default_caption": "Advanced"},
        },
    }


class DefaultConfig(BaseConfig):
    DEBUG = os.environ.get("DEBUG", "true").lower() == "true"

    CACHE_TYPE = "simple"

    GOOGLE_ANALYTICS_ID = os.environ.get("GOOGLE_ANALYTICS_ID", "UA-123456-78")

    SSL_ENABLE = True
    MAIL_SERVER = "smtp.sendgrid.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "sendgrid_username"
    MAIL_PASSWORD = "sendgrid_password"
    MAIL_SUBJECT_PREFIX = "[site.com]"
    MAIL_SENDER = "admin@site.com"


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True

    SSL_ENABLE = False
    TEST_DB_PATH = os.path.join(pathlib.Path(__file__).parent, "tests/")
    TEST_DB_FILENAME = "test.db"
    TEST_DB = TEST_DB_PATH + TEST_DB_FILENAME
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{TEST_DB}"

    WTF_CSRF_ENABLED = False

    CELERY_TASK_ALWAYS_EAGER = True

    CACHE_TYPE = "null"

    TRELLO_BOARD = "1"
    TRELLO_LISTS = {"NEW": {"id": 1, "text": "New"}}


config = {"default": DefaultConfig, "production": DefaultConfig, "testing": TestConfig}
