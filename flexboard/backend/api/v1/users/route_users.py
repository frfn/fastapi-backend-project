from fastapi import APIRouter, Depends  # APIRouter - for routes / Depends - for Dependency Injection
from sqlalchemy.orm import Session  # Session is used for typing

from api_models.user import ShowUser, UserCreate
from database.orm_models.user import User
from database.session import get_database
from services.user_service import user_service

# Creating a router instance to signify that this file will be used as an API file | To be used in api/base.
# The prefix of this router will be '/user'
router: APIRouter = APIRouter()

"""
For response models:
- They must be a dictionary
- If you return a SQLAlchemy (ORM) object, and you specify the response model, it will cause Internal Server Error
    - Python cannot convert the SQLAlchemy (ORM) Object into a dictionary successfully.
    - orm_mode, a configuration you can turn on, can be used for the response model to handle objects and not dictionaries!
        - not recommended. Just return the object specified. orm_mode is not good. Convenient. Not good.
        
@router.post("/users") --> @router.post("/") -- why? the prefix, '/users', has been set in the api/api_routes.py class!
"""


@router.post("/create-user", response_model=ShowUser)
def create_user(user: UserCreate, db_session: Session = Depends(get_database)) -> ShowUser:
    new_user: User = user_service.create_new_user(user, db_session)

    show_user: ShowUser = ShowUser(
        username=new_user.username,
        email=new_user.email,
        is_active=new_user.is_active
    )

    return show_user
