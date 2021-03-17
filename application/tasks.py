# -*- coding: utf-8 -*-
"""
    tasks.py
    ~~~~~~~~
    celery tasks
"""

import random

import requests
from sendgrid import SendGridAPIClient
from flask import current_app, render_template

# from celery.utils.log import get_task_logger
from sendgrid.helpers.mail import Mail, Email, Content

from application.utils import SubmissionsTrelloClient
from application.models import Submission, Status
from application.extensions import celery


def exponential_backoff(task_self):
    """Exponentially increase delay of task retry.

    Helper function that can be used in task ``eta`` or ``self.retry`` for bound tasks.
    It begins with 60 seconds, but exponentially increases the delay so that tasks
    aren't just being retried feverishly by Celery.

    Args:
        task_self (Celery.task): an instance of the celery task being retried

    Todo:
        * maybe it's best left to task max_retries but need a way to cancel after n failuers

    """
    minutes = task_self.default_retry_delay / 60
    rand = random.uniform(minutes, minutes * 1.3)
    return int(rand ** task_self.request.retries) * 60


@celery.task
def create_hook(_id, card):
    """Create Webhook for Trello Card.

    When a card is created after a submission, we need to fix it with a webhook back to  our app.

    Args:
        _id (int): the submission id
        card(str): the trello id for the card

    Todo:
        * No Exception handling!
        * should this handle submission not found?
    """
    client = SubmissionsTrelloClient()
    submission = Submission().get_by_id(_id)
    webhook = client.create_hook(current_app.config["TRELLO_HOOK"], card, token=current_app.config["TRELLO_API_TOKEN"])
    Submission().update(submission, hook=webhook.id)

    # send confirmation email
    send_email.apply_async(args=[submission.id, Status(submission.status).name.lower()])


@celery.task
def extract_card_email(_id):
    """Forcibly extract the Trello card email address.

    The Trello card email address allows submitters to directly reply to comment notifications.
    Trello does NOT provide this information via the API.
    See: https://stackoverflow.com/questions/42247377/trello-api-e-mail-address-of-my-card-returns-null  # noqa: E501

    So we have to do good 'ole browser emulation

    Args:
        _id (int): the submission id

    """
    session = requests.Session()

    # Load the login page to capture the dsc cookie
    session.get("https://trello.com/login")

    # Authenticate using email and password
    auth_response = session.post(
        "https://trello.com/1/authentication",
        data={
            "factors[user]": current_app.config["TRELLO_USERNAME"],
            "factors[password]": current_app.config["TRELLO_PASSWORD"],
            "method": "password",
        },
    )

    # Perform authorization step
    session.post(
        "https://trello.com/1/authorization/session",
        data={"authentication": auth_response.json()["code"], "dsc": session.cookies["dsc"]},
    )

    # Fetch the card JSON
    submission = Submission().get_by_id(_id)
    response = session.get(submission.card_url + ".json")

    # Extract the special email and save it to our database record
    submission.card_email = response.json()["email"]
    Submission().save(submission)


@celery.task(bind=True)
def send_email(self, _id, template_name, template_params=None):
    """Sends an email

    Currently configured to send emails for updates to submission statuses

    Args:
        self: this task is bound to allow access to self
        _id (int): the submission id
        email(str): email address of the intended recipient
        template_name(str): the name of the template to use for this email. Must be located in
            templates/email directory.

    Todo:
        * use send_at to send emails at a updates at reasonable times
        * should this handle submission not found?
        * add attachment in Scheduled email.

    """
    if not template_params:
        template_params = {}

    # logger = get_task_logger(__name__)

    # subject lines for emails based on submission status
    # not the best place for this, I admit.
    SUBJECTS = {
        "new": "Talk Submission Received",
        "inreview": "Talk Submission In-Review",
        "scheduled": "🎉 CONGRATS! Talk Submission Accepted 🎉",
        "comment": "Reply to Comments",
    }

    submission = Submission().get_by_id(_id)

    sg = SendGridAPIClient(apikey=current_app.config["SENDGRID_API_KEY"])

    if not template_name:
        # No template specified, use the submission status to determine what we're sending
        template_name = Status(submission.status).name.lower()

    template = f"email/{template_name}.html"

    mail = Mail(
        Email(current_app.config["SENDGRID_DEFAULT_FROM"]),
        SUBJECTS[template_name],
        Email(submission.email),
        Content(
            "text/html",
            (render_template(template, title=SUBJECTS[template_name], submission=submission, **template_params)),
        ),
    )

    mail.personalizations[0].add_cc(Email(current_app.config["SENDGRID_DEFAULT_FROM"]))

    if template_name == "comment" and submission.card_email:
        # Add the card itself as the reply-to address.  When the user replies, it will create a
        # comment on the card via the Organizers account
        mail.reply_to = Email(submission.card_email)

    # mail.add_attachment(build_attachment())
    # mail.send_at = 1443636842

    sg.client.mail.send.post(request_body=mail.get())
    # logger.error(resp.status_code)
    # logger.error(resp.body)
    # logger.error(resp.headers)
