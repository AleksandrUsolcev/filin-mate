#!/bin/bash -x

apt-get update
apt-get install nano
python main.py || exit 1
exec "$@"
