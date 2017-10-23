from flask import Flask
from flask_moment import Moment
from flask_cache import Cache

from config import config

app = Flask(__name__)


def configure(config_name='default'):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)


configure()

cache = Cache(app, config={
    'CACHE_TYPE': 'simple'
})
moment = Moment(app)
moment.init_app(app)

from .routes import *
