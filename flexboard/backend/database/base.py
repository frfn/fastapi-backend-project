from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


# If you make a Base class object, it can be interpreted properly by SQLAlchemy.

# Extending "Base" to other classes | https://docs.sqlalchemy.org/en/14/orm/declarative_tables.html
# - the `User` and `Job` tables will be created because we extend "Base" to their classes

# Decorators | https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/api.html

# By adding `@as_declarative`, we can have a `MetaData` object.
# Important as it will keep all the database metadata / information.

# We use Base for `Base.metadata.create_all(bind=engine)`.
# Since classes `Job` and `User` extends `Base`, when we call `create_all()` in `main.py`, it will create the tables.
# Read link below about `declarative_base()`, you will see why this structure is important.
@as_declarative()  # == declarative_base(): https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/api.html#sqlalchemy.ext.declarative.declarative_base
class Base:
    # Attributes.
    id: Any
    __name__: str

    # We do not need to declare table name for each class.
    # Must be __tablename__, not __table__, it will take the class name and return a String
    # Mark a class-level method as representing the definition of a mapped property or special declarative member name.
    @declared_attr  # this decorator must be here as shown in the documentation.
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
