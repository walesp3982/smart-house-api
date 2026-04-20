import secrets
from uuid import uuid4

import pytest

from app.entities import DeviceEntity, DeviceType
from app.exceptions.device_exception import DeviceNotFoundByIdError


def create_false_device(type: DeviceType) -> DeviceEntity:
    device_uuid = uuid4.__str__()
    code_activation = secrets.token_hex(4)
    return DeviceEntity(
        device_uuid=device_uuid, activation_code=code_activation, type=type
    )


def test_create_device(device_repo):
    new_device = create_false_device(DeviceType.CAMERA)

    int_device = device_repo.create(new_device)

    assert isinstance(int_device, int)

    assert int_device >= 0


def test_get_by_id(device_repo):
    new_device = create_false_device(DeviceType.CAMERA)

    int_device = device_repo.create(new_device)

    device_in_repo = device_repo.get_by_id(int_device)

    assert isinstance(device_in_repo, DeviceEntity)
    assert int_device == device_in_repo.id


def test_not_found_device(device_repo):
    new_device = create_false_device(DeviceType.CAMERA)

    int_device = device_repo.create(new_device)

    device_in_repo = device_repo.get_by_id(int_device)

    device_repo.delete(device_in_repo.id)

    assert device_repo.get_by_id(int_device) is None


def test_invalid_deletion_device(device_repo):
    new_device = create_false_device(DeviceType.CAMERA)
    int_device = device_repo.create(new_device)

    device_repo.delete(int_device)

    with pytest.raises(DeviceNotFoundByIdError):
        device_repo.delete(int_device)
