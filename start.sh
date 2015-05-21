#!/bin/sh

./redis-stable/src/redis-server &
python ./app.py