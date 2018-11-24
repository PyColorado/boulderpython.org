# -*- coding: utf-8 -*-
"""
    filters.py
    ~~~~~~~~~~
    Jinja template filters
"""

import os, pathlib
import markdown2

from flask import request


def autoversion(filename):
    """ Returns a string matching the filename and a query param of the file's
    last modification time in milliseconds

    Useful for agressive caching of static assets like app JavaScript and CSS.

    Args:
        filename (str): the name of the file receiving a

    Returns:
        string: a filename plus it's version number query param
    """
    fullpath = os.path.join(pathlib.Path(__file__).parent, filename[1:])
    try:
        timestamp = str(os.path.getmtime(fullpath))
    except OSError as e:
        return filename
    return "{0}?v={1}".format(filename, timestamp)


def current_route(value, *args):
    """ Returns the a string `current` if URL matches value.

    Useful for navigation elements in templates to add a class name if the current
    page matches the nav element's target href.

    Args:
        value (str): value passed in by filter method

    Returns:
        string: 'current' if conditional is met, otherwise nothing
    """
    if value == str(request.url_rule):
        return "current"


def markdown(value):
    """ Converts the specified markdown string to HTML

    Args:
        value (str): Markdown string

    Returns:
        string: HTML equivalent
    """
    return markdown2.markdown(value)
