# -*- coding: utf-8 -*-
"""
    tests.trello.py
    ~~~~~~~~~
    a Trello mock for testing
"""


class MockTrelloCard():
    id = 1
    url = 'http://mock.trello.com/card/1'

    def __init__(self):
        return


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

    def get_board(self, *arg, **kwrags):
        return MockTrelloBoard()
