# -*- coding: utf-8 -*-
"""
    tests.trello.py
    ~~~~~~~~~
    a Trello mock for testing
"""
from flask import current_app as app


class MockTrelloCard():
    id = 1
    url = 'http://mock.trello.com/card/1'

    def __init__(self):
        return


class MockTrelloLabel():
    def __init__(self, _id, name, *args, **kwargs):
        self.id = _id
        self.name = name


class MockTrelloList():
    id = None

    def __init__(self, _id, *args, **kwargs):
        self.id = _id
        return

    def __getitem__(self, x):
        return getattr(self, x)

    def add_card(self, *args, **kwargs):
        return MockTrelloCard

    def __repr__(self):
        return {'id': self._id}


class MockTrelloBoard():
    def __init__(self, *args, **kwargs):
        return

    def get_list(self, _id, *args, **kwargs):
        return MockTrelloList(_id)


class MockTrelloClient():
    def __init__(self, *args, **kwargs):
        return

    @property
    def board(self):
        return self.get_board(1)

    def get_board(self, board_id):
        return MockTrelloBoard()

    @property
    def new_submissions_list(self):
        return self.board.get_list(1)

    @property
    def labels(self):
        label_idx = 0
        labels = {}

        for label_group in app.config['DEFAULT_TRELLO_LABELS'].values():
            for label_name in label_group:
                labels[label_name] = label_idx
                label_idx += 1

        return labels
