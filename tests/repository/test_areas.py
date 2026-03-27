import pytest

from app.entities.areas import AreaEntity, AreaType
from app.exceptions.areas_exceptions import (
    AreaEntityIdNotStartedError,
    AreaNotFoundByIdError,
)
from app.repository.interfaces import FilterAreas


def create_area(
    name: str, house_id: int, type: AreaType = AreaType.living_room
) -> AreaEntity:
    return AreaEntity(name=name, type=type, house_id=house_id)


def test_create_area(area_repo, create_house):
    """
    Testing de la creación de area en una db
    """
    house_id = create_house(name="casa1")

    area_1 = create_area(name="casa1", house_id=house_id)

    area_id = area_repo.create(area_1)

    assert isinstance(area_id, int)
    assert area_id >= 0


def test_area_get_by_id(area_repo, create_house):
    """
    Testing de la obtención de una casa por su id
    """
    house_id = create_house(name="casa vacacional")

    area = create_area(name="cocina", house_id=house_id)

    area_id = area_repo.create(area)

    db_area = area_repo.get_by_id(area_id)

    assert isinstance(db_area, AreaEntity)

    assert area_id == db_area.id

    assert area.model_dump(exclude={"id"}) == db_area.model_dump(exclude={"id"})


def test_area_get_all(area_repo, create_house):
    """
    Testing de la obtención de todas las casas
    """
    house_id = create_house(name="casa 1")

    areas: list[AreaEntity] = []
    areas.append(create_area(name="algo", house_id=house_id))
    areas.append(create_area(name="otro", house_id=house_id))

    areas_id: list[int] = []
    for area in areas:
        areas_id.append(area_repo.create(area))

    areas_db = area_repo.get_all()

    assert isinstance(areas_db, list)

    for area_db in areas_db:
        assert area_db.id in areas_id


def test_area_get_all_filter_house_id(area_repo, create_house):
    house_1 = create_house(name="casa1", email_user="a@gmail.com")
    house_2 = create_house(name="casa2", email_user="b@gmail.com")

    areas_houses: list[AreaEntity] = []
    areas_houses.append(create_area(name="cocina", house_id=house_1))
    areas_houses.append(create_area(name="sala", house_id=house_2))
    areas_houses.append(create_area(name="dormitorio", house_id=house_1))

    ## Vistas tabular
    for area in areas_houses:
        area_repo.create(area)

    areas_db_1 = area_repo.get_all(FilterAreas(house_id=house_1))
    areas_db_2 = area_repo.get_all(FilterAreas(house_id=house_2))

    assert isinstance(areas_db_1, list)
    assert isinstance(areas_db_2, list)
    assert len(areas_db_1) == 2
    assert len(areas_db_2) == 1


def test_update_area(area_repo, create_house):
    """
    Testing de la actualización de un área
    """
    house_id = create_house(name="casa")

    area = create_area(name="cocina", house_id=house_id)

    area_id = area_repo.create(area)

    # Actualizar el área
    area.id = area_id
    area.name = "cocina nueva"
    area.type = AreaType.kitchen

    area_repo.update(area)

    # Verificar la actualización
    updated_area = area_repo.get_by_id(area_id)
    assert updated_area.name == "cocina nueva"
    assert updated_area.type == AreaType.kitchen


def test_update_area_id_none(area_repo):
    """
    Testing de la actualización de un área sin id
    """
    area = create_area(name="test", house_id=1)

    with pytest.raises(AreaEntityIdNotStartedError):
        area_repo.update(area)


def test_update_area_not_found(area_repo):
    """
    Testing de la actualización de un área que no existe
    """
    area = create_area(name="test", house_id=1)
    area.id = 9999  # ID que no existe

    with pytest.raises(AreaNotFoundByIdError):
        area_repo.update(area)


def test_delete_area(area_repo, create_house):
    """
    Testing de la eliminación de un área
    """
    house_id = create_house(name="casa")

    area = create_area(name="baño", house_id=house_id)

    area_id = area_repo.create(area)

    area_repo.delete(area_id)

    # Verificar que el área ya no existe
    deleted_area = area_repo.get_by_id(area_id)
    assert deleted_area is None


def test_delete_area_not_found(area_repo):
    """
    Testing de la eliminación de un área que no existe
    """
    with pytest.raises(AreaNotFoundByIdError):
        area_repo.delete(9999)
