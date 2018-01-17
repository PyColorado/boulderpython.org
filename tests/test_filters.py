# -*- coding: utf-8 -*-
"""
    tests.test_filters
    ~~~~~~~~~~~~~~~~~

    tests for jinja filters
"""

import pytest
from flask import render_template_string

from application.filters import autoversion, current_route


@pytest.mark.usefixtures('session')
class TestFilters:

    def test_filename_no_mtime(self):
        r = autoversion('filename.css')
        assert r == 'filename.css'

    def test_filename(self, mocker):
        _time = 1289182.0
        mtime = mocker.patch('os.path.getmtime')
        mtime.return_value = _time
        r = autoversion('filename.css')
        assert '?v=' in r
        assert _time == float(r.split('=')[1])

    def test_current_route(self, app):
        with app.test_request_context(path='/'):
            assert current_route('/') == 'current'

    def test_not_current_route(self, app):
        with app.test_request_context(path='/'):
            assert current_route('/nope/') is None

    def test_convert_ms_tz_mst(self, app):
        time = 1518571800000
        utc_offset = -25200000
        assert render_template_string("{{ time|convert_ms(offset=offset, format='%I:%M%p') }}",
                                      time=time,
                                      offset=utc_offset) == '06:30PM'

    def test_convert_ms_tz_est(self, app):
        time = 1518571800000
        utc_offset = -18000000
        assert render_template_string("{{ time|convert_ms(offset=offset, format='%I:%M%p') }}",
                                      time=time,
                                      offset=utc_offset) == '08:30PM'
