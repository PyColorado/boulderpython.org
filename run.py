# -*- coding: utf-8 -*-
"""
    run.py
    ~~~~~~
    application management
"""

import os

import click, livereload
from sqlalchemy import exc

from application import create_app
from application.extensions import db


app = create_app()


@app.cli.command('initdb')
def initdb():
    '''Creates the database tables.'''
    try:
        # Clear out our SQL database
        click.echo(' * Clearing database...')
        db.drop_all()

    except exc.OperationalError as e:
        click.secho(f'{e}', fg='red')

    except Exception as e:
        click.secho(f'{e}', fg='red')

    click.echo(' * Creating database tables...')
    db.create_all()

    # all done
    click.secho(' * DONE', fg='green')


@app.cli.command('runserver')
@click.option('--reload', 'reload', is_flag=True, help='run application with livereload')
def runserver(reload):
    '''Shortcut to ``flask run``'''
    if reload:
        server = livereload.Server(app.wsgi_app)
        server.watch('.', ignore=lambda x: ('log' in x or '.idea' in x))
        server.serve(port=os.environ.get('PORT', '9999'), host=os.environ.get('HOST', 'localhost'))
        return
    app.run()
