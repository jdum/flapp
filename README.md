Minimal flask app.

test:

    python -c 'import flapp'

run:
    install redis
    redis conf -> /etc/redis/6379.conf
    as root:
        redis-server /etc/redis/6379.conf


    gunicorn --workers 1 -b :8080 flapp.wsgi:app


    curl http://127.0.0.1:8080/

    Hello World
    python version: 3.10.6 (main, May 29 2023, 11:10:38) [GCC 11.3.0]
    Redis (4.6.0) capital: b'Paris'
