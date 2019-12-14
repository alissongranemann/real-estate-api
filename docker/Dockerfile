FROM python:3.7-alpine

ENV FLASK_APP flasky.py
ENV FLASK_CONFIG production

RUN apk update && \
    apk add postgresql-dev gcc python3-dev build-base musl-dev bash curl

# install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH /root/.poetry/bin:$PATH

COPY . /srv/app
WORKDIR /srv/app

RUN poetry config virtualenvs.create false && \
    poetry config virtualenvs.in-project false
RUN make install

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]
