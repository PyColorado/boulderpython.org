# -*- coding: utf-8 -*-
"""
    tests.tasks
    ~~~~~~~~~~~~~~~~~

    tests for celery tasks
"""

import pytest

# from application.models import Submission
# from application.tasks import create_hook

# from tests.mocks.trello import MockTrelloClient


@pytest.mark.usefixtures('session')
class TestTasks:

    def test_create_hook(self, app, celery_worker, mocker):
        pass
        # with app.test_request_context():
        #     sub = Submission().create(
        #         email='email', title='title', card_id='100', card_url='url')

        #     # mocker.patch('application.tasks.TrelloClient', new=MockTrelloClient)
        #     mocker.patch('application.utils.Trello', new=MockTrelloClient)

        #     mocker.patch('application.tasks.Submission.get_by_id', lambda: sub)

        #     res = create_hook.delay(sub.id, sub.card_id)
        #     assert res.successful()
        #     assert False

    def test_send_email(self):
        pass
