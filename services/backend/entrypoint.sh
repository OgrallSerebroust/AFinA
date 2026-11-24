#!/bin/bash

set -e

if [ -z "$1" ]
  then
    echo "No argument supplied"
    exit 1
elif [ $1 = "manage" ]
  then
    exec python manage.py "${@:2}"
    exit $?
elif [ $1 = "migrate" ]
  then
      python manage.py migrate
elif [ $1 = "pre-run" ]
  then
      python manage.py collectstatic --noinput
elif [ $1 = "run" ]
  then
    exec gunicorn --bind 0.0.0.0:8000 \
              --capture-output \
              --access-logfile - \
              --error-logfile - \
              --log-level info \
              --workers ${MICROSERVICE_N_WORKERS:-1} \
              --worker-class=common.uvicornworker.UvicornWorker \
              server.asgi:application
    exit $?
elif [ $1 = "dev" ]
  then
    # python manage.py migrate
    exec python manage.py runserver 0.0.0.0:8000
    exit $?
elif [ $1 = "celery" ]
  then
    exec celery -A server "${@:2}"
    exit $?
else
  echo "Invalid argument"
  exit 1
fi
