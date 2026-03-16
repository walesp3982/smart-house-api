import pytest
from sqlalchemy import create_engine

from app.models import metadata
from app.repository import UserRepository


@pytest.fixture
def connection():
    """Fixture to create an in-memory SQLite database engine."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    with engine.begin() as connection:
        metadata.create_all(bind=connection)
        yield connection
        metadata.drop_all(bind=connection)


@pytest.fixture
def user_repo(connection):
    return UserRepository(connection)
