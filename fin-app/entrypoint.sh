#!/bin/sh
set -e

poetry run python manage.py makemigrations
poetry run python manage.py migrate

exec "$@"