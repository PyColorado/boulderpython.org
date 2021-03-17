# -*- coding: utf-8 -*-
"""
    tests.routes
    ~~~~~~~~~~~~~~~~~

    tests for application routes and view logic
"""
from json import JSONDecodeError

from unittest import mock

import pytest

from application.models import Submission

from tests.mocks.trello import MockTrelloClient
from tests.mocks.meetup import MockMeetup


class MisbehavedMockMeetup(MockMeetup):
    def GetEvents(self, *args, **kwargs):
        # Technically this could happen with GetGroup too, but I've only ever seen it on GetEvents
        raise JSONDecodeError("Expecting value", "", 0)


class MockMailChimpListMember:
    def create(self):
        return ""


# class MockMailChimpLists():
#     members = MockMailChimpListMember()


# class MockMailChimp():
#     mc_secret = 'mail-chimp'
#     lists = MockMailChimpLists()

#     def __init__(self, *args, **kwargs):
#         return


@pytest.mark.usefixtures("session")
class TestRoutes:
    def test_index(self, app, client, mocker):
        resp = client.get("/")
        assert b"<h1>Upcoming Events</h1>" in resp.data
        assert resp.status_code == 200

    def test_submit_get(self, client, mocker):
        resp = client.get("/submit")
        assert b'<form method="POST" action="/submit">' in resp.data
        assert resp.status_code == 200

    def test_submit_post(self, client, mocker):
        mocker.patch("application.routes.SubmissionsTrelloClient", new=MockTrelloClient)
        data = dict(
            email="submit1@example.com",
            title="foo",
            pitch="foo",
            format="IN-DEPTH",
            audience="INTERMEDIATE",
            description="foo",
            notes="foo",
        )

        # https://stackoverflow.com/questions/37579411/testing-a-post-that-uses-flask-wtf-validate-on-submit
        resp = client.post("/submit", data=data, follow_redirects=True)

        # make sure it's successful
        assert resp.status_code == 200

        # make sure the object was saved
        assert Submission().first(email="submit1@example.com")

    def test_submit_redirect(self, client, mocker):
        mocker.patch("application.routes.SubmissionsTrelloClient", new=MockTrelloClient)
        with mock.patch("application.routes.url_for") as patched:
            data = dict(
                email="submit2@example.com",
                title="foo",
                pitch="foo",
                format="IN-DEPTH",
                audience="INTERMEDIATE",
                description="foo",
                notes="foo",
            )

            client.post("/submit", data=data, follow_redirects=True)

            patched.assert_called_once_with("bp.submit", id=1, success=1, url="http://mock.trello.com/card/1")
        # Now patch with the misbehaved client and make sure we still render.
        resp = client.get("/")
        assert b"<h1>Upcoming Events</h1>" in resp.data
        assert resp.status_code == 200

    def test_hook_head(self, client, mocker):
        resp = client.head("/trello/hook")
        assert resp.status_code == 200

    def test_robots(self, client):
        resp = client.get("/robots.txt")
        assert b"User-agent: *" in resp.data
        assert resp.status_code == 200

    # def test_subscribe(self, client, mocker):
    #     mc = mocker.patch('mailchimp3.MailChimp', new=MockMailChimp)
    #     mc2 = mocker.patch('mailchimp3.entities.listmembers.ListMembers', 'create')
    #     resp = client.post('/subscribe', data=dict({'email': 'foo@baar.com'}))
    #     assert resp.status_code == 200

    def test_privacy(self, client):
        resp = client.get("/privacy")
        assert b"<h1>PRIVACY POLICY</h1>" in resp.data
        assert resp.status_code == 200
