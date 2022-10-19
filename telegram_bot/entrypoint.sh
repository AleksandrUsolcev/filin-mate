#!/bin/sh

apt-get update
apt-get install nano
pip3 install -r /app/requirements.txt --no-cache-dir
python main.py
exec "$@"
