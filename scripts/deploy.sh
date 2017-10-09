#!/usr/bin/env bash

# Decrypt the credentials we added to the repo using the key we added with the Travis command line tool
openssl aes-256-cbc -K $encrypted_985474bef3df_key -iv $encrypted_985474bef3df_iv -in client-secret.json.enc -out client-secret.json -d

# Here we use the decrypted service account credentials to authenticate the command line tool
gcloud auth activate-service-account --key-file client-secret.json
gcloud -q app deploy app.yaml --promote --verbosity=info
