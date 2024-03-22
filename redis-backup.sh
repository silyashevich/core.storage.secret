#!/bin/bash

docker exec core.storage.secret.redis redis-cli save
docker cp core.storage.secret.redis:/data/dump.rdb ./dump.rdb
