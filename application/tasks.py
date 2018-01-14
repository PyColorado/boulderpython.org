# -*- coding: utf-8 -*-
"""
    tasks.py
    ~~~~~~~~
    celery tasks
"""

from . import app, celery
from .utils import TrelloClient
from .models import Submission


@celery.task
def create_hook(_id, card):
    client, lst = TrelloClient()
    submission = Submission().get_by_id(_id)
    hook = client.create_hook(app.config['TRELLO_HOOK'], card)
    Submission().update(submission, hook=hook.id)
