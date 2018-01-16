Management
===============

The application management commands reside in ``run.py``, but you use the cli command ``flask``
to invoke application processes.


Running the Development Server
------------------------------

To run the development server, use ``flask runserver``

.. code-block:: bash

    $ flask runserver --help
    Usage: flask runserver [OPTIONS]

      Shortcut to ``flask run``

    Options:
      --reload  run application with livereload
      --help    Show this message and exit.

Optional args for runserver are:

    - ``--reload`` development server uses `livereload`_ (app runs on ``localhost:9999`` by default)

The application still accepts a config overide via the env var: ``FLASK_CONFIG``, so to start the
application with your specified config use: ``FLASK_CONFIG=local.cfg flask runserver``


Initialize Application Database
-------------------------------

To initialize the database, use ``flask initdb``. Currently there are no optional arguments to initdb.


.. code-block:: bash

    $ flask initdb --help
    Usage: flask initdb [OPTIONS]

      Creates the database tables.

    Options:
      --help  Show this message and exit.



Running Tests
------------------------------

To run the unit tests, use ``flask test``.

.. code-block:: bash

    $ flask test --help
    Usage: flask test [OPTIONS]

    Options:
      -v       Increase verbosity while testing.
      -x       Exit after first failure.
      -rs      Enables skipped test report.
      -cov     Enable code coverage.
      -flake8  Enable pep8 and pyflakes testing.
      --help   Show this message and exit.


Optional args for test are:

    - ``-v`` increases verbosity on py.test output
    - ``-x`` exits after first failure
    - ``-rs`` enables skipped test report
    - ``-cov``  enables code coverage
    - ``-flake8`` enables pep8 and pyflakes testing via `flake8`_


.. _flake8: http://flake8.pycqa.org/en/latest/
.. _livereload: https://livereload.readthedocs.io/en/latest/