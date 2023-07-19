# Warning: bad config, jsut for quick test with --workers 1
import os
import sys

import redis
from flask import Flask

app = Flask(__name__)


# Redis part

things = {
    "ref15": {
        "color": "red",
        "price": 50.0,
        "quantity": 100,
        "purchased": 0,
    },
    "rf12": {
        "color": "blue",
        "price": 60.0,
        "quantity": 50,
        "purchased": 0,
    },
}

HOST = os.environ.get("REDIS_HOST") or "localhost"
PORT = int(os.environ.get("REDIS_PORT") or "6379")


def init_redis_db():
    base = redis.Redis(host=HOST, port=PORT, db=0)
    with base.pipeline() as pipe:
        for ref, info in things.items():
            for field, value in info.items():
                pipe.hset(ref, field, value)
        pipe.execute()
    base.bgsave()


def get_quantity() -> str:
    base = redis.Redis(host=HOST, port=PORT, db=0)
    ref = "ref15"
    info = base.hgetall(ref)
    return info[b"quantity"].decode("utf8")


def test_db() -> bool:
    base = redis.Redis(host=HOST, port=PORT, db=0)
    ref = "ref15"
    zero = b"0"
    with base.pipeline() as pipe:
        try:
            pipe.watch(ref)
            nleft: bytes = base.hget(ref, "quantity")
            if nleft > zero:
                pipe.multi()
                pipe.hincrby(ref, "quantity", -1)
                pipe.hincrby(ref, "purchased", 1)
                pipe.execute()
                flag = True
            else:
                pipe.unwatch()
                flag = False
        except redis.WatchError:
            flag = False
    return flag


def init_redis():
    print(f"Init Redis host: {HOST}, port: {PORT}")
    init_redis_db()
    quantity1 = get_quantity()
    print(f"Init quantity1: {quantity1}")
    test_db()
    quantity2 = get_quantity()
    print(f"Init quantity2: {quantity2}")


# /Redis part

init_redis()


@app.route("/")
def hello_world():
    quantity = get_quantity()
    print(f"quantity: {quantity}")
    return (
        "Hello World\n"
        f"python version: {sys.version}\n"
        f"Redis ({redis.__version__}) quantity: {quantity}\n"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0")
