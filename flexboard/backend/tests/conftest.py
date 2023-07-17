# Configuration for Python Tests for this Application

import os
import sys
from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.api_routes import api_router
from database.base import Base
from database.orm_models.user import User
from database.session import get_database
from tests.test_utils import TestUtils

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# separating, so I can see what's inside here!

"""
Apparently, adding the directory name to sys.path is required for testing purposes: 
https://stackoverflow.com/questions/20971619/ensuring-py-test-includes-the-application-directory-in-sys-path
"""

_file = __file__
_abs_path = os.path.abspath(_file)
_dir_name = os.path.dirname(_abs_path)
_directory_name = os.path.dirname(_dir_name)
sys.path.append(_directory_name)

POSTGRES_DATABASE_URL = "sqlite:///./generated_test_db.db"  # -- this creates an actual file in your project folder. You can delete after.

# Use connect_args parameter only with sqlite (I do not have a clue on this nor do I care right now.)
engine = create_engine(POSTGRES_DATABASE_URL, connect_args={"check_same_thread": False})

test_session = sessionmaker(autoflush=True, bind=engine)


def start_application():
    app = FastAPI()
    app.include_router(api_router)
    return app


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(bind=engine)  # Create the tables.
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[test_session, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = test_session(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()  # if something failed, rolling back means it will not commit any pending operations in the transactions.
    connection.close()


# For tests, to use fixtures -- have app, and db_session as parameters in the test method.
@pytest.fixture(scope="function")
def client(app: FastAPI, db_session: test_session) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.

    Notice how none of the functions has () at the end of it.
    - We must not execute, but just pass the reference.
    """

    def _get_test_database():
        try:
            yield db_session
        finally:
            pass

    # This is how we test our database. We override the dependency injection. This is cool.
    # We do this in work code too.
    app.dependency_overrides[get_database] = _get_test_database
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def user_and_header_with_bearer_token(client, db_session):
    password: str = 'for_token'

    user: User = TestUtils.create_random_user(db_session, password=password)

    token_response = client.post(f"login/token", data={"username": user.username, "password": password})

    new_bearer_token: str = token_response.json().get('access_token')

    header_with_bearer_token: dict = {"Authorization": f"Bearer {new_bearer_token}"}

    return user, header_with_bearer_token
