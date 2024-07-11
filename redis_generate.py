#!/usr/bin/env python
import argparse
import redis
import time
import uuid
from tqdm import tqdm



def connect_redis(conn_dict):
    conn = redis.StrictRedis(host=conn_dict['host'],
                             port=conn_dict['port'],
                             db=conn_dict['db'])
    return conn


def conn_string_type(string):
    try:
        host, portdb = string.split(':')
        port, db = portdb.split('/')
        db = int(db)
    except ValueError:
        format = '<host>:<port>/<db>'
        raise argparse.ArgumentTypeError(
            'incorrect format, should be: %s' % format)
    return {'host': host, 'port': port, 'db': db}


def generate_redis(source):
    src = connect_redis(source)
    srcPipe = src.pipeline()
    with tqdm(total=100000) as pbar:
        for i in range(100000):
            key = str(uuid.uuid4())
            srcPipe.set(key, "1")
            srcPipe.expire(key, 600)
            srcPipe.execute()
            pbar.update(1)
    return


if __name__ == '__main__':
    source = conn_string_type("127.0.0.1:6379/0")
    generate_redis(source)
