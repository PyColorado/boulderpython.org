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


def TrelloClient():
    '''Return an instance of the Trello client and the new submissions list

    Returns:
        TrelloClient:   an instance of the Trello API client
        TrelloList:     the new submissions list from our Trello board
    '''
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
