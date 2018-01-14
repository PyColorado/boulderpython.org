# Boulder Python Website

[![Build Status](https://travis-ci.org/boulder-python/boulderpython.org.svg?branch=master)](https://travis-ci.org/boulder-python/boulderpython.org)

Our website grew out of @iandouglas's [Flask + Google App Engine template](https://github.com/iandouglas/flask-gae-skeleton).
What kind of Python community would we be if our site wasn't also developed using Python?? :)


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

Our community has implemented the PyCon ["Code of Conduct"](https://us.pycon.org/2017/about/code-of-conduct/) for ensuring
all members attending our sessions, meetups, and events feel included and heard. Thanks for your mutual respect to one
another.

## Website Contributions

We welcome contributions, changes, and corrections to our website.  Please submit a pull request (with tests) as
outlined below.

### Google SDK Requirements

You'll need to install the Google Cloud SDK and the app-engine-python component:

```bash
# Install the Google Cloud SDK
curl https://sdk.cloud.google.com | bash

# Install the Python App Engine component
gcloud components install app-engine-python
```

### virtualenv

I recommend installing an actual virtualenv for your project, but App Engine will also need your external packages
installed in the /lib/ folder here. Remember that App Engine can only support 100% Python packages. Anything that
compiles a C/C++ library cannot be used on GAE.

```bash
# Create new virtualenv
virtualenv boulder-python

# linux/mac:
boulder-python/bin/activate

# windows:
boulder-python\scripts\activate

# install all requirements into your virtualenv
pip install -r requirements.txt

# install all requirements into your /lib/ folder as well, but only the packages
# this is necessary because packages need to be sent to App Engine as well
pip install -r requirements.txt -t lib
```

### Running

As of 2018, the Flask application features a few new integrations. Notably, they're the [Meetup API](https://www.meetup.com/meetup_api/)
and [MailChimp](https://mailchimp.com/) integrations. We want to keep this project public, so we have to be careful with
our API keys. To get around this, we use a simple config file, here's how we set it up:

 1. Create a file called `local.cfg` in the application package root.
 2. Add the following to it with your API keys.
 3. **DON'T** commit this file

```
SECRET_KEY = 'your-secret-key'
MEETUP_KEY = 'your-meetup-api-key'
MAILCHIMP_USERNAME = 'mc-username'
MAILCHIMP_API_KEY = 'mc-api-key'
MAILCHIMP_LIST_ID = 'mc-list-id'
```

To run the application now, use:

```
$ APP_CONFIG=local.cfg python run.py
```


### Testing

Please consider developing your project using TDD principles, it will make your life so much easier.

You can easily run the tests within PyCharm (my editor of choice), or you can run them from the command line:

```python run.py -t```

The tests require access to the Google App Engine SDK.  You can specify the location of your installed SDK with an
environment variable:

Linux / MacOS:

```export GOOGLE_APP_ENGINE_SDK=${HOME}/google-cloud-sdk```

Windows:

```set GOOGLE_APP_ENGINE_SDK=C:\Program Files\Google\App Engine```


### Building Static Assets

With the new redesign, our static asset files (js and css) have changed. We're still using SASS, but now the project
relies on gulp and npm to build and minify both scss files, but also JavaScript.

With npm and gulp installed, simply run:
```
$ gulp
```

The default gulp command builds scss and concatenates scripts into `app.css`, and `app.js`, respectively. It will also
begin the gulp watch command so if you save any changes in your scss and js files, gulp rebuilds them automatically.