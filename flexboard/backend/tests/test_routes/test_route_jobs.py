import http
import json
from typing import List

from api_models.job import JobCreate
from database.orm_models.job import Job
from database.orm_models.user import User
from tests.test_utils import TestUtils
from services.job_service import job_service

ROUTE_JOBS: str = "/jobs"


def test_create_job(client, user_and_header_with_bearer_token):
    """
    Tests the /jobs/create-job endpoint.
    """
    header_with_bearer_token: dict = user_and_header_with_bearer_token[1]

    data: dict = {
        "title": "test job",
        "company": "test company",
        "company_url": "testurl.com",
        "description": "this is a test!"
    }

    # In real world, we would use 'data=data'
    # 'data' dict would probably be an object too.
    # 'data=' is the body from FE.
    response = client.post(f"{ROUTE_JOBS}/create-job", json=data, headers=header_with_bearer_token)

    response_json = response.json()
    response_title: str = response_json.get("title")

    assert response.status_code == 200
    assert response_title == data.get("title")


def test_create_job_using_data_kwargs(client, user_and_header_with_bearer_token):
    """
    Tests the /jobs/create-job endpoint.
    """
    header_with_bearer_token: dict = user_and_header_with_bearer_token[1]

    data: dict = {
        "title": "test job",
        "company": "test company",
        "company_url": "testurl.com",
        "description": "this is a test!"
    }

    data_to_json: str = json.dumps(data)

    # In real world, we would use 'data=data'
    # 'data' dict would probably be an object too.
    # 'data=' is the body from FE.
    response = client.post(f"{ROUTE_JOBS}/create-job", data=data_to_json, headers=header_with_bearer_token)

    response_json = response.json()
    response_title: str = response_json.get("title")

    assert response.status_code == 200
    assert response_title == data.get("title")


def test_create_new_job(db_session):
    """
    Tests just the utility function.
    """
    job_create: JobCreate = JobCreate(
        title="test job",
        company="test company",
        company_url="testurl.com",
        description="this is a test!"
    )

    user: User = TestUtils.create_random_user(db_session)
    job: Job = job_service.create_new_job(job_create, user.id, db_session)
    received_job: Job = job_service.retrieve_job(job.id, db_session)

    assert job.id == received_job.id
    assert job_create.title == job.title


def test_retrieve_job_by_id(client, user_and_header_with_bearer_token, db_session):
    """
    Tests the /jobs/get-job endpoint.
    """
    user: User = user_and_header_with_bearer_token[0]
    header_with_bearer_token: dict = user_and_header_with_bearer_token[1]

    job_create: JobCreate = JobCreate(
        title="test job",
        company="test company",
        company_url="testurl.com",
        description="this is a test!"
    )

    job: Job = job_service.create_new_job(job_create, user.id, db_session)

    response = client.get(f"{ROUTE_JOBS}/get-job/{job.id}", headers=header_with_bearer_token)

    response_json = response.json()

    assert response.status_code == http.HTTPStatus.OK
    assert response_json.get('title') == job.title
    assert response_json.get('company') == job.company
    assert response_json.get('company_url') == job.company_url
    assert response_json.get('description') == job.description
    assert response_json.get('location') == job.location


def test_list_jobs(client, user_and_header_with_bearer_token, db_session):
    """
    Tests the /jobs/list-jobs endpoint.
    """
    user: User = user_and_header_with_bearer_token[0]
    header_with_bearer_token: dict = user_and_header_with_bearer_token[1]

    total_count: int = 5
    added_jobs: List[Job] = list()

    for index in range(total_count):
        job_create: JobCreate = JobCreate(
            title=f"test job: {index}",
            company=f"test company {index}",
            company_url=f"testurl-index-{index}.com",
            description="this is an index test!",
            is_active=True,
        )
        job: Job = job_service.create_new_job(job_create, user.id, db_session)
        added_jobs.append(job)

    job_title_names_added: List[str] = [added_job.title for added_job in added_jobs]

    response = client.get(f"{ROUTE_JOBS}/list-jobs", headers=header_with_bearer_token)
    response_json = response.json()

    job_title_names: List[str] = list()
    for response_json_show_job_dict in response_json:
        job_title_names.append(response_json_show_job_dict.get("title"))
        assert response_json_show_job_dict.get("is_active")

    assert response.status_code == http.HTTPStatus.OK
    assert len(response_json) == total_count

    for job_title_name in job_title_names:
        assert job_title_name in job_title_names_added


def test_delete_job(client, user_and_header_with_bearer_token, db_session):
    """
    Tests the /jobs/delete-job endpoint.
    """
    user: User = user_and_header_with_bearer_token[0]
    header_with_bearer_token: dict = user_and_header_with_bearer_token[1]

    job_create: JobCreate = JobCreate(
        title="test job",
        company="test company",
        company_url="testurl.com",
        description="this is a test!"
    )

    job: Job = job_service.create_new_job(job_create, user.id, db_session)

    retrieved_job: Job = job_service.retrieve_job(job.id, db_session)

    assert retrieved_job.id == job.id

    response = client.delete(f'/jobs/delete-job/{job.id}', headers=header_with_bearer_token)
    response_json = response.json()

    assert response_json == f"Success, job {job.id} has been deleted."

    retrieved_job: Job = job_service.retrieve_job(job.id, db_session)

    assert retrieved_job is None
