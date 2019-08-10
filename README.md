# Real State API

## Local setup

In order to make this application runnable, you need to install the following packages (linux):

```bash
apt-get install postgresql-10 python-psycopg2 libpq-dev
```

To install postgresql, add postgres apt repository is required. The instructions are in https://www.postgresql.org/download/

Also, create the real-state database is needed. To do that, run the following command on psql:

```bash
create database real_state_dev
```

Or you can always use Docker (recommended) to get those things isolated, in a container.

To run the application, install the dependencies running:

```bash
pip install -r requirements
```

Add a virtual enviroment for python's packages in the root directory to isolate the dependencies is always a good alternative.

Configurate the enviroment variables accordingly on `env` file, following the `.env.example`.

After all the previous steps are finished, run `python app.py` and check it on your browser with the `http://127.0.0.1:5000/` url.
