#!/bin/bash

if [[ -z $1 ]]; then
	echo "Please specify a Heroku app"
	exit 1
fi

heroku config --app $1 | sed -E 's/: +/=/' | grep -v "^="
