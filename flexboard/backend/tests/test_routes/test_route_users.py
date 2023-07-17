# We will use pytest for testing
import json

from database.orm_models.user import User
from services.user_service import user_service
from tests.test_utils import TestUtils

"""
Tests for route_users.py

Takeaways:

- We can access 'client' because it is a fixture in conftest.py
- For any file under the folder /tests, it will have access to client
"""

ROUTE_USERS = '/users'


def test_create_user(client):
    data: dict = {
        "username": "test_username",
        "email": "test_username@email.com",
        "password": "test_password"
    }

    json_data: str = json.dumps(data)

    """
    You must use:
        json_data = json.dumps(data) -- if you're going to use 'data='
    
    else you must use:
        json=data
        
    'json=' will convert the dictionary into a JSON object automatically
    """
    response = client.post(f"{ROUTE_USERS}/create-user", data=json_data)

    expected_json: dict = {
        'username': 'test_username',
        'email': 'test_username@email.com',
        'is_active': True
    }

    # 200 means it is okay! Successful!
    # 4XX means wrong on client side
    # 5XX means wrong on our side
    assert response.status_code == 200
    assert response.json() == expected_json


def test_get_user_by_email(db_session):
    user: User = TestUtils.create_random_user(db_session)
    retrieved_user: User = user_service.get_user_by_email_or_username(user.email, db_session)
    assert user.email == retrieved_user.email
