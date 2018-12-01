# Boulder Python Website

[![Build Status](https://travis-ci.org/boulder-python/boulderpython.org.svg?branch=master)](https://travis-ci.org/boulder-python/boulderpython.org)
[![Coverage Status](https://coveralls.io/repos/github/boulder-python/boulderpython.org/badge.svg?branch=master)](https://coveralls.io/github/boulder-python/boulderpython.org?branch=master)
[![Docs](https://readthedocs.org/projects/boulderpythonorg/badge/?version=latest)](http://boulderpythonorg.readthedocs.io/en/latest/?badge=latest)

Our website grew out of @iandouglas's [Flask + Google App Engine template](https://github.com/iandouglas/flask-gae-skeleton).
What kind of Python community would we be if our site wasn't also developed using Python?? :)

Official Documentation: [boulderpythonorg.readthedocs.io](https://boulderpythonorg.readthedocs.io)


## A Community in Progress

We are a group of python developers, scientists, automators, and enthusiasts that gather once a month in Boulder,
Colorado to discuss all things python.  We usually meet on the 2nd Tuesday of each month.  You can find and engage with
us on [Meetup](https://www.meetup.com/boulderpython/), [Twitter](https://twitter.com/boulderpython), and
[Slack](https://denver-dev-slack.herokuapp.com/) (#meetup-python)
and (#help-python).


### Speak at a Meetup

We're always looking for speakers at our meetups.  Whether you have a short talk, long talk, or just an idea for a talk,
we'd love to have you.  Submit your talk directly on [boulderpython.org](https://boulderpython.org/submit).


### Organizers
Scott Vitale, scott@spigotlabs.com, @svvitale on [Twitter](https://twitter.com/svvitale),
[Github](https://github.com/svvitale)

Zoë Farmer, zoe@dataleek.io, @TheDataLeek on [Twitter](https://twitter.com/TheDataLeek),
[Github](https://github.com/thedataleek)

Frank Valcarcel, frank@cuttlesoft.com, @fmdfrank on [Twitter](https://twitter.com/fmdfrank), @frankV on
[Github](https://github.com/frankv)


### Sponsors

[Galvanize Boulder](https://www.galvanize.com/boulder/campus) hosts our meetups and provides tasty food, beer, and
refreshments (along with full stack and data science bootcamp programs).  Contact xxx to learn more.

[Spigot Labs](http://spigotlabs.com/) - Add RFID to your beer, wine, and food festivals to track tastes and interactions
between patrons and vendors.

[Cuttlesoft](https://www.cuttlesoft.com/) - Cuttlesoft is a custom software agency. They craft beautifully designed and
highly scalable solutions for web, mobile, IoT, and the cloud.


## Code of Conduct

Our community has implemented the PyCon ["Code of Conduct"](https://us.pycon.org/2018/about/code-of-conduct/) for ensuring
all members attending our sessions, meetups, and events feel included and heard. Thanks for your mutual respect to one
another.

## Website Contributions

We welcome contributions, changes, and corrections to our website. Please submit a pull request.

### Running

As of 2018, the Flask application features a few new integrations. Notably, they're the [Meetup API](https://www.meetup.com/meetup_api/),
[Trello](https://trello.com), and [MailChimp](https://mailchimp.com/) integrations. We want to keep this project public, so we have to be careful with
our API keys. To get around this, we use a simple config file, here's how we set it up:

 1. Copy the `local-example.cfg` and fill it with your API Keys and settings.
 2. Be careful **NOT** to commit this file into your fork/repo

To run the application now, use:

```
$ FLASK_CONFIG=local.cfg flask runserver
```


### Testing

You can easily run the tests suite from the command line:

```py.test test```

pytest has a set of optional arguments that can enable many options and plugins.

Here are some we recommend:

    - `-v/--verbose` increases verbosity on py.test output
    - `-x` exit after first failure
    - `-rs` enables skipped test report
    - `--cov` enables code coverage
    - `--flake8` enables pep8 and pyflakes testing via [flake8](http://flake8.pycqa.org/en/latest/)

For example, our test run uses:
```
$ py.test tests --verbose --cov --cov-report term-missing --flake8 application
```

Check out pytest's [usage docs](https://docs.pytest.org/en/latest/usage.html).


### Building Static Assets

With the new redesign, our static asset files (js and css) have changed. We're still using SASS, but now the project
relies on gulp and npm to build and minify both scss files, but also JavaScript.

With npm and gulp installed, simply run:
```
$ gulp
```

The default gulp command builds scss and concatenates scripts into `app.css`, and `app.js`, respectively. It will also
begin the gulp watch command so if you save any changes in your scss and js files, gulp rebuilds them automatically.


### Celery

We now use Celery to handle Trello webhooks and send out emails to speakers.

Celery requires a task broker. Either RabbitMQ or Redis are good choices.

To run Celery, use the following command:
```
$ FLASK_CONFIG=local.cfg flask celeryd
```


### Pre-Commit Hooks

Initialize pre-commit hooks for auto-Black'ing (you should already have ``pre-commit`` installed in your system python):
```
$ pre-commit install
```