# -*- coding: utf-8 -*-
"""
    tests.test_filters
    ~~~~~~~~~~~~~~~~~

    tests for jinja filters
"""

import pytest

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
