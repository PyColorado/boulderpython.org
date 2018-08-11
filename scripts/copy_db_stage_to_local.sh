#!/usr/bin/env bash -e
heroku pg:backups:capture --app boulder-python-staging
curl -k -o dump.sql `heroku pg:backups:public-url --app boulder-python-staging`
bash scripts/restore_from_dump.sh
