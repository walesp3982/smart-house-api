from typing import Callable

import pytest
from sqlalchemy import create_engine

from app.entities import UserEntity
from app.infraestructure.models import metadata
from app.repository import DeviceRepository, UserRepository
from app.repository.house import HouseRepository


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


@pytest.fixture
def device_repo(connection):
    return DeviceRepository(connection)


@pytest.fixture
def house_repo(connection):
    return HouseRepository(connection)


@pytest.fixture
def user_id(user_repo):
    return user_repo.create(
        UserEntity(
            name="juan", email="juan@gmail.com", password="password", is_verified=True
        )
    )


@pytest.fixture
def create_user(user_repo) -> Callable[..., int]:
    def _create(name="Test User", email="test@test.com"):
        return user_repo.create(
            UserEntity(name=name, email=email, password="password", is_verified=True)
        )

    return _create
