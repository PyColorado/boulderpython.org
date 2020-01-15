# -*- coding: utf-8 -*-
"""
    routes.py
    ~~~~~~~~~
    application routes
"""
from json import JSONDecodeError

import requests
from requests.exceptions import HTTPError
from mailchimp3 import MailChimp
from flask import Blueprint, current_app, jsonify, render_template, request, redirect, url_for

from application.models import Status, Submission, TrelloList
from application.tasks import create_hook, send_email, extract_card_email
from application.utils import SubmissionsTrelloClient, pluck
from application.extensions import cache
from application.forms import SubmissionForm


bp = Blueprint("bp", __name__)
cached_meetup_response = {}


@cache.cached(timeout=60)
@bp.route("/", methods=["GET"])
def index():
    """Application index.

    Home page for web application. Pulls data from Meetup.
    """
    try:
        group = requests.get(f"https://api.meetup.com/{current_app.config['MEETUP_GROUP']}").json()
        events = requests.get(f"https://api.meetup.com/{current_app.config['MEETUP_GROUP']}/events").json()

        # Success!  Update our cache in case the next call fails
        cached_meetup_response["group"] = group
        cached_meetup_response["events"] = events

    except JSONDecodeError:
        # Sometimes Meetup misbehaves, just use the cached versions.
        group = cached_meetup_response["group"]
        events = cached_meetup_response["events"]

    return render_template("index.html", group=group, upcoming=events[0], events=events)


@bp.route("/submit", methods=["GET", "POST"])
def submit():
    """Submission form page.

    Renders the submission application form and handles form POSTs as well.

    Returns:
        render_template: if page is being called by GET, or form had errors
        redirect: when form is successfully ingested (this redirects and clears form)

    Todo:
        * add Title to Submission object (waiting on update to model)
        * need simple notification for successful form POST, currently no feedback
    """
    form = SubmissionForm()

    if form.validate_on_submit():
        client = SubmissionsTrelloClient()
        labels = client.labels

        card = client.new_submissions_list.add_card(
            name=form.data["title"],
            desc="#DESCRIPTION \n{} \n\n#NOTES \n{}".format(form.data["description"], form.data["notes"]),
            labels=[labels[form.data["format"]], labels[form.data["audience"]]],
            position="top",
            assign=[current_app.config["TRELLO_ASSIGNEE"]],
        )

        submission = Submission().create(
            title=form.data["title"], email=form.data["email"], card_id=card.id, card_url=card.url
        )

        # message Celery to create the webhook
        create_hook.apply_async(args=[submission.id, submission.card_id])

        # message Celery to fetch the card email address
        extract_card_email.apply_async(args=[submission.id])

        # reset form by redirecting back and apply url params
        return redirect(url_for("bp.submit", success=1, id=card.id, url=card.url))

    return render_template("submit.html", form=form)


@bp.route("/trello/hook", methods=["GET", "POST"])
def hook():
    """Trello hook endpoint. Submission cards are fit with a webhook back to our application.

    A great tool for testing this locally is ngrok. Remember to update the value of
    TRELLO_HOOK in app config.
    * example: `ngrok http --subdomain=boulderpython 5000`

    Todo:
        * handle due date updated, this should send a calendar invite
        * handle card moved to Archive list, hsould update submission status
    """

    # this needs to be here so Trello can validate the URL
    if request.method == "HEAD":
        return "OK", 200

    data = request.get_json()
    action = data["action"]

    # if card has moved
    if action["display"]["translationKey"] == "action_move_card_from_list_to_list":
        handle_submission_state_changed(data, action)

    # Card was commented on
    elif action["display"]["translationKey"] == "action_comment_on_card":
        handle_comment_received(data, action)

    return "", 200


def handle_submission_state_changed(data, action):

    send = False
    lists = {}

    # Create a lookup table by symbolic list name
    for local_list in TrelloList().all():
        lists[local_list.list_symbolic_name] = local_list.list_id

    submission = Submission().first(card_id=data["model"]["id"])
    if submission:
        # if card moved from NEW to IN-REVIEW
        if (
            action["data"]["listAfter"]["id"] == lists["REVIEW"]
            and action["data"]["listBefore"]["id"] == lists["NEW"]
            and submission.status == Status.NEW.value
        ):
            Submission().update(submission, status=Status.INREVIEW.value)
            current_app.logger.info(f"Submission {submission.id} is now IN-REVIEW")
            send = True

        # if card moved from IN-REVIEW to SCHEDULED
        elif (
            action["data"]["listAfter"]["id"] == lists["SCHEDULED"]
            and action["data"]["listBefore"]["id"] == lists["REVIEW"]
            and submission.status == Status.INREVIEW.value
        ):
            Submission().update(submission, status=Status.SCHEDULED.value)
            current_app.logger.info(f"Submission {submission.id} is now SCHEDULED")
            send = True

        # if the card has been updated, send an email
        if send:
            send_email.apply_async(args=[submission.id, Status(submission.status).name.lower()])
    else:
        current_app.logger.error("Submission not found for Card: {}".format(data["model"]["id"]))


def handle_comment_received(data, action):
    submission = Submission().first(card_id=data["model"]["id"])

    if submission:
        current_app.logger.info(f"Comment received on Submission {submission.id}")

        template_params = {
            "comment": action["display"]["entities"]["comment"]["text"],
            "name": action["memberCreator"]["fullName"],
        }

        if action["memberCreator"]["id"] != current_app.config["TRELLO_ASSIGNEE"]:
            # Only send an email when a comment is left by someone other than the submitter
            # Organizers themselves should have notifications enabled for the whole board, so
            # they don't really need to get another email notification.  This also prevents
            # a noisy email back to the submitter when they reply to a comment by email.
            send_email.apply_async(args=[submission.id, "comment", template_params])
    else:
        current_app.logger.error("Submission not found for Card: {}".format(data["model"]["id"]))


@bp.route("/robots.txt")
def robots():
    """Tell robots what to do."""
    return "User-agent: *"


@bp.route("/subscribe", methods=["GET", "POST"])
def subscribe():
    """Subscribe email address to the Boulder Python newsletter"""
    data = request.get_json()
    try:
        client = MailChimp(current_app.config.get("MAILCHIMP_USERNAME"), current_app.config.get("MAILCHIMP_API_KEY"))

        client.lists.members.create(
            current_app.config.get("MAILCHIMP_LIST_ID"), {"email_address": data["email"], "status": "subscribed"}
        )

        return jsonify({"result": "subscribed"})

    except HTTPError as e:
        if e.response.status_code == 400:
            json = e.response.json()
            resp = json.get("errors") or json.get("detail") or json
            print(json.get("errors") or json.get("detail") or json)
            current_app.logger.error(
                "An HTTPError occurred subscribing email to MailChimp: {}".format(
                    json.get("errors") or json.get("detail") or json
                )
            )

    except Exception as e:
        current_app.logger.error("An {} occurred subscribing email to MailChimp: {}".format(e.__class__, e))
        resp = "An error occurred: {} - {}".format(e.__class__, e)

    return jsonify({"result": resp}), 500


@bp.route("/privacy", methods=["GET"])
def privacy():
    return render_template("privacy.html")


@bp.route("/submission-process", methods=["GET"])
def submission_process():
    client = SubmissionsTrelloClient()
    list_id = TrelloList().first(list_symbolic_name="HOWDOESTHISWORK").list_id
    how_does_this_work_list = client.board.get_list(list_id)

    return render_template("submission_process.html", how_does_this_work_cards=how_does_this_work_list.list_cards())


@bp.errorhandler(404)
def page_not_found(e=Exception):  # pragma: no cover
    """Simple 404 error handler"""
    current_app.logger.debug(e)
    return render_template("errors/404.html", e=e), 404


@bp.errorhandler(500)
def server_error(e=Exception):  # pragma: no cover
    """Simple 500 error handler"""
    current_app.logger.error(e)
    return render_template("errors/500.html", e=e), 500
