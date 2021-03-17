# -*- coding: utf-8 -*-
"""
    utils.py
    ~~~~~~~~
    utility function
"""
import collections
import functools

from flask import current_app as app

from application import TrelloList
from trello import TrelloClient as Trello


class SubmissionsTrelloClient(Trello):
    """Wrap the base Trello client with one that understands the business logic of the Submissions
    app."""

    def __init__(self):
        with app.app_context():
            super().__init__(
                api_key=app.config["TRELLO_API_KEY"],
                token=app.config["TRELLO_API_TOKEN"],
            )

    @property
    @functools.lru_cache()
    def board(self):
        with app.app_context():
            return self.get_board(app.config["TRELLO_BOARD"])

    @property
    @functools.lru_cache()
    def new_submissions_list(self):
        list_id = TrelloList().first(list_symbolic_name="NEW").list_id
        return self.board.get_list(list_id)

    @property
    @functools.lru_cache()
    def labels(self):

        with app.app_context():
            # Build a map of known label captions to common label names
            known_label_captions = {
                options["default_caption"]: common_name
                for label_group in app.config["DEFAULT_TRELLO_LABELS"].values()
                for common_name, options in label_group.items()
            }

        # Iterate over the Trello labels, matching them by caption, and mapping common label name
        # to Trello label ID
        labels_by_common_name = {}

        for trello_label in self.board.get_labels():
            common_name = known_label_captions.get(trello_label.name, None)

            if common_name:
                labels_by_common_name[common_name] = trello_label.id

        return labels_by_common_name


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
