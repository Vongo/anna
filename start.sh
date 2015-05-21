#!/bin/sh

./src/web/redis-stable/src/redis-server &
python ./src/web/app.py