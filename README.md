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
we'd love to have you.  Submit your talk on [Papercall](https://papercall.io/boulder-python) to get the conversation
going!

### Organizers
Ian Douglas, ian@iandouglas.com, @iandouglas736 on [Twitter](https://twitter.com/iandouglas736), @iandouglas on
[Github](https://github.com/iandouglas)

Scott Vitale, scott@spigotlabs.com, @svvitale on [Twitter](https://twitter.com/svvitale), 
[Github](https://github.com/svvitale)

### Sponsors

[Galvanize Boulder](https://www.galvanize.com/boulder/campus) hosts our meetups and provides tasty food, beer, and 
refreshments (along with full stack and data science bootcamp programs).  Contact xxx to learn more.

[stream.io](https://getstream.io/) - Build Scalable Newsfeeds & Activity Streams

[Spigot Labs](http://spigotlabs.com/) - Add RFID to your beer, wine, and food festivals to track tastes and interactions 
between patrons and vendors.

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

### Testing

Please consider developing your project using TDD principles, it will make your life so much easier.

You can easily run the tests within PyCharm (my editor of choice), or you can run them from the command line:

```python run_tests.py```

The tests require access to the Google App Engine SDK.  You can specify the location of your installed SDK with an
environment variable:

Linux / MacOS:

```export GOOGLE_APP_ENGINE_SDK=${HOME}/google-cloud-sdk```

Windows:

```set GOOGLE_APP_ENGINE_SDK=C:\Program Files\Google\App Engine```

### What are the .haml files and .scss? Do I really need them?

I use HAML as a shortcut to writing properly-formatted HTML. You're welcome to remove them, but once you understand
the simplicity of HAML, I'm guessing you'll keep HAML around. While it's not very Pythonic, to get HAML working,
you'll need Ruby installed on your system and a simple "gem install haml" (possibly with sudo) should be all you need.

Likewise with the .scss files, they allow for writing nested CSS which them compiles down into semantically-correct
CSS files. You'll need to "gem install sass" (possibly with sudo)

I use PyCharm as my preferred Python editor, and the professional edition will detect the HAML and SCSS files and
prompt you to add "watchers" which will run the HAML/SCSS compilers for you whenever your files get saved. Any manual
changes you make to the .html or .css files will be lost when the compilers run.

The .haml and .scss files are ignored via the app.yaml file so they won't end up on App Engine as part of your deploy.
