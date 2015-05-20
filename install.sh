#!/bin/sh

sudo pip install flask
sudo pip install redis

wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
sudo make