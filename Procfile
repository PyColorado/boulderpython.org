web: gunicorn "application:create_app('production')" --log-file -
celery: celery worker -A application.celery --loglevel=info
