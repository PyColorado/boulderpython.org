#!/usr/bin/env bash -e
heroku pg:copy boulder-python::DATABASE_URL DATABASE_URL -a boulder-python-staging --confirm boulder-python-staging
