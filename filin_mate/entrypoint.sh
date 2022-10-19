#!/bin/sh

pip3 install -r /app/requirements.txt --no-cache-dir
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py loaddata stat_types.json
gunicorn filin_mate.wsgi:application --bind 0:8000
exec "$@"
