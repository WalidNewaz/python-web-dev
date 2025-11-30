# Chapter 11: Working with Relational Databases

In this chapter, you will learn:

* How to use **SQLAlchemy** with FastAPI for relational data.
* How to use the **Django ORM** for advanced queries.
* How to manage schema changes with **Alembic** (FastAPI) and **migrations** (Django).
* How to implement **CRUD operations** that persist to a database.
* How to write **tests** for database-backed APIs.

## Install dependencies

```commandline
poetry install
```

## Launch app

Run the following command to launch the To Do API:

```commandline
cd fastapi-todo
poetry run uvicorn app.main:app --reload
```

## Run tests

```commandline
poetry run pytest
```
