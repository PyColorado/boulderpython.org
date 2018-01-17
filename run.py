# -*- coding: utf-8 -*-
"""
    run.py
    ~~~~~~
    application management
"""

import os

import click, pytest, livereload
from sqlalchemy import exc

from application import create_app, configure
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


@app.cli.command('test')
@click.option('-v', 'verbose', flag_value='--verbose', help="Increase verbosity while testing.")
@click.option('-x', 'x', flag_value='-x', help="Exit after first failure.")
@click.option('-rs', 'rs', flag_value='-rs', help="Enables skipped test report.")
@click.option('-reports', 'reports', flag_value=['--cov-report', 'term-missing'], help="")
@click.option('-cov', 'cov', flag_value='--cov', help="Enable code coverage.")
@click.option('-flake8', 'flake8', flag_value='--flake8', help="Enable pep8 and pyflakes testing.")
@click.pass_context
def test(ctx, *args, **kwargs):
    # since reports requires two words, and pytest wants a list, we need this
    reports = ctx.params.pop('reports')
    pytest.main(
        ['tests', '--pyargs', 'application'] + [v for k, v in ctx.params.items() if v] + reports)
