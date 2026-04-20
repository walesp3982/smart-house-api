import pytest

from app.entities.installed_device import InstalledDeviceEntity
from app.exceptions.installed_device_exceptions import (
    InstalledDeviceEntityIdNotStartedError,
    InstalledDeviceNotFoundByIdError,
)
from app.repository.interfaces.installed_device import FilterInstalledDevices


def create_installed_device_entity(
    name: str,
    device_id: int,
    house_id: int,
    area_id: int | None = None,
    user_id: int = 1,
) -> InstalledDeviceEntity:
    return InstalledDeviceEntity(
        name=name,
        device_id=device_id,
        house_id=house_id,
        area_id=area_id,
        user_id=user_id,
    )


def test_create_installed_device(
    installed_device_repo, create_device, create_house, create_user
):
    """
    Testing de la creación de installed device en una db
    """
    user_id = create_user()
    house_id = create_house(name="Test House", user_id=user_id)
    device_id = create_device()

    installed_device = create_installed_device_entity(
        name="Living Room Light",
        device_id=device_id,
        house_id=house_id,
        user_id=user_id,
    )

    installed_device_id = installed_device_repo.create(installed_device)

    assert isinstance(installed_device_id, int)
    assert installed_device_id >= 0


def test_installed_device_get_by_id(
    installed_device_repo, create_device, create_house, create_user
):
    """
    Testing de la obtención de un installed device por su id
    """
    user_id = create_user()
    house_id = create_house(name="Test House", user_id=user_id)
    device_id = create_device()

    installed_device = create_installed_device_entity(
        name="Kitchen Light", device_id=device_id, house_id=house_id, user_id=user_id
    )

    installed_device_id = installed_device_repo.create(installed_device)

    db_installed_device = installed_device_repo.get_by_id(installed_device_id)

    assert isinstance(db_installed_device, InstalledDeviceEntity)

    assert installed_device_id == db_installed_device.id

    assert installed_device.model_dump(
        exclude={"id"}
    ) == db_installed_device.model_dump(exclude={"id"})


def test_installed_device_get_all(
    installed_device_repo, create_device, create_house, create_user
):
    """
    Testing de la obtención de todos los installed devices
    """
    user_id = create_user()
    house_id = create_house(name="Test House", user_id=user_id)
    device_id_1 = create_device()
    device_id_2 = create_device()

    installed_device_1 = create_installed_device_entity(
        name="Device 1", device_id=device_id_1, house_id=house_id, user_id=user_id
    )
    installed_device_2 = create_installed_device_entity(
        name="Device 2", device_id=device_id_2, house_id=house_id, user_id=user_id
    )

    installed_device_repo.create(installed_device_1)
    installed_device_repo.create(installed_device_2)

    all_installed_devices = installed_device_repo.get_all()

    assert isinstance(all_installed_devices, list)
    assert len(all_installed_devices) >= 2


def test_installed_device_get_all_with_filter_house_id(
    installed_device_repo, create_device, create_house, create_user
):
    """
    Testing de la obtención de installed devices con filtro por house_id
    """
    user_id = create_user()
    house_id = create_house(name="Test House", user_id=user_id)
    device_id = create_device()

    installed_device = create_installed_device_entity(
        name="Device", device_id=device_id, house_id=house_id, user_id=user_id
    )

    installed_device_repo.create(installed_device)

    filtered_devices = installed_device_repo.get_all(
        filters=FilterInstalledDevices(house_id=house_id)
    )

    assert len(filtered_devices) >= 1
    assert all(d.house_id == house_id for d in filtered_devices)


def test_installed_device_get_all_with_filter_user_id(
    installed_device_repo, create_device, create_house, create_user
):
    """
    Testing de la obtención de installed devices con filtro por user_id
    """
    user_id = create_user()
    house_id = create_house(name="Test House", user_id=user_id)
    device_id = create_device()

    installed_device = create_installed_device_entity(
        name="Device", device_id=device_id, house_id=house_id, user_id=user_id
    )

    installed_device_repo.create(installed_device)

    filtered_devices = installed_device_repo.get_all(
        filters=FilterInstalledDevices(user_id=user_id)
    )

    assert len(filtered_devices) >= 1
    assert all(d.user_id == user_id for d in filtered_devices)


def test_installed_device_get_all_with_filter_name(
    installed_device_repo, create_device, create_house, create_user
):
    """
    Testing de la obtención de installed devices con filtro por name
    """
    user_id = create_user()
    house_id = create_house(name="Test House", user_id=user_id)
    device_id = create_device()

    installed_device = create_installed_device_entity(
        name="Living Room Light",
        device_id=device_id,
        house_id=house_id,
        user_id=user_id,
    )

    installed_device_repo.create(installed_device)

    filtered_devices = installed_device_repo.get_all(
        filters=FilterInstalledDevices(name="Living")
    )

    assert len(filtered_devices) >= 1
    assert all("Living" in d.name for d in filtered_devices)


def test_installed_device_update(
    installed_device_repo, create_device, create_house, create_user
):
    """
    Testing de la actualización de un installed device
    """
    user_id = create_user()
    house_id = create_house(name="Test House", user_id=user_id)
    device_id = create_device()

    installed_device = create_installed_device_entity(
        name="Old Name", device_id=device_id, house_id=house_id, user_id=user_id
    )

    installed_device_id = installed_device_repo.create(installed_device)

    installed_device_updated = InstalledDeviceEntity(
        id=installed_device_id,
        name="New Name",
        device_id=device_id,
        house_id=house_id,
        user_id=user_id,
        area_id=None,
    )

    installed_device_repo.update(installed_device_updated)

    db_installed_device = installed_device_repo.get_by_id(installed_device_id)

    assert db_installed_device.name == "New Name"


def test_installed_device_update_without_id_raises_error(installed_device_repo):
    """
    Testing que actualizar un installed device sin id lanza error
    """
    installed_device = InstalledDeviceEntity(
        id=None, name="Device", device_id=1, house_id=1, user_id=1, area_id=None
    )

    with pytest.raises(InstalledDeviceEntityIdNotStartedError):
        installed_device_repo.update(installed_device)


def test_installed_device_update_non_existent_raises_error(installed_device_repo):
    """
    Testing que actualizar un installed device no existente lanza error
    """
    installed_device = InstalledDeviceEntity(
        id=9999, name="Device", device_id=1, house_id=1, user_id=1, area_id=None
    )

    with pytest.raises(InstalledDeviceNotFoundByIdError):
        installed_device_repo.update(installed_device)


def test_installed_device_delete(
    installed_device_repo, create_device, create_house, create_user
):
    """
    Testing de la eliminación de un installed device
    """
    user_id = create_user()
    house_id = create_house(name="Test House", user_id=user_id)
    device_id = create_device()

    installed_device = create_installed_device_entity(
        name="Device", device_id=device_id, house_id=house_id, user_id=user_id
    )

    installed_device_id = installed_device_repo.create(installed_device)

    installed_device_repo.delete(installed_device_id)

    db_installed_device = installed_device_repo.get_by_id(installed_device_id)

    assert db_installed_device is None


def test_installed_device_delete_non_existent_raises_error(installed_device_repo):
    """
    Testing que eliminar un installed device no existente lanza error
    """
    with pytest.raises(InstalledDeviceNotFoundByIdError):
        installed_device_repo.delete(9999)
