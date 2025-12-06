from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.core.db import Base, get_db
from app.main import app
from app.core.security import get_password_hash
from app.users.entities import UserEntity as User

TEST_DB_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_test_app():
    """Factory to return a fresh TestClient with DB overrides."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # IMPORTANT: Set overrides BEFORE creating TestClient
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


# def seed_test_user():
#     """Adds a test user to the DB."""
#     db = TestingSessionLocal()
#     user = User(
#         id=1,
#         username="alice",
#         hashed_password=get_password_hash("wonderland"),
#         name="Alice Sharpe",
#         email="asharpe@example.com",
#         role="user",
#         scopes=["read", "write"],
#         disabled=False,
#     )
#     db.add(user)
#     db.commit()
#     db.close()
