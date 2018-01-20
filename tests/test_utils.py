# -*- coding: utf-8 -*-
"""
    tests.utils
    ~~~~~~~~~~~~~~~~~

    tests for application utility functions
"""

import pytest

from application.utils import TrelloClient
from tests.mocks.trello import MockTrelloClient


@pytest.mark.usefixtures('session')
class TestUtils:

    def test_trello_client(self, app, mocker):
        mocker.patch('application.utils.Trello', new=MockTrelloClient)
        client, lst = TrelloClient()
        assert lst['id'] == 1
