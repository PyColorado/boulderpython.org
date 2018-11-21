#!/usr/bin/env bash
# Fail immediately if an error occurs.
set -e
psql -c "DROP DATABASE IF EXISTS boulderpython;" postgres
psql -c "CREATE DATABASE boulderpython;" postgres

# Ignore errors here because we ALWAYS end up with warnings
pg_restore --verbose --clean --no-acl --no-owner -h localhost -d boulderpython dump.sql || true
