# -*- coding: utf-8 -*-
"""
    tasks.py
    ~~~~~~~~
    celery tasks
"""

import random

from sendgrid import SendGridAPIClient
from flask import current_app, render_template
# from celery.utils.log import get_task_logger
from sendgrid.helpers.mail import Mail, Email, Content

from application.utils import SubmissionsTrelloClient
from application.models import Submission, Status
from application.extensions import celery


def exponential_backoff(task_self):
    '''Exponentially increase delay of task retry.

    Helper function that can be used in task ``eta`` or ``self.retry`` for bound tasks.
    It begins with 60 seconds, but exponentially increases the delay so that tasks
    aren't just being retried feverishly by Celery.

    Args:
        task_self (Celery.task): an instance of the celery task being retried

    Todo:
        * maybe it's best left to task max_retries but need a way to cancel after n failuers

    '''
    minutes = task_self.default_retry_delay / 60
    rand = random.uniform(minutes, minutes * 1.3)
    return int(rand ** task_self.request.retries) * 60


@celery.task
def create_hook(_id, card):
    '''Create Webhook for Trello Card.

    When a card is created after a submission, we need to fix it with a webhook back to  our app.

    Args:
        _id (int): the submission id
        card(str): the trello id for the card

    Todo:
        * No Exception handling!
        * should this handle submission not found?
    '''
    client = SubmissionsTrelloClient()
    submission = Submission().get_by_id(_id)
    webhook = client.create_hook(current_app.config['TRELLO_HOOK'], card)
    Submission().update(submission, hook=webhook.id)

    # send confirmation email
    send_email.apply_async((submission.id, submission.email))


@celery.task(bind=True)
def send_email(self, _id, email):
    '''Sends an email

    Currently configured to send emails for updates to submission statuses

    Args:
        self: this task is bound to allow access to self
        _id (int): the submission id
        email(str): email address of the intended recipient

    Todo:
        * use send_at to send emails at a updates at reasonable times
        * should this handle submission not found?
        * add attachment in Scheduled email.

    '''
    # logger = get_task_logger(__name__)

    # subject lines for emails based on submission status
    # not the best place for this, I admit.
    SUBJECTS = {
        Status.NEW.value: 'Talk Submission Received',
        Status.INREVIEW.value: 'Talk Submission In-Review',
        Status.SCHEDULED.value: '🎉 CONGRATS! Talk Submission Accepted 🎉'
    }

    submission = Submission().get_by_id(_id)

    sg = SendGridAPIClient(apikey=current_app.config['SENDGRID_API_KEY'])

    mail = Mail(
        Email(current_app.config['SENDGRID_DEFAULT_FROM']),
        SUBJECTS[submission.status],
        Email(submission.email),
        Content("text/html", (
            render_template(
                'email/{}.html'.format(Status(submission.status).name.lower()),
                title=SUBJECTS[submission.status],
                submission=submission)))
    )

    mail.personalizations[0].add_cc(Email(current_app.config['SENDGRID_DEFAULT_FROM']))
    # mail.add_attachment(build_attachment())
    # mail.send_at = 1443636842

    sg.client.mail.send.post(request_body=mail.get())
    # logger.error(resp.status_code)
    # logger.error(resp.body)
    # logger.error(resp.headers)
