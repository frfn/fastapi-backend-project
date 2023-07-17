from typing import Optional

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from config import config_object

# Creating the factory for sessions
engine: Engine = create_engine(config_object.POSTGRES_DATABASE_URL)

# Creating the local session
session: sessionmaker = sessionmaker(bind=engine, autoflush=False)


# Why use yield in get_database() function?
# https://stackoverflow.com/questions/64763770/why-we-use-yield-to-get-sessionlocal-in-fastapi-with-sqlalchemy

# In try / finally, the `finally` clause will be executed first. THEN returning.
# This means we will have a closed database object. Not what we want.

# Flow of execution without yield:
#       `try` clause --> `finally` clause (will close the DB) --> `return` clause

# Flow of execution with yield:
#       `try` clause --> `yield` returns open DB Session --> `finally` clause

# If we use 'yield' instead of 'return' in this instance,
# We provide the DB object, use the open connection, THEN we hit the finally clause, closing the database.

# SQLAlchemy has a Connection Pooling mechanism by default.
# That means with yield you are creating a single session for each request.
# When you use return you are using a single database connection for all your app.


def get_database():
    database: Optional[Session] = None
    try:
        database: Optional[Session] = session()
        # `yield` returns a generator object. Depends() handles parsing out the Session object from the generator.
        # https://stackoverflow.com/questions/64763770/why-we-use-yield-to-get-sessionlocal-in-fastapi-with-sqlalchemy
        yield database
    finally:
        if database:
            database.close()
            print("Successfully closed the database.")
        else:
            print("Database could not be found.")


