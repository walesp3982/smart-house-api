import secrets
from typing import Callable, cast
from uuid import uuid4

import pytest
from sqlalchemy import create_engine

from app.entities import DeviceEntity, DeviceType, UserEntity
from app.entities.house import HouseEntity
from app.infraestructure.models import metadata
from app.repository import AreaRepository, DeviceRepository, UserRepository
from app.repository.house import HouseRepository
from app.repository.installed_device import InstalledDeviceRepository
from app.repository.track_device import TrackDeviceRepository


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


@pytest.fixture
def create_house(house_repo, create_user) -> Callable[..., int]:
    def _create(
        name: str,
        location: str | None = None,
        invitation_validation: bool = True,
        email_user: str = "juan@example.com",
        user_id: int | None = None,
    ):
        if user_id is None:
            user_id = cast(int, create_user(email=email_user))
        house = house_repo.create(
            HouseEntity(
                name=name,
                user_id=user_id,
                location=location,
                invitation_validation=invitation_validation,
            )
        )
        return house

    return _create


@pytest.fixture
def area_repo(connection):
    return AreaRepository(connection)


@pytest.fixture
def track_device_repo(connection):
    return TrackDeviceRepository(connection)


@pytest.fixture
def installed_device_repo(connection):
    return InstalledDeviceRepository(connection)


@pytest.fixture
def create_device(device_repo) -> Callable[..., int]:
    def _create(type: DeviceType = DeviceType.LIGHT):
        device_uuid = uuid4().__str__()
        code_activation = secrets.token_hex(4)
        device = DeviceEntity(
            device_uuid=device_uuid, activation_code=code_activation, type=type
        )
        return device_repo.create(device)

    return _create


@pytest.fixture
def create_installed_device(
    installed_device_repo, create_device, create_house, create_user
) -> Callable[..., int]:
    def _create(
        name: str = "Test Device",
        house_id: int | None = None,
        area_id: int | None = None,
        user_id: int | None = None,
    ):
        if user_id is None:
            user_id = cast(int, create_user())
        if house_id is None:
            house_id = cast(int, create_house(name="Test House", user_id=user_id))

        device_id = create_device()

        from app.entities.installed_device import InstalledDeviceEntity

        installed_device = InstalledDeviceEntity(
            name=name,
            device_id=device_id,
            house_id=house_id,
            area_id=area_id,
            user_id=user_id,
        )
        return installed_device_repo.create(installed_device)

    return _create
