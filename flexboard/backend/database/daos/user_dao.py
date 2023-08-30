from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from api_models.user import UserCreate
from database.orm_models.user import User


class UserDao:
    # Create a new user in the Database!
    def create_new_user(self, user_create: UserCreate, bcrypt_hashed_password: str, db_session: Session) -> User:
        # User isn't a normal class object, there is no __init__ (the constructor) hence why we get the yellow highlights
        # User is NOT a normal class, this is a SQL Alchemy object, data will come from Database!
        # when creating the new user, there will be more properties added on!!
        # Like: id, metadata, registry, etc.!

        db_user: User = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=bcrypt_hashed_password,

            # We can't unpack user as shown below
            # **user.model_dump()

            # UserCreate contains an attribute that User does not have
            #   - password.

            # The attribute we _do_ have is 'hashed_password.'

            # The values below are auto-populated because they have default values in the Base class (database object)
            #   - is_active=True,
            #   - is_superuser=False,
        )

        # Raw SQL may look like INSERT()... | Do we implicitly start a transaction? Yes we do.
        # add() preps 'user' to be added to the database
        db_session.add(db_user)

        # commit() saves the 'user' to the database, only after commit() will SQLAlchemy fill in is_active, is_superuser, id, etc!
        db_session.commit()

        # refreshes the row of data for user, so we can grab the primary key, etc. TBH, this is NOT needed,
        db_session.refresh(db_user)

        return db_user

    def get_user_by_email_or_username(self, username_or_email: Optional[str], session: Session) -> Optional[User]:
        user: Optional[User] = session.query(User).filter(
            or_(
                User.username == username_or_email,
                User.email == username_or_email
            )
        ).first()
        return user


user_dao: UserDao = UserDao()
