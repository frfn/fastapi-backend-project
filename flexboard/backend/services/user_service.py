from typing import Optional

from sqlalchemy.orm import Session

from api_models.user import UserCreate
from database.daos.user_dao import UserDao, user_dao
from database.orm_models.user import User
from services.hash_service import HashService, hash_service


class UserService:
    def __init__(self, user_dao_param: UserDao, hash_service_param: HashService):
        self.user_dao = user_dao_param
        self.hash_service = hash_service_param

    def create_new_user(self, user_create: UserCreate, db_session: Session) -> Optional[User]:
        user: User = self.user_dao.create_new_user(user_create, db_session)

        if not user:
            return None

        return user

    def get_user_by_email_or_username(self, username_or_email: str, session: Session) -> Optional[User]:
        user: User = self.user_dao.get_user_by_email_or_username(username_or_email, session)

        if not user:
            return None

        return user

    def authenticate_user(self, plain_password: str, hashed_password: str) -> bool:
        return self.hash_service.verify_password(plain_password=plain_password, hashed_password=hashed_password)


user_service: UserService = UserService(user_dao, hash_service)
