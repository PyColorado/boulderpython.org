# -*- coding: utf-8 -*-
"""
    run.py
    ~~~~~~
    application management
"""

import os, sys

import click, livereload
from sqlalchemy import exc
from flask.cli import with_appcontext
from celery.bin.celery import main as celery_main

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
        server.watch('.', ignore=lambda x: ('log' in x))
        server.serve(port=os.environ.get('PORT', '9999'), host=os.environ.get('HOST', 'localhost'))
        return
    app.run()


@app.cli.command('celeryd')
def celeryd():
    celery_args = ['celery', 'worker', '-l', 'info', '-E']
    with app.app_context():
        return celery_main(celery_args)


@app.cli.command('ishell')
@click.argument('ipython_args', nargs=-1, type=click.UNPROCESSED)
@with_appcontext
def shell(ipython_args):
    '''Runs an iPython shell in the app context.

    Runs an interactive Python shell in the context of a given Flask application. The application
    will populate the default namespace of this shell according to it's configuration. This is
    useful for executing small snippets of management code without having to manually configuring
    the application.

    Stolen from: https://github.com/ei-grad/flask-shell-ipython/blob/master/flask_shell_ipython.py
    '''
    import IPython
    from IPython.terminal.ipapp import load_default_config
    from traitlets.config.loader import Config
    from flask.globals import _app_ctx_stack

    app = _app_ctx_stack.top.app

    if 'IPYTHON_CONFIG' in app.config:
        config = Config(app.config['IPYTHON_CONFIG'])
    else:
        config = load_default_config()

    config.TerminalInteractiveShell.banner1 = '''Python %s on %s
IPython: %s
App: %s%s
Instance: %s''' % (sys.version,
                   sys.platform,
                   IPython.__version__,
                   app.import_name,
                   app.debug and ' [debug]' or '',
                   app.instance_path)

    IPython.start_ipython(
        argv=ipython_args,
        user_ns=app.make_shell_context(),
        config=config,
    )


if __name__ == '__main__':
    runserver(['--reload'])
