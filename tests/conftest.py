# -*- coding: utf-8 -*-
'''
    __init__.py
    ~~~~~~~~~~~
    description
'''

import os
import pytest

from application import create_app
from application.extensions import db as _db


@pytest.fixture(scope='session')
def app(request):
    '''Session-wide test `Flask` application.'''
    app = create_app('testing')

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture
def client(app):
    '''return an instance of the application's test client'''
    return app.test_client()


@pytest.fixture(scope='session')
def db(app, request):
    '''Session-wide test database.'''
    if os.path.exists(app.config['TEST_DB']):
        os.unlink(app.config['TEST_DB'])

    def teardown():
        _db.drop_all()
        os.unlink(app.config['TEST_DB'])

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    '''Creates a new database session for a test.'''
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session
