# -*- coding: utf-8 -*-
'''
    routes.py
    ~~~~~~~~~
    application routes
'''

import meetup.api
from requests.exceptions import HTTPError
from mailchimp3 import MailChimp
from flask import (
    Blueprint,
    current_app,
    jsonify,
    render_template,
    request,
    redirect,
    url_for
)

from application.models import Status, Submission
from application.tasks import create_hook, send_email
from application.utils import TrelloClient
from application.extensions import cache
from application.forms import SubmissionForm


bp = Blueprint('bp', __name__)


@cache.cached(timeout=60)
@bp.route('/', methods=['GET'])
def index():
    '''Application index.

    Home page for web application. Pulls data from Meetup.

    Todo:
        * move Meetup Client to `utils` and have it return a tuple
        * Meetup occasionally responds with an empty JSON, so we should cache this to avoid that.
    '''
    client = meetup.api.Client(current_app.config.get('MEETUP_KEY'))
    group = client.GetGroup({'urlname': 'BoulderPython'})
    events = client.GetEvents({'group_urlname': current_app.config['MEETUP_GROUP']}).results
    upcoming = dict(
        **next((event for event in events if event['id'] == group.next_event['id']), None)
    )

    return render_template('index.html', group=group, upcoming=upcoming, events=events)


@bp.route('/submit', methods=['GET', 'POST'])
def submit():
    '''Submission form page.

    Renders the submission application form and handles form POSTs as well.

    Returns:
        render_template: if page is being called by GET, or form had errors
        redirect: when form is successfully ingested (this redirects and clears form)

    Todo:
        * add Title to Submission object (waiting on update to model)
        * need simple notification for successful form POST, currently no feedback
    '''
    form = SubmissionForm()
    labels = current_app.config['TRELLO_LABELS']

    if form.validate_on_submit():
        client, lst = TrelloClient()

        card = lst.add_card(
            name=form.data['title'],
            desc="#DESCRIPTION \n{} \n\n#NOTES \n{}".format(
                form.data['description'],
                form.data['notes']),
            labels=[
                labels['FORMAT'][form.data['format']],
                labels['AUDIENCE'][form.data['audience']]
            ],
            position='top',
            assign=[current_app.config['TRELLO_ASSIGNEE']]
        )

        submission = Submission().create(
            title=form.data['title'], email=form.data['email'], card_id=card.id, card_url=card.url)

        # message Celery to create the webhook
        create_hook.apply_async(args=[submission.id, submission.card_id])

        # reset form by redirecting back and apply url params
        return redirect(url_for('bp.submit', success=1, id=card.id, url=card.url))

    return render_template('submit.html', form=form)


@bp.route('/trello/hook', methods=['GET', 'POST'])
def hook(send=False):
    '''Trello hook endpoint. Submission cards are fit with a webhook back to our application.

    A great tool for testing this locally is ngrok. Remember to update the value of
    TRELLO_HOOK in app config.
    * example: `ngrok http --subdomain=boulderpython 5000`

    Todo:
        * handle due date updated, this should send a calendar invite
        * handle card moved to Archive list, hsould update submission status
    '''

    # this needs to be here so Trello can validate the URL
    if request.method == 'HEAD':
        return 'OK', 200

    data = request.get_json()
    action = data["action"]
    lists = current_app.config["TRELLO_LISTS"]

    # if card has moved
    if action["display"]["translationKey"] == "action_move_card_from_list_to_list":

        submission = Submission().first(card_id=data['model']['id'])
        if submission:
            # if card moved from NEW to IN-REVIEW
            if action["data"]["listAfter"]["id"] == lists["REVIEW"]["id"] \
                    and action["data"]["listBefore"]["id"] == lists["NEW"]["id"] \
                    and submission.status == Status.NEW.value:
                Submission().update(submission, status=Status.INREVIEW.value)
                current_app.logger.info("Submission {submission.id} is now IN-REVIEW")
                send = True

            # if card moved from IN-REVIEW to SCHEDULED
            elif action["data"]["listAfter"]["id"] == lists["SCHEDULED"]["id"] \
                    and action["data"]["listBefore"]["id"] == lists["REVIEW"]["id"] \
                    and submission.status == Status.INREVIEW.value:
                Submission().update(submission, status=Status.SCHEDULED.value)
                current_app.logger.info("Submission {submission.id} is now SCHEDULED")
                send = True

            # if the card has been updated, send an email
            if send:
                send_email.apply_async(args=[submission.id, submission.email])
        else:
            current_app.logger.error(
                'Submission not found for Card: {}'.format(data['model']['id']))

    return '', 200


@bp.route('/robots.txt')
def robots():
    '''Tell robots what to do.'''
    return ('User-agent: *')


@bp.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    '''Subscribe email address to the Boulder Python newsletter'''
    data = request.get_json()
    try:
        client = MailChimp(
            current_app.config.get('MAILCHIMP_USERNAME'),
            current_app.config.get('MAILCHIMP_API_KEY'))

        client.lists.members.create(current_app.config.get('MAILCHIMP_LIST_ID'), {
            'email_address': data['email'],
            'status': 'subscribed',
        })

        return jsonify({'result': 'subscribed'})

    except HTTPError as e:
        if e.response.status_code == 400:
            json = e.response.json()
            resp = json.get('errors') or json.get('detail') or json
            print(json.get('errors') or json.get('detail') or json)
            current_app.logger.error(
                'An HTTPError occurred subscribing email to MailChimp: {}'.format(
                    json.get('errors') or json.get('detail') or json))

    except Exception as e:
        current_app.logger.error(
            'An {} occurred subscribing email to MailChimp: {}'.format(e.__class__, e))
        resp = 'An error occurred: {} - {}'.format(e.__class__, e)

    return jsonify({'result': resp}), 500


@bp.route('/privacy', methods=['GET'])
def privacy():
    return render_template('privacy.html')


@bp.errorhandler(404)
def page_not_found(e=Exception):  # pragma: no cover
    '''Simple 404 error handler'''
    current_app.logger.debug(e)
    return render_template('errors/404.html', e=e), 404


@bp.errorhandler(500)
def server_error(e=Exception):  # pragma: no cover
    '''Simple 500 error handler'''
    current_app.logger.error(e)
    return render_template('errors/500.html', e=e), 500
