Minimal flask app.

test:

    python -c 'import flapp'

run:

    gunicorn --workers 2 -b :8080 flapp.wsgi:app
