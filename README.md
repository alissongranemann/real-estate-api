# Real Estate API

## Local setup

### Local environment

First of all, you need to install poetry. To do that, run

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

To get started you need Poetry's bin directory (\$HOME/.poetry/bin) in your `PATH`
environment variable. Next time you log in this will be done
automatically.

To configure your current shell run `source $HOME/.poetry/env`

This project uses `black` as the code formatter and `flake8` as the linter.
To add git-hooks on your enviroment, so you can run `black` and `flake8` on your project for every commit, please execute `pre-commit install`.

Also, you need to configurate the enviroment variables accordingly. Create `env` file in the project's root folder and set the variables following the `.env.example`.

In order to have the poetry packages in a local virtual environment (in the project root directory), run:

```bash
poetry config virtualenvs.in-project true
make install
```

### Development

You can always use Docker (recommended) to get those things isolated, in a container.
To create and start the container running on background, execute:

```bash
docker-compose up -d
```

To run the migrations, execute the command:

```bash
docker-compose exec flasky make migrate
```

Check the running application on your browser with the `http://127.0.0.1:8000/api/v1` url.
