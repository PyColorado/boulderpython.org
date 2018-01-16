Gunicorn
===============

Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX. It's a pre-fork worker model.
The Gunicorn server is broadly compatible with various web frameworks, simply implemented,
light on server resources, and fairly speedy.

boulderpython.org uses gunicorn to be more adaptable when being deployed to server environments.

.. Gunicorn's logging configuration can be found in ``app/confg/logging.cfg``. The logging configuration
.. catches only error, or above, level logging output and uses JSON formatting for log messages.


Starting/Stopping gunicorn
--------------------------

Refer to the ``Procfile`` for the proper command used to start gunicorn, currently:

.. code-block:: bash

    gunicorn --log-config config/logging.cfg --config config/gunicorn.py wsgi:app --preload


* ``--log-config``: sets the logging configuration from a file
* ``--config``: sets the gunicorn configuration from a file
* ``wsgi:app``: tells gunicorn which module and object to call for our application
* ``--preload``: loads application code before the worker processes are forked


Stopping a Run-Away Gunicorn Process
""""""""""""""""""""""""""""""""""""

If an error causes your gunicorn workers to keep spawning (or you simply spawned too many), you
can try the following to kill them all in one go:

.. code-block:: bash

    kill -9 `ps aux |grep gunicorn |grep wsgi | awk '{ print $2 }'`


Gunicorn Configuration
----------------------


Server Socket
""""""""""""""""

 * ``bind`` - The socket to bind.

        A string of the form: ``HOST``, ``HOST:PORT``, ``unix:PATH``. An IP is a valid HOST.

 * ``backlog`` - The number of pending connections.

        This refers to the number of clients that can be waiting to be served.
        Exceeding this number results in the client getting an error when attempting
        to connect. It should only affect servers under significant load.

Worker processes
""""""""""""""""

* ``workers`` - The number of worker processes that this server should keep alive for handling requests.

        A positive integer generally in the 2-4 x $(NUM_CORES)
        range. You'll want to vary this a bit to find the best
        for your particular application's work load.

* ``worker_class`` - The type of workers to use.

        The default sync class should handle most 'normal' types of work
        loads. You'll want to read
        http://docs.gunicorn.org/en/latest/design.html#choosing-a-worker-type
        for information on when you might want to choose one
        of the other worker classes.

        A string referring to a Python path to a subclass of
        gunicorn.workers.base.Worker. The default provided values
        can be seen at
        http://docs.gunicorn.org/en/latest/settings.html#worker-class

* ``worker_connections`` - For the eventlet and gevent worker classes

        This limits the maximum number of simultaneous clients that
        a single process can handle.

        A positive integer generally set to around 1000.

* ``timeout`` - If a worker does not notify the master process in this number of seconds it is killed and a new worker is spawned to replace it.

        Generally set to thirty seconds. Only set this noticeably
        higher if you're sure of the repercussions for sync workers.
        For the non sync workers it just means that the worker
        process is still communicating and is not tied to the length
        of time required to handle a single request.

* ``keepalive`` - The number of seconds to wait for the next request on a Keep-Alive HTTP connection.

        A positive integer. Generally set in the 1-5 seconds range.