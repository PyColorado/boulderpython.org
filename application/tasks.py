# -*- coding: utf-8 -*-
"""
    tasks.py
    ~~~~~~~~
    celery tasks
"""

from flask import render_template

from . import app, celery
from .utils import TrelloClient
from .models import Submission, Status
from .extensions import mail


@celery.task
def create_hook(_id, card):
    client, lst = TrelloClient()
    submission = Submission().get_by_id(_id)
    webhook = client.create_hook(app.config['TRELLO_HOOK'], card)
    Submission().update(submission, hook=webhook.id)

    # send confirmation email
    send_email.apply_async((submission.id, submission.email))


@celery.task
def send_email(_id, email):
    SUBJECTS = {
        Status.NEW.value: 'Talk Submission Received',
        Status.INREVIEW.value: 'Talk Submission In-Review',
        Status.SCHEDULED.value: '🎉 CONGRATS! Talk Submission Accepted 🎉'
    }

    submission = Submission().get_by_id(_id)

    mail.send_email(
        to_email=submission.email,
        subject=SUBJECTS[submission.status],
        html=render_template('email/{}.html'.format(Status(submission.status).name.lower()),
            title=SUBJECTS[submission.status], submission=submission)
    )
