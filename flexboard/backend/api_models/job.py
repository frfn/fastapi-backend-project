from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


# Inheritance: Base Pydantic Class for other Pydantic Classes
class JobBase(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    company_url: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = "Remote"
    date_posted: Optional[datetime] = datetime.now().date()
    is_active: Optional[bool]


# Request Body. JobCreate only requires 4 values after inheriting JobBase!
# We override because we're saying for this object, certain attributes MUST have a value.
class JobCreate(BaseModel):
    title: str
    company: str
    company_url: str
    description: str
    location: Optional[str] = "Remote"
    date_posted: Optional[datetime] = datetime.now().date()


class UpdateJob(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    company_url: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    date_posted: Optional[datetime] = None
    is_active: Optional[bool] = None
    owner_id: Optional[int] = None


# Response Body. ShowJob may not need to add anything.
class ShowJob(BaseModel):
    title: str
    company: str
    company_url: str
    description: str
    location: str
    date_posted: date
    is_active: bool

    # We will enable orm mode! Turns SQLAlchemy ORM Object into a dictionary.
    # Now we can return the SQLAlchemy ORM Object and expect the response model to be processed.
    # Serialization both works for normal Python Objects and SQLAlchemy objects!
    # It's only when we try to parse the SQLAlchemy ORM object INTO a Pydantic Model
    class Config:
        from_attributes = True
