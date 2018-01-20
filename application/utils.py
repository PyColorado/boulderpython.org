# -*- coding: utf-8 -*-
"""
    utils.py
    ~~~~~~~~
    utility function
"""
import collections

from flask import current_app as app
from trello import TrelloClient as Trello


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
        newSubmissionsList = board.get_list(app.config['TRELLO_LISTS']['NEW']['id'])

        return client, newSubmissionsList


def pluck(iterable, test_fn):
    """ Return the first value from iterable that passes test_fn.

    :param iterable: Any valid Python iterable, including lists of dicts/objects
    :param test_fn: Lambda or other test function that receives a list entry as its only parameter.
    :return: First matching list entry or None if no matching entry is found.
    """
    if not isinstance(iterable, collections.Iterable):
        return None

    for item in iterable:
        if test_fn(item):
            return item

    return None
