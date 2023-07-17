from typing import Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.sql import update, Update, delete, Delete

from api_models.job import JobCreate, UpdateJob
from database.orm_models.job import Job
from database.orm_models.user import User


# FLUSH vs COMMIT
# Why flush / commit at all?
# - This is how you interact with the database
# - If you do .add(something_here), it won't be added to the database at all,
#   - it will save to the queue
#   - You must use flush(then commit) OR just commit to communicate the changes to the db.
#
# Flush
# - Will not fully commit the changes to the database, you still need to call commit.
#   Ex. User wants to upload 5 files, we can flush them, and just temporarily add them as pending operations in a transaction.
#
#   Note: You STILL MUST commit() the changes if you're using flush. Flush is always called as a part of a call to commit.
#
#   https://stackoverflow.com/questions/4201455/sqlalchemy-whats-the-difference-between-flush-and-commit
#
# Commit (aka. persists)
# - Will permanently commit the change to the database
#   This will commit the changes into the database.

# From Work:
# - It's better to return Pydantic Models instead of SQLAlchemy ORM Models.
#   Note: We can only do this because orm_mode = True, tbh, orm_mode is not good.
#
#    - We will be leaking ORM models which is NOT good since they are powerful objects that can run persistence operations.


class JobDao:
    def create_new_job(self, job: JobCreate, owner_id: int, session: Session) -> Job:
        # We create Job object because this is a SQLAlchemy object, it can interact with the database for us.
        # I personally do not like doing it this way.

        # As shown below, we can unpack with the double asterisk (**) method.
        # db_job = Job(
        #     title=job.title,
        #     company=job.company,
        #     company_url=job.company_url,
        #     description=job.description,
        #     owner_id=owner_id
        # )

        # These yellows are incorrectly here, PyCharm is thinking that there is no __init__ method for Job class!
        #  the base class IS annotated with as_declarative() which in turns makes possible.
        db_job: Job = Job(**job.model_dump(), owner_id=owner_id)

        # This new Base class object (an ORM object) can now be interpreted by the db_session.
        # add, commit, refresh, return | go to repository/users.py to see what these are!
        session.add(db_job)
        session.commit()
        session.refresh(db_job)  # refresh the row of data ... we do this to get the id. Not needed.

        return db_job

    def retrieve_job(self, job_id: int, session: Session) -> Optional[Job]:
        return session.get(Job, job_id)

    def list_jobs(self, session: Session) -> list[Job]:
        # The way SQLAlchemy works, you MUST use == instead of 'is' keyword.
        jobs: list[Job] = session.query(Job).filter(Job.is_active == True).all()
        return jobs

    def update_job_by_id(
        self,
        job_id: int,
        update_job: UpdateJob,
        user: User,
        session: Session
    ) -> Optional[Job]:
        update_job_dict: dict = self._update_job_payload(update_job)

        update_statement: Update = update(Job).where(
            and_(
                Job.id == job_id,
                Job.owner_id == user.id
            )
        ).values(update_job_dict).returning(Job)

        db_job: Job = session.execute(update_statement).scalar()
        # Flushes (loads up the operations), and commits(saves) to the DB.
        session.commit()

        return db_job

    def _update_job_payload(self, update_job: UpdateJob) -> dict:
        update_job_payload: dict = dict()
        for update_job_key, update_job_value in update_job.model_dump().items():
            if update_job_value:
                update_job_payload[update_job_key] = update_job_value
        return update_job_payload

    def delete_job_by_id(self, job_id: int, session: Session):
        delete_statement: Delete = delete(Job).where(Job.id == job_id)
        session.execute(delete_statement)
        session.commit()


job_dao: JobDao = JobDao()
