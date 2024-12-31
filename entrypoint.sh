#!/bin/bash

APP_ENV="${APP_ENV:-DEV}"

if [[ ! $APP_ENV =~ ^(DEV|TEST|PROD|LOCAL)$ ]]; then
  echo "Invalid APP_ENV: $APP_ENV. Allowed values are DEV, TEST, PROD, LOCAL."
  exit 1
fi

echo "Running in $APP_ENV environment"

if [ "$APP_ENV" == "LOCAL" ]; then
    echo "Authentication turned off"
fi

exec gunicorn --config gunicorn_conf.py --reload "wsgi:app(\"$APP_ENV\")"
