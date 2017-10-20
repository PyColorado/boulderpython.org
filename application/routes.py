# stdlib
import logging

# 3rd party
from flask import render_template, make_response, send_from_directory
from scss import Compiler

# local
from . import app, cache

# STATIC CONTENT ##################################################################################################
@app.route('/', methods=['GET'])
def homepage():
    return render_template('home.html')


@app.route('/privacy', methods=['GET'])
def privacy():
    return render_template('privacy.html')


@app.route('/robots.txt')
def robots():
    # removed sitemap link cause useless
    return (
        'User-agent: *'
    )


@cache.cached(timeout=60)
@app.route('/static/css/main.css')
def styling():
    with open('./application/static/css/main.scss', 'r') as scssobj:
        style = Compiler().compile_string(scssobj.read())
    resp = make_response(style)
    resp.mimetype = 'text/css'
    return resp


@cache.cached(timeout=60)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('./static/img/favicon/',
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


# ERRORS ###############################################################################################################
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e=Exception):  # pragma: no cover
    logging.debug(e)
    return render_template('404.html', e=e), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e=Exception):  # pragma: no cover
    logging.debug(e)
    return render_template('500.html', e=e), 500

