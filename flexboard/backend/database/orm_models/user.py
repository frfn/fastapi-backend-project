from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from database.base import Base


class User(Base):
    # index is used for fast search
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    username = Column(String, unique=True, nullable=False)

    # index=True | we will be using email for authentication
    email = Column(String, unique=True, nullable=False, index=True)

    # hashed password | probably b-crypt, salted password
    hashed_password = Column(String, nullable=False)

    # you can make user active through email verification, to complex
    is_active = Column(Boolean, default=True, nullable=False)

    # this will be able to control everything | an Admin
    is_superuser = Column(Boolean, default=False)

    # go to jobs.py | 'owner' correlates to owner variable | will show jobs this person has posted
    jobs = relationship('Job', back_populates='owner')
    # is relationship going to be a column? No, column() is not used.
