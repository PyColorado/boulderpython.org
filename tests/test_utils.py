# -*- coding: utf-8 -*-
"""
    tests.utils
    ~~~~~~~~~~~~~~~~~

    tests for application utility functions
"""

import pytest

from tests.mocks.trello import MockTrelloClient
from application.utils import pluck


@pytest.mark.usefixtures("session")
class TestUtils:
    def test_trello_client(self, app, mocker):
        SubmissionsTrelloClient = mocker.patch("application.utils.SubmissionsTrelloClient", new=MockTrelloClient)
        client = SubmissionsTrelloClient()
        lst = client.board.get_list(1)
        assert lst["id"] == 1

    def test_pluck(self, *args, **kwargs):
        good_iterable = [{"name": "PyColorado"}, {"name": "DenverPython"}, {"name": "BoulderPython"}]
        assert pluck(good_iterable, lambda x: x["name"] == "BoulderPython") == good_iterable[-1]

        empty_iterable = []
        assert pluck(empty_iterable, lambda x: True) is None

        bad_iterable1 = None
        assert pluck(bad_iterable1, lambda x: True) is None

        bad_iterable2 = 5
        assert pluck(bad_iterable2, lambda x: True) is None
