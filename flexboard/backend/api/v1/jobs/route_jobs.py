from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.v1.login.route_login import get_current_user_from_token
from api_models.job import ShowJob, JobCreate, UpdateJob
from database.orm_models.job import Job
from database.orm_models.user import User
from database.session import get_database
from services.job_service import job_service

router: APIRouter = APIRouter()


@router.post("/create-job", response_model=ShowJob)
def create_job(job: JobCreate, user: User = Depends(get_current_user_from_token), session: Session = Depends(get_database)) -> ShowJob:
    if not user:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    job: Job = job_service.create_new_job(job, user.id, session)

    if not job:
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Job could not be created.")

    # job is an ORM Object, but since we put orm_mode = True, it will be converted to a dictionary object. But we shall return as ShowJob.
    # Pydantic can only parse Pydantic objects, not other objects!
    return ShowJob(
        title=job.title,
        company=job.company,
        company_url=job.company_url,
        description=job.description,
        location=job.location,
        date_posted=job.date_posted,
        is_active=job.is_active
    )


@router.get("/get-job/{job_id}", response_model=ShowJob)
def get_job_by_id(
    job_id: int,
    user: User = Depends(get_current_user_from_token),
    session: Session = Depends(get_database)
) -> ShowJob:
    if not user:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    job: Job = job_service.retrieve_job(job_id, session)

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")

    return ShowJob(
        title=job.title,
        company=job.company,
        company_url=job.company_url,
        description=job.description,
        location=job.location,
        date_posted=job.date_posted,
        is_active=job.is_active
    )


@router.get("/list-jobs", response_model=List[ShowJob])
def list_jobs(
    user: User = Depends(get_current_user_from_token),
    session: Session = Depends(get_database)
) -> List[ShowJob]:
    if not user:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    jobs: List[Job] = job_service.list_jobs(session)

    if not jobs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jobs not found.")

    show_jobs: List[ShowJob] = list()

    for job in jobs:
        show_jobs.append(
            ShowJob(
                title=job.title,
                company=job.company,
                company_url=job.company_url,
                description=job.description,
                location=job.location,
                date_posted=job.date_posted,
                is_active=job.is_active,
            )
        )

    return show_jobs


@router.put("/update-job/{job_id}", response_model=ShowJob)
def update_job_by_id(
    job_id: int,
    update_job: UpdateJob,
    user: User = Depends(get_current_user_from_token),
    session: Session = Depends(get_database)
) -> ShowJob:
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    db_job: Job = job_service.retrieve_job(job_id, session)

    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")

    if db_job.owner_id == user.id or user.is_superuser:
        updated_job: Optional[Job] = job_service.update_job_by_id(job_id, update_job, user, session)

        if not updated_job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not updated.")

        if updated_job:
            return ShowJob(
                title=updated_job.title,
                company=updated_job.company,
                company_url=updated_job.company_url,
                description=updated_job.description,
                location=updated_job.location,
                date_posted=updated_job.date_posted,
                is_active=updated_job.is_active
            )
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not owner of job.")


@router.delete("/delete-job/{job_id}")
def delete_job_by_id(
    job_id: int,
    user: User = Depends(get_current_user_from_token),
    session: Session = Depends(get_database)
):
    if not user:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    db_job: Job = job_service.retrieve_job(job_id, session)

    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")

    if db_job.owner_id == user.id or user.is_superuser:
        job_service.delete_job_by_id(job_id, session)
        return f"Success, job {job_id} has been deleted."
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not owner of job.")
