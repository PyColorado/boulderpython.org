# -*- coding: utf-8 -*-
"""
    tests.utils
    ~~~~~~~~~~~~~~~~~

    tests for application utility functions
"""

import pytest

from application.utils import TrelloClient, pluck


class MockTrelloBoard():
    def __init__(self, *args, **kwargs):
        return

    def get_list(self, _id, *args, **kwargs):
        return {'id': _id}


class MockTrelloClient():
    def __init__(self, *args, **kwargs):
        return

    def get_board(self, *arg, **kwrags):
        return MockTrelloBoard()


@pytest.mark.usefixtures('session')
class TestUtils:

    def setup_method(self):
        self.config = {
            'TRELLO_API_KEY': '',
            'TRELLO_API_SECRET': '',
            'TRELLO_TOKEN': '',
            'TRELLO_TOKEN_SECRET': '',
            'TRELLO_BOARD': '1',
            'TRELLO_LISTS': {'NEW': {'id': 1}}
        }

    def test_trello_client(self, app, mocker):
        app.config.update(self.config)
        mocker.patch('application.utils.Trello', new=MockTrelloClient)
        client, lst = TrelloClient()
        assert lst['id'] == 1

    def test_pluck(self, *args, **kwargs):
        good_iterable = [
            {'name': 'PyColorado'},
            {'name': 'DenverPython'},
            {'name': 'BoulderPython'}
        ]
        assert pluck(good_iterable, lambda x: x['name'] == 'BoulderPython') == good_iterable[-1]

        empty_iterable = []
        assert pluck(empty_iterable, lambda x: True) is None

        bad_iterable1 = None
        assert pluck(bad_iterable1, lambda x: True) is None

        bad_iterable2 = 5
        assert pluck(bad_iterable2, lambda x: True) is None

