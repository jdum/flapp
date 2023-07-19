# Warning: bad config, jsut for quick test with --workers 1
import os
import sys

import redis
from flask import Flask

app = Flask(__name__)

REDIS_HOST = os.environ.get("REDIS_HOST") or "localhost"
REDIS_PORT = int(os.environ.get("REDIS_PORT") or "6379")
REDIS_DB = 0


@app.route("/")
def hello_world():
    red = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    red.mset({"Croatia": "Zagreb", "France": "Paris"})
    capital = red.get("France")
    return (
        "Hello World\n"
        f"python version: {sys.version}\n"
        f"Redis ({redis.__version__}) capital: {capital}\n"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0")
