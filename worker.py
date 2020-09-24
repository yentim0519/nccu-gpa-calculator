import os

import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_url = os.getenv('redis://redistogo:bec8e321794ffa93fa51afcc703334e3@pike.redistogo.com:11600/', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()