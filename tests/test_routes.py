# -*- coding: utf-8 -*-
"""
    tests.routes
    ~~~~~~~~~~~~~~~~~

    tests for application routes and view logic
"""

import pytest


class MockMeetupGroup():
    def __init__(self, *args, **kwargs):
        self.name = 'Mock Meetup Group'
        self.link = 'https://www.meetup.com/MeetupGroup/'
        self.next_event = {
            'id': 0,
            'name': 'Monthly Meetup',
            'yes_rsvp_count': 9,
            'time': 1518571800000,  # February 13, 2018 6:30PM
            'utc_offset': -25200000
        }


class MockMeetupEvents():
    def __init__(self, *args, **kwargs):
        self.results = [self.events(_) for _ in range(5)]

    def events(self, idx):
        return {k: idx for k in ['id', 'venue', 'time']}


class MockMeetup():
    api_key = ''

    def __init__(self, *args, **kwargs):
        return

    def GetGroup(self, *args, **kwargs):
        return MockMeetupGroup()

    def GetEvents(self, *args, **kwargs):
        return MockMeetupEvents()


class MockMailChimpListMember():
    def create(self):
        return ''


# class MockMailChimpLists():
#     members = MockMailChimpListMember()


# class MockMailChimp():
#     mc_secret = 'mail-chimp'
#     lists = MockMailChimpLists()

#     def __init__(self, *args, **kwargs):
#         return


@pytest.mark.usefixtures('session')
class TestRoutes:

    def setup_class(self, *args, **kwargs):
        self.config = {
            'MEETUP_GROUP': 'group',
        }

    def test_index(self, app, client, mocker):
        app.config.update(self.config)
        mocker.patch('meetup.api.Client', new=MockMeetup)
        resp = client.get('/')
        assert b'<h2 style="color:#fff;">February 13, 2018 6:30PM</h2>' in resp.data
        assert resp.status_code == 200

    def test_submit(self, client, mocker):
        pass

    def test_hook_head(self, client, mocker):
        resp = client.head('/trello/hook')
        assert resp.status_code == 200

    def test_robots(self, client):
        resp = client.get('/robots.txt')
        assert b'User-agent: *' in resp.data
        assert resp.status_code == 200

    # def test_subscribe(self, client, mocker):
    #     mc = mocker.patch('mailchimp3.MailChimp', new=MockMailChimp)
    #     mc2 = mocker.patch('mailchimp3.entities.listmembers.ListMembers', 'create')
    #     resp = client.post('/subscribe', data=dict({'email': 'foo@baar.com'}))
    #     assert resp.status_code == 200

    def test_privacy(self, client):
        resp = client.get('/privacy')
        assert b'<h1>PRIVACY POLICY</h1>' in resp.data
        assert resp.status_code == 200
