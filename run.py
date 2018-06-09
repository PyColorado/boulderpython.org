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

from application import create_app, TrelloList
from application.extensions import db
from application.utils import SubmissionsTrelloClient
from trello import ResourceUnavailable

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


@app.cli.command('initlists')
def init_lists():
    '''Populates a Trello board with the default lists.'''
    client = SubmissionsTrelloClient()
    board = client.board

    if not board:
        click.secho('TRELLO_BOARD must be specified in the app configuration.', fg='red')
        sys.exit(1)

    # We iterate the list in reverse order because by default the Trello client inserts new lists
    # at the beginning.  So in a sense, we need to create them from right-to-left.
    for default_list_options in reversed(app.config['DEFAULT_TRELLO_LISTS']):

        default_list_name = default_list_options['name']
        default_list_caption = default_list_options['default_caption']

        # Verity that this list is already in our database and that it points to a valid list on
        # the trello board.
        local_list = None
        matching_lists = TrelloList().find(list_symbolic_name=default_list_name).all()

        if matching_lists:
            local_list = matching_lists[0]

            # Verify that this list ID is on the trello board
            try:
                trello_list = board.get_list(local_list.list_id)

                # Reopen the list if it was accidentally closed.
                if trello_list.closed:
                    trello_list.open()

            except ResourceUnavailable:
                trello_list = None

            if trello_list:
                # All good.
                click.echo(f' * "{default_list_name}" list present in both database and Trello.')
                continue

        # No entry or a mismatched ID in the database.  See if the list already exists on the
        # board (with the default caption).
        for existing_list in board.open_lists():
            if existing_list.name == default_list_caption:
                # There it is!
                click.echo(f' * Found existing Trello list for "{default_list_name}"...')
                trello_list = existing_list
                break
        else:
            # No matching trello list found.  Create it.
            click.echo(f' * Creating Trello list for "{default_list_name}"...')
            trello_list = board.add_list(default_list_caption)

        if local_list:
            # Just need to update the local entry.
            click.echo(f' * Updating list ID in database for "{default_list_name}"...')

            local_list.list_id = trello_list.id
            TrelloList().save(local_list)
        else:
            # Need to create a new local entry.
            click.echo(f' * Adding list ID to database for "{default_list_name}"...')

            TrelloList().create(list_symbolic_name=default_list_name,
                                list_id=trello_list.id)

    # all done
    click.secho(' * DONE', fg='green')


@app.cli.command('initlabels')
def init_labels():
    '''Populates a Trello board with the default labels.'''
    client = SubmissionsTrelloClient()
    board = client.board
    all_label_names = set(map(lambda x: x.name, board.get_labels()))

    for default_labels_by_category in app.config['DEFAULT_TRELLO_LABELS'].values():
        for label in default_labels_by_category.values():
            default_caption = label['default_caption']

            if default_caption not in all_label_names:
                click.echo(f' * Adding label "{default_caption}"...')
                board.add_label(default_caption, label['default_color'])
            else:
                click.echo(f' * "{default_caption}" label already exists...')

    # all done
    click.secho(' * DONE', fg='green')


@app.cli.command('initboard')
def init_board():
    '''Populates a Trello board with the default lists and labels.'''
    init_lists()
    init_labels()


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
