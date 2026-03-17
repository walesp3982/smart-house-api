import pytest
from sqlalchemy import create_engine

from app.models import metadata
from app.repository import UserRepository


@pytest.fixture
def connection():
    """Fixture to create an in-memory SQLite database engine."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    with engine.begin() as conn:
        metadata.create_all(bind=conn)

    with engine.connect() as conn:
        transaction = conn.begin()
        yield conn
        transaction.rollback()


@pytest.fixture
def user_repo(connection):
    return UserRepository(connection)
