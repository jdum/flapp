# Warning: bad config, jsut for quick test with --workers 1
import os
import sys

import redis
import sqlalchemy
from flask import Flask

app = Flask(__name__)

REDIS_SOCKET = os.environ.get("REDIS_SOCKET") or ""
REDIS_HOST = os.environ.get("REDIS_HOST") or "localhost"
REDIS_PORT = int(os.environ.get("REDIS_PORT") or "6379")
REDIS_DB = 0


@app.route("/")
def hello_world():
    if REDIS_SOCKET:
        red = redis.Redis(unix_socket_path=REDIS_SOCKET)
    else:
        red = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    red.mset({"Croatia": "Zagreb", "France": "Paris"})
    capital = red.get("France")
    return (
        "Hello World\n"
        f"python version: {sys.version}\n"
        f"Redis ({redis.__version__}) capital: {capital}\n"
        f"sqlalchemy ({sqlalchemy.__version__})\n"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0")
