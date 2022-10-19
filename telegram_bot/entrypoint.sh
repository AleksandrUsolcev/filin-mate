#!/bin/sh

apt-get update
apt-get install nano
python main.py
exec "$@"
