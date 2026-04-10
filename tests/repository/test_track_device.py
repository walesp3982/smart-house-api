from datetime import datetime
from uuid import uuid4

import pytest

from app.entities.track_device import StatusDevice, TrackDevice
from app.exceptions.track_device_exceptions import (
    TrackDeviceEntityIdNotStartedError,
    TrackDeviceNotFoundByIdError,
)
from app.repository.interfaces.track_device import FilterTrackDevices


def create_track_device(
    device_id: int,
    status: StatusDevice = StatusDevice.ON,
    timestamp: datetime | None = None,
) -> TrackDevice:
    if timestamp is None:
        timestamp = datetime.now()
    return TrackDevice(device_id=device_id, status=status, timestamp=timestamp)


def test_create_track_device(track_device_repo, create_installed_device):
    """
    Testing de la creación de track device en una db
    """
    installed_device_id = create_installed_device()

    track_device = create_track_device(device_id=installed_device_id)

    track_device_id = track_device_repo.create(track_device)

    assert isinstance(track_device_id, int)
    assert track_device_id >= 0


def test_track_device_get_by_id(track_device_repo, create_installed_device):
    """
    Testing de la obtención de un track device por su id
    """
    installed_device_id = create_installed_device()

    track_device = create_track_device(device_id=installed_device_id)

    track_device_id = track_device_repo.create(track_device)

    db_track_device = track_device_repo.get_by_id(track_device_id)

    assert isinstance(db_track_device, TrackDevice)

    assert track_device_id == db_track_device.id

    assert track_device.model_dump(exclude={"id"}) == db_track_device.model_dump(
        exclude={"id"}
    )


def test_track_device_get_all(track_device_repo, create_installed_device, create_user):
    """
    Testing de la obtención de todos los track devices
    """
    user_id = create_user(email=f"user1_{uuid4()}@test.com")
    installed_device_id_1 = create_installed_device(name="Device 1", user_id=user_id)
    installed_device_id_2 = create_installed_device(name="Device 2", user_id=user_id)

    track_device_1 = create_track_device(
        device_id=installed_device_id_1, status=StatusDevice.ON
    )
    track_device_2 = create_track_device(
        device_id=installed_device_id_2, status=StatusDevice.OFF
    )

    track_device_repo.create(track_device_1)
    track_device_repo.create(track_device_2)

    all_track_devices = track_device_repo.get_all()

    assert isinstance(all_track_devices, list)
    assert len(all_track_devices) >= 2


def test_track_device_get_all_with_filter_device_id(
    track_device_repo, create_installed_device, create_user
):
    """
    Testing de la obtención de track devices con filtro por device_id
    """
    user_id = create_user(email=f"user1_{uuid4()}@test.com")
    installed_device_id_1 = create_installed_device(name="Device 1", user_id=user_id)
    installed_device_id_2 = create_installed_device(name="Device 2", user_id=user_id)

    track_device_1 = create_track_device(device_id=installed_device_id_1)
    track_device_2 = create_track_device(device_id=installed_device_id_2)

    track_device_repo.create(track_device_1)
    track_device_repo.create(track_device_2)

    filtered_track_devices = track_device_repo.get_all(
        filters=FilterTrackDevices(device_id=installed_device_id_1)
    )

    assert len(filtered_track_devices) == 1
    assert filtered_track_devices[0].device_id == installed_device_id_1


def test_track_device_get_all_with_filter_status(
    track_device_repo, create_installed_device, create_user
):
    """
    Testing de la obtención de track devices con filtro por status
    """
    user_id = create_user(email=f"user1_{uuid4()}@test.com")
    installed_device_id_1 = create_installed_device(name="Device 1", user_id=user_id)
    installed_device_id_2 = create_installed_device(name="Device 2", user_id=user_id)

    track_device_1 = create_track_device(
        device_id=installed_device_id_1, status=StatusDevice.ON
    )
    track_device_2 = create_track_device(
        device_id=installed_device_id_2, status=StatusDevice.OFF
    )

    track_device_repo.create(track_device_1)
    track_device_repo.create(track_device_2)

    filtered_track_devices = track_device_repo.get_all(
        filters=FilterTrackDevices(status=StatusDevice.ON.value)
    )

    assert len(filtered_track_devices) >= 1
    assert all(td.status == StatusDevice.ON for td in filtered_track_devices)


def test_track_device_update(track_device_repo, create_installed_device):
    """
    Testing de la actualización de un track device
    """
    installed_device_id = create_installed_device()

    track_device = create_track_device(
        device_id=installed_device_id, status=StatusDevice.ON
    )

    track_device_id = track_device_repo.create(track_device)

    track_device_updated = TrackDevice(
        id=track_device_id,
        device_id=installed_device_id,
        status=StatusDevice.OFF,
        timestamp=datetime.now(),
    )

    track_device_repo.update(track_device_updated)

    db_track_device = track_device_repo.get_by_id(track_device_id)

    assert db_track_device.status == StatusDevice.OFF


def test_track_device_update_without_id_raises_error(track_device_repo):
    """
    Testing que actualizar un track device sin id lanza error
    """
    track_device = TrackDevice(
        id=None, device_id=1, status=StatusDevice.ON, timestamp=datetime.now()
    )

    with pytest.raises(TrackDeviceEntityIdNotStartedError):
        track_device_repo.update(track_device)


def test_track_device_update_non_existent_raises_error(track_device_repo):
    """
    Testing que actualizar un track device no existente lanza error
    """
    track_device = TrackDevice(
        id=9999, device_id=1, status=StatusDevice.ON, timestamp=datetime.now()
    )

    with pytest.raises(TrackDeviceNotFoundByIdError):
        track_device_repo.update(track_device)


def test_track_device_delete(track_device_repo, create_installed_device):
    """
    Testing de la eliminación de un track device
    """
    installed_device_id = create_installed_device()

    track_device = create_track_device(device_id=installed_device_id)

    track_device_id = track_device_repo.create(track_device)

    track_device_repo.delete(track_device_id)

    db_track_device = track_device_repo.get_by_id(track_device_id)

    assert db_track_device is None


def test_track_device_delete_non_existent_raises_error(track_device_repo):
    """
    Testing que eliminar un track device no existente lanza error
    """
    with pytest.raises(TrackDeviceNotFoundByIdError):
        track_device_repo.delete(9999)
