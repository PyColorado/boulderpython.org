#!/usr/bin/env python3.6


"""
Runs the boulderpython website
"""


# stdlib
import os
import sys
import argparse
import signal
import time

# 3rd
import livereload
from typing import Optional

# local
from application import app, configure


PORT = os.environ.get('PORT') or '9999'
HOST = os.environ.get('HOST') or 'localhost'


def main(args: argparse.Namespace) -> None:
    configure(os.getenv('FLASK_CONFIG') or 'default')

    if args.test is True:
        pid = os.fork()
        if pid == 0:
            run_server(mode='debug')
        else:
            os.system(f'py.test')
            os.kill(pid, signal.SIGINT)
    elif (args is not None) and (args.debug or app.debug):
        run_server(mode='debug')
    else:
        run_server(mode='prod')


def run_server(mode: Optional[str]='debug') -> None:
    """
    Runs the server in either debug or prod mode

    :param mode: mode to run in
    :return: None
    """
    if mode == 'debug':
        # DEBUG (livereload) MODE
        configure('testing')
        app.jinja_env.auto_reload = True
        app.debug = True
        server = livereload.Server(app.wsgi_app)
        server.watch('.', ignore=lambda x: ('log' in x or
                                            '.idea' in x))
        server.serve(
            port=PORT,
            host=HOST
        )
    elif mode == 'prod':
        # Pseduo Prod Mode
        pid = os.fork()
        if pid == 0:
            while True:
                try:
                    time.sleep(1)
                except KeyboardInterrupt:
                    os.kill(pid, signal.SIGINT)
                    break
        else:
            os.system(f'gunicorn -b :{PORT} application:app')


def get_args():
    """
    Get command line arguments
    :return: arguments
    """
    parser = argparse.ArgumentParser(
        description='Run the Boulder Python Website'
    )
    parser.add_argument('-d', '--debug', default=False, action='store_true',
                        help='Run in DEBUG mode.')
    parser.add_argument('-t', '--test', default=False, action='store_true',
                        help='Run in TEST mode.')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
    sys.exit(main(args))
