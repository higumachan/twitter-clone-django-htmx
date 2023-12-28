# twitter-clone-django-htmx README

Python Boilerplate contains all the boilerplate you need to create a Python package.

## Local Development

- Python
- docker-compose


> Requires [pipenv](https://pipenv.readthedocs.io/en/latest/) for dependency management
> Install with `pip install pipenv --user`



### Install the local development environment

1. Setup `pre-commit` hooks (_black_, _isort_):

    ```bash
    # assumes pre-commit is installed on system via: `pip install pre-commit`
    pre-commit install
    ```

2. The following command installs project and development dependencies:

    ```bash
    pipenv install --dev
    ```

### Add new packages

From the project root directory run the following:
```
pipenv install {PACKAGE TO INSTALL}
```

 ## Run code checks

 To run linters:
 ```
 # runs flake8, pydocstyle
 make check
 ```

To run type checker:
```
make mypy
```

## Running tests

This project uses the [django test framework](https://docs.djangoproject.com/en/2.2/topics/testing/) for running testcases.

Tests cases are written and placed in the `tests` directory of_each_ related django application.

To run the tests use the following command:
```
# bring update postgres/localstack environment
docker-compose up -d

# enter venv
pipenv shell
cd twitter_clone_django_htmx
python manage.py test
```

> In addition the following `make` command is available:

```
make test
```

## Environment Variables

- DB_NAME
- DB_USER
- DB_PASS
- DB_HOST
- DB_PORT
