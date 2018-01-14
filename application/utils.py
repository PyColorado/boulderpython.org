# -*- coding: utf-8 -*-
"""
    utils.py
    ~~~~~~~~
    utility function
"""

import os

from flask import current_app as app
from trello import TrelloClient as Trello

from config import config


def configure(app, config_name='default'):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    if os.environ.get('APP_CONFIG'):
        app.config.from_envvar('APP_CONFIG')


def TrelloClient():
    """return an instance of the Trello client and the new submissions list"""
    with app.app_context():
        client = Trello(
            api_key=app.config['TRELLO_API_KEY'],
            api_secret=app.config['TRELLO_API_SECRET'],
            token=app.config['TRELLO_TOKEN'],
            token_secret=app.config['TRELLO_TOKEN_SECRET']
        )

        board = client.get_board(app.config['TRELLO_BOARD'])
        newSubmissionsList = board.get_list(app.config['TRELLO_LIST'])

        return client, newSubmissionsList
