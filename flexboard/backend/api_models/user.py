"""
Pydantic Schema / Models

By creating these models, you are validating Request Bodies that are coming in.

When using FastAPI, you can have an argument inside the API endpoint function that is of type Pydantic Class!
- meaning if you use that class, you will have validation!

For EmailStr
- you must install this dependency
- will give us support for Email string only
"""

from pydantic import BaseModel, EmailStr, Field


# Request Body
class UserCreate(BaseModel):
    username: str = Field(
        ...,                        # required field: https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#required-with-ellipsis
        min_length=1,               # 1 min length
        max_length=30,              # 30 max length
        description='username',     # username
    )
    password: str = Field(...)

    # Must be of type EmailStr, no need to add =Field() but you can have lol,  but it will already have validation.
    email: EmailStr = Field(...)


# Response Body
class ShowUser(BaseModel):
    username: str
    email: str
    is_active: bool

    # Code below fixes the problem for the response model
    # It turns the incoming SQLAlchemy object into a dictionary!
    # I just created a new ShowUser object and returned that... seems more intuitive! Good to know though.

    # class Config():
    #     orm_mode = True
