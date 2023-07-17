# This class must exist. Else the tables will not be created.

# This file collects all the classes that extends the `Base` in `base.py`

# `User` and `Job` extends Base, that's why it's here.
# This is how SQLAlchemy works. This is the file that we

from database.base import Base
from database.orm_models.user import User
from database.orm_models.job import Job
