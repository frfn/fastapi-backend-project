from fastapi import APIRouter

from api.v1.jobs import route_jobs
from api.v1.users import route_users
from api.v1.login import route_login

# this acts like the main instance of FastAPI! think of it as a 'mini FastAPI' class
# You then 'include' this in the main instance of FastAPI
api_router = APIRouter()

# include all the APIRouter instances from other API file!
# with tags... we're just adding metadata, saying that this route belongs to 'users'
api_router.include_router(route_users.router, prefix='/users', tags=['users'])
api_router.include_router(route_jobs.router, prefix='/jobs', tags=['jobs'])
api_router.include_router(route_login.router, prefix='/login', tags=['login'])

