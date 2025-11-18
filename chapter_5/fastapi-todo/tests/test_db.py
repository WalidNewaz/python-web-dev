from app import db
from app.auth_service import verify_password

def test_fake_user_db_structure():
    assert "alice" in db.fake_users_db
    alice = db.fake_users_db["alice"]
    assert "username" in alice
    assert "hashed_password" in alice
    assert verify_password("wonderland", alice["hashed_password"])

def test_todos_initial_state():
    assert isinstance(db.todos, list)
    assert db.todos == []
    assert isinstance(db.next_id, int)
    assert db.next_id == 1
