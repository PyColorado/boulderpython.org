.. _quickstart:

Quick Start
================

We suggest you follow the process of:

    #. Configuration
    #. Install Python Dependencies
    #. Build Static Assets
    #. Run Application
    #. Run Celery

Your first minutes with the Boulder Python application must be used to set the application
up for your environment. This documentation will help you understand how the application
is constructed and generally, how it works.

The application requires Python 3.6.


Configuration
-------------

.. warning:: You must replace these configuration values or the application will not run!

The following configuration values must be replaced or have their corresponding environment variables updated.
You can also opt to use a config file (see `section coming soon`).

Application
    - ``SITE_NAME`` (defaults to `boulderpython.org`)
    - ``SITE_ADMIN`` (defaults to `hi@boulderpython.org`)
    - ``SECRET_KEY`` (has default, but **you should change this**)

Database
    - ``SQLALCHEMY_DATABASE_URI`` (defaults to local Postgres Database)

Celery
    - ``CELERY_BROKER_URL`` (defaults to local RabbitMQ server)
    - ``CELERY_RESULT_BACKEND`` (defaults to local RabbitMQ server)

:ref:`SendGridConfig`
    - ``SENDGRID_API_KEY``
    - ``SENDGRID_DEFAULT_FROM``

:ref:`MeetupConfig`
    - ``MEETUP_KEY``
    - ``MEETUP_GROUP``

:ref:`MailChimpConfig`
    -  ``MAILCHIMP_API_KEY``
    -  ``MAILCHIMP_LIST_ID``
    -  ``MAILCHIMP_INTEREST_IDS``

:ref:`TrelloConfig`
    - ``TRELLO_API_KEY``
    - ``TRELLO_API_SECRET``
    - ``TRELLO_TOKEN``
    - ``TRELLO_TOKEN_SECRET``
    - ``TRELLO_ASSIGNEE``
    - ``TRELLO_HOOK``
    - ``TRELLO_BOARD``


Install Python Dependencies
---------------------------

Install python dependencies using ``pipenv``:

.. code-block:: bash

    $ pipenv sync -d

Initialize pre-commit hooks for auto-Black'ing (you should already have ``pre-commit`` installed in your system python):

.. code-block:: bash

    $ pre-commit install


Build Static Assets
-------------------

Install node dependencies then run ``gulp`` (you should already have `gulp.js`_ installed globally):

.. code-block:: bash

    $ npm install
    $ gulp



Running App
-----------

.. code-block:: bash

    $ flask runserver


Running Celery
--------------

.. code-block:: bash

    $ celery worker -A application.celery --loglevel=info



.. _gulp.js: https://gulpjs.com/