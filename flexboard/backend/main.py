from fastapi import FastAPI

from api.api_routes import api_router
from config import config_object
from database.tables import Base
from database.session import engine


def create_tables():
    """
    Connects to the database and creates tables from objects extends the Base class. Users, Jobs, etc.
    """
    # https://docs.sqlalchemy.org/en/14/core/metadata.html#creating-and-dropping-database-tables
    Base.metadata.create_all(bind=engine)


def start():
    application: FastAPI = FastAPI(
        title=config_object.PROJECT_TITLE,
        version=config_object.PROJECT_VERSION,
        summary=config_object.AUTHOR
    )

    application.include_router(api_router)

    create_tables()

    return application


app: FastAPI = start()


# Test Endpoint
@app.get("/")
def a():
    return 'Hello'
