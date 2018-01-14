# -*- coding: utf-8 -*-
"""
    routes.py
    ~~~~~~~~~
    application routes
"""

import logging
from datetime import datetime as dt

import meetup.api
from requests.exceptions import HTTPError
from mailchimp3 import MailChimp
from flask import (
    current_app,
    jsonify,
    render_template,
    request,
    make_response,
    send_from_directory
)

from . import app
from .models import Submission
from .utils import TrelloClient
from .extensions import cache
from .forms import SubmissionForm


@cache.cached(timeout=60)
@app.route('/', methods=['GET'])
def index():
    client = meetup.api.Client(app.config.get('MEETUP_KEY'))
    group = client.GetGroup({'urlname': 'BoulderPython'})
    events = client.GetEvents({'group_urlname': 'BoulderPython'}).__dict__['results']
    upcoming = dict(
        **{'date': dt.fromtimestamp(
            group.next_event['time'] / 1000.00).strftime('%B %d, %Y %-I:%M%p')},
        **next((event for event in events if event['id'] == group.next_event['id']), None))

    return render_template('index.html', group=group, upcoming=upcoming, events=events)


@app.route('/privacy', methods=['GET'])
def privacy():
    return render_template('privacy.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit():

    form = SubmissionForm()
    labels = app.config['TRELLO_LABELS']

    if form.validate_on_submit():
        client, newSubmissionsList = TrelloClient()

        card = newSubmissionsList.add_card(
            name=form.data['title'],
            desc=form.data['description'],
            labels=[
                labels['FORMAT'][form.data['FORMAT']],
                labels['AUDIENCE'][form.data['AUDIENCE']]
            ],
            position='top',
            assign=[app.config['TRELLO_ASSIGNEE']]
        )

        submission = Submission().create(
            email=form.data['email'],
            card_id=card.id,
            card_url=card.url,
            status='NEW')

    return render_template('submit.html', form=form)


@app.route('/robots.txt')
def robots():
    return ('User-agent: *')


@cache.cached(timeout=60)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        './static/img/favicon/', 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    """Adds user to Mailchimp mailing list."""
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

    except Exception as e:
        print('An error occurred: {} - {}'.format(e.__class__, e))
        resp = 'An error occurred: {} - {}'.format(e.__class__, e)

    return jsonify({'result': resp}), 500


# ERRORS ######################################################################
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e=Exception):  # pragma: no cover
    logging.debug(e)
    return render_template('errors/404.html', e=e), 404


# Handle 500 errors
@app.errorhandler(500)
def server_error(e=Exception):  # pragma: no cover
    logging.debug(e)
    return render_template('errors/500.html', e=e), 500
