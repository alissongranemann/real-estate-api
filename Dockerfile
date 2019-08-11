FROM python:3.7-alpine

ENV FLASK_APP flasky.py
ENV FLASK_CONFIG production

RUN apk update && \
    apk add postgresql-dev gcc python3-dev musl-dev

RUN adduser -D flasky
USER flasky

WORKDIR /home/flasky

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY migrations migrations
COPY flasky.py config.py boot.sh ./

# run-time configuration
EXPOSE 5000
# ENTRYPOINT ["./boot.sh"]
