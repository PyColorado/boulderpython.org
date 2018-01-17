# -*- coding: utf-8 -*-
"""
    tests.test_errorhandlers
    ~~~~~~~~~~~~~~~~~

    tests for error handlers
"""

import pytest


@pytest.mark.usefixtures('session')
class TestErrors:

    def test_page_not_found(self, client):
        resp = client.get('error')
        # assert b'<h1>404: NOT FOUND</h1>' in resp.data
        assert resp.status_code == 404

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_internal_server_error(self, client):
        resp = client.get('test/error/500')
        assert resp.status_code == 500
