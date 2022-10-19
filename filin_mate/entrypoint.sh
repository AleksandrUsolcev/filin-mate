#!/bin/sh

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py loaddata stat_types.json
exec "$@"
