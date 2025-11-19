# Chapter 5: User Registration and Role-Based Authorization with FastAPI

This chapter builds on our authentication system from Chapter 4 by implementing:

* **User Registration**
* **Role-based authorization (RBAC)**
* An overview of **scopes and attribute-based access control (ABAC)**
* Best practices for securing endpoints based on user roles

## Preparation & Cleanup

The code from the earlier chapter was reorganized in order to introduce modularity in the design. 

```bash
app/
├── todo/
│   ├── schemas.py        # Pydantic request/response models
│   ├── entities.py       # Business/domain entities
│   ├── repository.py     # DB access
│   ├── service.py        # Business logic
│   ├── router.py         # FastAPI routes
│   └── __init__.py
├── auth/
│   ├── ...
├── core/
│   ├── config.py         # Application config
│   ├── constants.py      # Shared constants
│   ├── security.py       # Shared security ops
│   └── db.py             # DB connection (real/fake)
└── main.py               # Main entrypoint
```

Each module contains a `router.py` which contains the route handlers for the module. This is essentially the entry-point of the module.

```python
# ---- Router -----
router = APIRouter(prefix="/api/todos", tags=["ToDos"])
```

The routers are then registered with the main application as follows:

```python
# ---- Routers ----
from app.todos.router import router as todos_router

# ---- Todo CRUD Routes ----
app.include_router(todos_router)
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
