# -*- coding: utf-8 -*-
"""
    filters.py
    ~~~~~~~~~~
    Jinja template filters
"""

import os, pathlib

from flask import request


def autoversion(filename):
    """appends file's modified time as query param"""
    fullpath = os.path.join(pathlib.Path(__file__).parent, filename[1:])
    try:
        timestamp = str(os.path.getmtime(fullpath))
    except OSError as e:
        return filename
    return '{0}?v={1}'.format(filename, timestamp)


def current_route(value, *args):
    """
        Returns 'current', if value matches current url,
        used to set class on current route in nav
    """
    if value == str(request.url_rule):
        return 'current'
