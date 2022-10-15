#!/bin/bash -x

python manage.py migrate --noinput
python manage.py collectstatic --no-input
python manage.py loaddata stat_types.json || exit 1
exec "$@"
