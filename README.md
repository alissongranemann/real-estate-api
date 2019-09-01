# Real Estate API

## Local setup

### Enviroment

First of all, you need to install all the dependencies. To do that, run

```bash
pip install -r requirements
```

This project uses `black` as the code formatter and `flake8` as the linter.
To add git-hooks on your enviroment, so you can run `black` and `flake8` on your project for every commit, please execute `pre-commit install`.

Also, you need to configurate the enviroment variables accordingly. Create `env` file in the project's root folder and set the variables following the `.env.example`.

### Database

In order to make this application runnable, you need to setup the database.
To start, install following packages (linux):

```bash
apt-get install postgresql-10 python-psycopg2 libpq-dev
```

To install postgresql, add postgres apt repository is required. The instructions are in [PostgreSQL](https://www.postgresql.org/download/)

Also, you need to create the real-state database. To do that, run the following command on psql:

```bash
create database real_state_dev
```

Or you can always use Docker (recommended) to get those things isolated, in a container.
To create and start the container running on background, execute:

```bash
docker-compose up -d db
```

To run the migrations, execute the command:

```bash
flask db upgrade
```

### Server

Run `python flasky.py` or `flask run` and check it on your browser with the `http://127.0.0.1:5000/api/v1` url.
