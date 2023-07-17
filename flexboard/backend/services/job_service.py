from typing import Optional

from sqlalchemy.orm import Session

from api_models.job import JobCreate, UpdateJob
from database.daos.job_dao import JobDao, job_dao
from database.orm_models.job import Job
from database.orm_models.user import User


class JobService:
    def __init__(self, job_dao_param: JobDao):
        self.job_dao = job_dao_param

    def create_new_job(self, job: JobCreate, owner_id: int, session: Session) -> Optional[Job]:
        job: Job = self.job_dao.create_new_job(job, owner_id, session)

        if not job:
            return None

        return job

    def retrieve_job(self, job_id: int, session: Session) -> Optional[Job]:
        job: Job = self.job_dao.retrieve_job(job_id, session)

        if not job:
            return None

        return job

    def list_jobs(self, session: Session) -> Optional[list[Job]]:
        jobs: list[Job] = self.job_dao.list_jobs(session)

        if not jobs:
            return jobs

        return jobs

    def update_job_by_id(
        self,
        job_id: int,
        update_job: UpdateJob,
        user: User,
        session: Session
    ) -> Optional[Job]:
        job: Job = self.job_dao.update_job_by_id(job_id, update_job, user, session)

        if not job:
            return None

        return job

    def delete_job_by_id(self, job_id: int, session: Session):
        self.job_dao.delete_job_by_id(job_id, session)


job_service: JobService = JobService(job_dao)
