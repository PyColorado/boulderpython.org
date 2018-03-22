# -*- coding: utf-8 -*-
"""
    meetup.py
    ~~~~~~~~~
    a mock for the Meetup APi client
"""


class MockMeetupGroup():
    def __init__(self, *args, **kwargs):
        self.name = 'Mock Meetup Group'
        self.link = 'https://www.meetup.com/MeetupGroup/'
        self.next_event = {
            'id': 0,
            'name': 'Monthly Meetup',
            'venue': 'Galvanize',
            'yes_rsvp_count': 9,
            'time': 1518571800000,  # February 13, 2018 6:30PM
            'utc_offset': -25200000
        }


class MockMeetupEvents():
    def __init__(self, *args, **kwargs):
        self.results = [MockMeetupGroup().next_event] + [self.events(_) for _ in range(1, 6)]

    def events(self, idx):
        return {k: idx for k in ['id', 'venue', 'time', 'utc_offset']}


class MockMeetup():
    api_key = ''

    def __init__(self, *args, **kwargs):
        return

    def GetGroup(self, *args, **kwargs):
        return MockMeetupGroup()

    def GetEvents(self, *args, **kwargs):
        return MockMeetupEvents()
