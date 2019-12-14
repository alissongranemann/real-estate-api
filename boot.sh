#!/bin/sh
make update
while true; do
    poetry run flask run --host=0.0.0.0
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Start command failed, retrying in 5 secs...
    sleep 5
done

# exec gunicorn -b :5000 --access-logfile - --error-logfile - flasky:app
