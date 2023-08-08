# Warning: bad config, jsut for quick test with --workers 1
import os
import sys

import celery
import click
import numpy
import pandas
import redis
import sqlalchemy
import flask
from flask import Flask

app = Flask(__name__)

REDIS_SOCKET = os.environ.get("REDIS_SOCKET") or ""
REDIS_HOST = os.environ.get("REDIS_HOST") or "localhost"
REDIS_PORT = int(os.environ.get("REDIS_PORT") or "6379")
REDIS_DB = 0


@app.route("/")
def hello_world():
    content = ["Hello World (0.1.2)"]
    content.append(redis_test())
    content.append(f"celery : {celery.__version__}")
    content.append(f"click : {click.__version__}")
    content.append(f"flask : {flask.__version__}")
    content.append(f"numpy : {numpy.__version__}")
    content.append(f"pandas : {pandas.__version__}")
    content.append(f"python : {sys.version}")
    content.append(f"sqlalchemy : {sqlalchemy.__version__}")

    return "<br>".join(content)


def redis_test() -> str:
    response = f"Redis v({redis.__version__}) "
    try:
        if REDIS_SOCKET:
            red = redis.Redis(unix_socket_path=REDIS_SOCKET)
        else:
            red = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        red.mset({"Croatia": "Zagreb", "France": "Paris"})
        capital = red.get("France")
        response += f"France: {capital}"
    except OSError as e:
        response = str(e)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0")
