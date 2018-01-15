# -*- coding: utf-8 -*-
"""
    config.py
    ~~~~~~~~~
    base application config
"""

import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'shhh_its_secret')

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'postgresql+psycopg2://localhost/boulderpython')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CELERY_BROKER_URL = os.environ.get('RABBITMQ_BIGWIG_URL', 'amqp://localhost//')
    CELERY_RESULT_BACKEND = os.environ.get('RABBITMQ_BIGWIG_URL', 'amqp://localhost//')

    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', None)
    SENDGRID_DEFAULT_FROM = 'Boulder Python <hi@boulderpython.org>'

    CACHE_TYPE = 'simple'
    GOOGLE_ANALYTICS_ID = 'UA-123456-78'

    MEETUP_KEY = os.environ.get('MEETUP_KEY', None)

    MAILCHIMP_USERNAME = os.environ.get('MAILCHIMP_USERNAME', None)
    MAILCHIMP_API_KEY = os.environ.get('MAILCHIMP_API_KEY', None)
    MAILCHIMP_LIST_ID = os.environ.get('MAILCHIMP_LIST_ID', None)

    TRELLO_API_KEY = os.environ.get('TRELLO_API_KEY', None)
    TRELLO_API_SECRET = os.environ.get('TRELLO_API_SECRET', None)
    TRELLO_TOKEN = os.environ.get('TRELLO_TOKEN', None)
    TRELLO_TOKEN_SECRET = os.environ.get('TRELLO_TOKEN_SECRET', None)
    TRELLO_ASSIGNEE = os.environ.get('TRELLO_ASSIGNEE', None)
    TRELLO_HOOK = os.environ.get('TRELLO_HOOK', 'https://boulderpython.ngrok.io/trello/hook')

    # this is public anyway (used in their URLs)
    TRELLO_BOARD = 'wm8hatnW'
    TRELLO_LIST = '5a0091836c98d9743f94b363'
    TRELLO_CARDS = {
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

    SSL_DISABLE = True
    MAIL_SERVER = 'smtp.sendgrid.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'sendgrid_username'
    MAIL_PASSWORD = 'sendgrid_password'
    MAIL_SUBJECT_PREFIX = '[site.com]'
    MAIL_SENDER = 'admin@site.com'
    SITE_ADMIN = os.environ.get('SITE_ADMIN', 'hi@boulderpython.com')

    @staticmethod
    def init_app(app):
        pass


class AppConfig(Config):
    """
    production config
    """
    @classmethod
    def init_app(cls, app):
        """
        config
        """
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.MAIL_SENDER,
            toaddrs=[cls.SITE_ADMIN],
            subject=cls.MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


config = {
    'production': AppConfig,
    'testing': AppConfig,
    'default': AppConfig
}
