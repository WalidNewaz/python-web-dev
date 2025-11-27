# Chapter 9: Django ORM and Advanced Queries

In this chapter, you will learn:

* How Django’s **ORM (Object-Relational Mapper)** works.
* How to define **models** for your Blog app.
* How to use **migrations** to keep the database schema in sync.
* How to run **basic and advanced queries** with the ORM.
* How to write **tests** for models and queries.

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