#!/usr/bin/env bash -e
heroku pg:backups:capture --app boulder-python
curl -k -o dump.sql `heroku pg:backups:public-url --app boulder-python`
bash scripts/restore_from_dump.sh
