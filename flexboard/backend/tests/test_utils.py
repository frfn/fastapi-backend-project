import random
from typing import Optional

from sqlalchemy.orm import Session

from database.orm_models.user import User
from services.hash_service import hash_service


class TestUtils:
    # db_session is a fixture inside conftest.py
    @classmethod
    def create_random_user(cls, session: Session, password: Optional[str] = None) -> User:
        modified_password: str = 'Testington!1'
        if password:
            modified_password: str = password

        new_user: User = User(
            username='Flexer Testington' + str(random.randint(0, 9999)),
            hashed_password=hash_service.hash(modified_password),
            email='flexer@testington.com'
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)  # to get the id
        return new_user
