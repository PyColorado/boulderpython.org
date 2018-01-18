web: gunicorn application:create_app() --log-file -
celery: celery worker -A application.celery --loglevel=info
