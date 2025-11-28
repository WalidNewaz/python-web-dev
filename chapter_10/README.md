# Chapter 10: Django Admin

In this chapter, you will learn:

- What the Django Admin is
- How to enable access to the Django Admin
- Registering models with the admin
- Customizing the Admin Views
- Permissions and Access Control

## Install dependencies

```commandline
poetry install
```

## Run DB migrations

```commandline
poetry run python manage.py makemigrations blog
poetry run python manage.py migrate
```

## Launch app

Run the following command to launch the To Do API:

```commandline
cd blogsite
poetry run python manage.py runserver
```

## Run tests

```commandline
poetry run pytest
```