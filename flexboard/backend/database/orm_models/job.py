"""
This will be our Table class

We will not use hardcoded SQL
- we use SQLAlchemy ORM to create the table for us. Cool.


Why not raw SQL?
- there are syntax differences that may not work for all DB environment
- double quotes ( mysql, sqlite ) vs single quotes ( postgres )
- so, if SQLAlchemy creates it for us, we do not have to worry about those nuances.


The difference between this class and Entity Class in SpringBoot
- Completely different.
- We are creating tables in this instance, as well as linking the table to an object


Keyword: index=True
What is indexing in postgresql?
- Indexes are special lookup tables that the database search engine can use to speed up data retrieval.
- Simply put, an index is a pointer to data in a table.
- An index in a database is very similar to an index in the back of a book.

"""
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship

from database.base import Base

# from sqlalchemy.ext.declarative import as_declarative
# Base = as_declarative()


# inherit from Base class ( id, __name__, __table__ )
# @as_declarative will also bring in more attributes behind the scenes
# Not PLURAL, just Job class.
class Job(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    company = Column(String)
    company_url = Column(String)
    location = Column(String)
    description = Column(String)
    date_posted = Column(Date)

    # control the showing of job post, if active or not
    # to make sure the Job Posting has _some_ verification
    is_active = Column(Boolean, nullable=False, default=True)

    # foreign key to User table
    owner_id = Column(Integer, ForeignKey('user.id'))

    # "jobs" can be any name
    # "owner" variable will be a User object
    # "jobs" is a nickname that we are going to use ( will be used in models/users.py )
    # there exists a User for this job
    # like: user1.jobs
    # go to users.py | 'jobs' correlates to jobs variable | will show user who posted this job
    owner = relationship('User', back_populates='jobs')
