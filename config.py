# -*- coding: utf-8 -*-
"""
    config.py
    ~~~~~~~~~
    base application config
"""

import os, pathlib


class BaseConfig:
    SITE_NAME = os.environ.get('SITE_NAME', 'boulderpython.org')
    SITE_ADMIN = os.environ.get('SITE_ADMIN', 'hi@boulderpython.com')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'shhh_its_secret')

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'postgresql+psycopg2://localhost/boulderpython')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CELERY_BROKER_URL = os.environ.get('RABBITMQ_BIGWIG_URL', 'amqp://localhost//')
    CELERY_RESULT_BACKEND = os.environ.get('RABBITMQ_BIGWIG_URL', 'rpc')

    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', None)
    SENDGRID_DEFAULT_FROM = 'Boulder Python <hi@boulderpython.org>'

    MEETUP_KEY = os.environ.get('MEETUP_KEY', None)
    MEETUP_GROUP = os.environ.get('MEETUP_GROUP', 'BoulderPython')

    MAILCHIMP_USERNAME = os.environ.get('MAILCHIMP_USERNAME', None)
    MAILCHIMP_API_KEY = os.environ.get('MAILCHIMP_API_KEY', None)
    MAILCHIMP_LIST_ID = os.environ.get('MAILCHIMP_LIST_ID', None)

    TRELLO_API_KEY = os.environ.get('TRELLO_API_KEY', None)
    TRELLO_API_SECRET = os.environ.get('TRELLO_API_SECRET', None)
    TRELLO_TOKEN = os.environ.get('TRELLO_TOKEN', None)
    TRELLO_TOKEN_SECRET = os.environ.get('TRELLO_TOKEN_SECRET', None)
    TRELLO_ASSIGNEE = os.environ.get('TRELLO_ASSIGNEE', None)
    TRELLO_HOOK = os.environ.get('TRELLO_HOOK', 'https://www.boulderpython.org/trello/hook')

    # this is public anyway (used in their URLs)
    TRELLO_BOARD = 'wm8hatnW'
    TRELLO_LISTS = {
        'NEW': {
            "id": "5a0091836c98d9743f94b363",
            "text": "New"
        },
        'REVIEW': {
            "id": "5a0091836c98d9743f94b364",
            "text": "In Review"
        },
        'SCHEDULED': {
            "id": "5a0091836c98d9743f94b365",
            "text": "Scheduled"
        },
        'HOWDOESTHISWORK': {
            "id": "5a932e60fdfdd4f02fa345b8",
            "text": "How Does this Work?"
        }
    }

    TRELLO_LABELS = {
        "FORMAT": {
            "IN-DEPTH": "5a0094fca8e476f047706616",
            "LIGHTNING": "5a00950b73846ef08844501e",
            "DEMO": "5a0095201f007932c3ea53d0",
            "BEGINNER": "5a0095307b5c511544f1447b"
        },
        "AUDIENCE": {
            "BEGINNER": "5a0091839ae3d60b0c9e04af",
            "INTERMEDIATE": "5a0091839ae3d60b0c9e04b1",
            "ADVANCED": "5a0091839ae3d60b0c9e04b0"
        }
    }


class DefaultConfig(BaseConfig):
    DEBUG = os.environ.get('DEBUG', True)

    CACHE_TYPE = 'simple'

    GOOGLE_ANALYTICS_ID = os.environ.get('GOOGLE_ANALYTICS_ID', 'UA-123456-78')

    SSL_DISABLE = True
    MAIL_SERVER = 'smtp.sendgrid.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'sendgrid_username'
    MAIL_PASSWORD = 'sendgrid_password'
    MAIL_SUBJECT_PREFIX = '[site.com]'
    MAIL_SENDER = 'admin@site.com'


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True

    TEST_DB_PATH = os.path.join(pathlib.Path(__file__).parent, 'tests/')
    TEST_DB_FILENAME = 'test.db'
    TEST_DB = TEST_DB_PATH + TEST_DB_FILENAME
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{TEST_DB}'

    WTF_CSRF_ENABLED = False

    CELERY_TASK_ALWAYS_EAGER = True

    CACHE_TYPE = 'null'

    TRELLO_BOARD = '1'
    TRELLO_LISTS = {
        'NEW': {
            "id": 1,
            "text": "New"
        }
    }


config = {
    'default': DefaultConfig,
    'production': DefaultConfig,
    'testing': TestConfig
}
