import pytest
from app.models import TodoItem, TodoCreate
from pydantic import ValidationError

def test_todo_model_valid():
    todo = TodoItem(id=1, title="Write tests")
    assert todo.completed is False

def test_todo_model_invalid():
    with pytest.raises(ValidationError):
        TodoItem(id="abc", title="")

def test_todo_model_invalid_title():
    with pytest.raises(ValidationError):
        TodoItem(id=1, title=1)

def test_todo_create_valid():
    created_todo = TodoCreate(title="Write tests")
    assert created_todo.title == "Write tests"

def test_todo_create_invalid():
    with pytest.raises(ValidationError):
        TodoCreate(title="")

def test_todo_create_invalid_title():
    with pytest.raises(ValidationError):
        TodoCreate(title=1)