# Chapter 6: OAuth2 Scopes, Token Expiry, and Advanced Authorization

In this chapter, we deepen our understanding of authorization by introducing:

* **OAuth2 scopes** for fine-grained access control
* **Token expiration and validation workflows**
* A conceptual overview of **refresh tokens** and **token rotation**
* An introduction to **third-party identity providers (IDPs)** like Google/Auth0

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
