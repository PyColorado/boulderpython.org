Config
===============

The application config must be setup to properly run thi application.

This application integrates the following third-party services:

 - :ref:`SendGridConfig`
 - :ref:`MeetupConfig`
 - :ref:`MailChimpConfig`
 - :ref:`TrelloConfig`

Additionally we use the following resources, and need to configure their access.

 - Postgres (via SQLAlchemy)
 - RabbitMQ (via Celery), `this can be replaced with Redis`


.. _SendGridConfig:

SendGrid
--------------------

For transactional email integration we use `SendGrid`_. Obtain an API key and replace the following
values in ``config.py`` (or update their conterpart environment variables):

    - ``SENDGRID_API_KEY``: Your SendGrid API key.
    - ``SENDGRID_DEFAULT_FROM``: Your default "from" email; ex: ``'Boulder Python <hi@boulderpython.org>'``

To easily integrate SendGrid we use the `flask-sendgrid`_ extension


.. _MeetupConfig:

Meetup
------

To easily integrate data about upcoming Meetups, we use the `Meetup API`_. Integration is really simple,
just retrieve your API Key for Meetup.com and replace the following:

    - ``MEETUP_KEY``: your Meetup API key.
    - ``MEETUP_GROUP``: the name of your Meetup (called its URL name). For instance, ours is ``BoulderPython`` and can be seen in our meetup URL: https://meetup.com/**BoulderPython**.


.. _MailChimpConfig:

MailChimp
---------

Our newsletter lives on `MailChimp`_. So we integrate a simple subscribe with out application.

To enable this, update these 3 config values:

    - ``MAILCHIMP_USERNAME``: your MailChimp account's username
    - ``MAILCHIMP_API_KEY``: your MailChimp API Key
    - ``MAILCHIMP_LIST_ID``: the MailChimp list you wish to add new subscribers to


.. _TrelloConfig:

Trello
------

Since our entire submission process is publicly viewable on our `Trello Submissions Board`_ we need to integrate
Trello into our application. We have to setup a considerable amount of configuration values to properly setup
our Trello integration.

First, the Trello authentication keys: ``TRELLO_API_KEY``, ``TRELLO_API_SECRET``, ``TRELLO_TOKEN``, ``TRELLO_TOKEN_SECRET``.
Trello makes it easy to obtain your keys and token secrets: use their `5 Minute Guide`_ to get started.

.. warning:: Keep your API and Token keys/secrets safe!

Additionally, we must setup a private ``TRELLO_ASSIGNEE`` value. This is the id of the user you wish to assign to each new
card (submission).

Lastly, we have some additional values to setup in order to complete our integration. These don't have to be hidden in
environment variables because they're already public and not really a risk.


    - ``TRELLO_HOOK``: this is just a URL pointing back to your app's root URL plus the Trello hook path; example: https://boulderpython.ngrok.io/trello/hook
    - ``TRELLO_BOARD``: the ID of your "Submissions" board
    - ``TRELLO_LISTS``: dictionary containing the names and IDs of the lists on our **board**.
    - ``TRELLO_LABELS``: dictionary containing the IDs of the labels on our **board** and **lists**.

TRELLO_LISTS
    On our Submissions board there are 4 lists, and they correspond to the 4 queues of our submission process:

        #. **New**
        #. **In-Review**
        #. **Scheduled**
        #. **Archived**

    Here's an example of how our lists are configured in ``config.py``:

    .. code-block:: python

        TRELLO_LISTS = {
            'NEW': {
                "id": "5a0091836c98d9743f94b363",
                "text": "New"
            },
            'REVIEW': {
                "id": "5a0091836c98d9743f94b364",
                "text": "In Review"
            },
            'SCHEDULED': {
                "id": "5a0091836c98d9743f94b365",
                "text": "Scheduled"
            }
        }

TRELLO_LABELS
    Our card lists have a set of labels that correspond to both the format and audience of each talk submission. We configured
    our submission form to apply the correct labels based on the submitters specification for their talk.

    FORMAT
        #. **IN-DEPTH**
        #. **LIGHTNING**
        #. **DEMO**
        #. **BEGINNER**

    AUDIENCE
        #. **BEGINNER**
        #. **INTERMEDIATE**
        #. **ADVANCED**

    Here's an example of how our labels are configured in ``config.py``:

    .. code-block:: python

        TRELLO_LABELS = {
            "FORMAT": {
                "IN-DEPTH": "5a0094fca8e476f047706616",
                "LIGHTNING": "5a00950b73846ef08844501e",
                "DEMO": "5a0095201f007932c3ea53d0",
                "BEGINNER": "5a0095307b5c511544f1447b"
            },
            "AUDIENCE": {
                "BEGINNER": "5a0091839ae3d60b0c9e04af",
                "INTERMEDIATE": "5a0091839ae3d60b0c9e04b1",
                "ADVANCED": "5a0091839ae3d60b0c9e04b0"
            }
        }

.. note:: See the selectbox options in ``forms.py`` to see how these are related in the Submission form.


.. _SendGrid: https://sendgrid.com
.. _flask-sendgrid: https://github.com/frankv/flask-sendgrid
.. _Meetup API: https://www.meetup.com/meetup_api/
.. _MailChimp: https://mailchimp.com
.. _Trello Submissions Board: https://trello.com/b/wm8hatnW/submissions
.. _5 Minute Guide: http://https://trello.readme.io/docs/get-started