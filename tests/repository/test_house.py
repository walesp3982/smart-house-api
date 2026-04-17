import pytest

from app.entities import HouseEntity
from app.entities.areas import AreaEntity, AreaType
from app.entities.house import HouseWithAreas
from app.exceptions.house_exception import HouseIdNotStarted, HouseNotFoundByIdError
from app.repository.interfaces.house import FilterGetAllHouse


def create_house_entity(user_id: int) -> HouseEntity:
    """
    helper que nos ayuda a crear HouseEntity facilmente

    Args:
        user_id: usuario existente en la db (Usa un fixture)

    Return:
        HouseEntity: entidad que representa una casa
    """
    return HouseEntity(name="casa1", user_id=user_id, invitation_validation=True)


def test_create_new_house(house_repo, user_id):
    new_house = create_house_entity(user_id)

    house_id = house_repo.create(new_house)

    assert isinstance(house_id, int)
    assert house_id >= 0


def test_get_all_house(house_repo, user_id):
    houses: list[HouseEntity] = []
    houses.append(create_house_entity(user_id))
    houses.append(create_house_entity(user_id))

    for house in houses:
        user_id = house_repo.create(house)

    all_houses = house_repo.get_all()
    assert isinstance(all_houses, list)

    assert len(all_houses) == len(houses)


def test_any_house(house_repo):
    all_house = house_repo.get_all()

    assert isinstance(all_house, list)

    assert len(all_house) == 0


def test_filter_user_id_get_all(house_repo, create_user):
    user1_id: int = create_user(name="Juan", email="j@gmail.com")
    user2_id: int = create_user(name="Esteban", email="e@gmail.com")
    user3_id: int = create_user(name="Maria", email="m@email.com")
    house_repo.create(create_house_entity(user1_id))
    house_repo.create(create_house_entity(user1_id))

    house_repo.create(create_house_entity(user2_id))

    assert len(house_repo.get_all(FilterGetAllHouse(user_id=user1_id))) == 2

    assert len(house_repo.get_all(FilterGetAllHouse(user_id=user2_id))) == 1

    assert len(house_repo.get_all(FilterGetAllHouse(user_id=user3_id))) == 0

    assert len(house_repo.get_all(FilterGetAllHouse())) == 3


def test_get_by_id(house_repo, user_id):
    house_entity = create_house_entity(user_id)
    id = house_repo.create(house_entity)

    house_db = house_repo.get_by_id(id)

    assert house_db is not None
    assert isinstance(house_db, HouseEntity)
    assert house_entity.model_dump(exclude={"id"}) == house_db.model_dump(exclude={"id"})


def test_update_house(house_repo, user_id) -> None:
    house_entity = create_house_entity(user_id)

    house_id = house_repo.create(house_entity)

    house = house_repo.get_by_id(house_id)

    house.name = "Casa de El Alto"

    house_repo.update(house)

    new_house = house_repo.get_by_id(house_id)

    assert new_house.name == house.name


def test_failed_update_house(house_repo, user_id) -> None:
    """
    Analiza el caso donde al update repositorio se mete
    como parametro un HouseEntity con id = None
    """
    house_entity = create_house_entity(user_id)

    with pytest.raises(HouseIdNotStarted):
        house_repo.update(house_entity)


def test_failed_not_found_update_house(house_repo, user_id):
    """
    Analiza cuando se intenta actualizar un house sin
    que exista en la db
    """
    house_id = house_repo.create(create_house_entity(user_id))
    house = house_repo.get_by_id(house_id)
    house.name = "algo"
    house_repo.delete(house_id)

    with pytest.raises(HouseNotFoundByIdError):
        house_repo.update(house)


def test_delete_house(house_repo, user_id):
    house_id = house_repo.create(create_house_entity(user_id))
    house_repo.delete(house_id)

    assert house_repo.get_by_id(house_id) is None


def test_failed_house(house_repo, user_id):
    """
    Revisa que lanze una excepción cuando el house_id no existe
    """
    house_id = house_repo.create(create_house_entity(user_id))
    house_repo.delete(house_id)

    with pytest.raises(HouseNotFoundByIdError):
        house_repo.delete(house_id)


def test_get_all_with_include_areas(house_repo, area_repo, create_house):
    house_id = create_house(name="Casa con áreas")

    # Crear áreas para la casa
    area1 = AreaEntity(name="Sala", type=AreaType.living_room, house_id=house_id)
    area2 = AreaEntity(name="Cocina", type=AreaType.kitchen, house_id=house_id)
    area_repo.create(area1)
    area_repo.create(area2)

    # Obtener casas con áreas incluidas
    houses_with_areas = house_repo.get_all(FilterGetAllHouse(include_areas=True))

    assert len(houses_with_areas) == 1
    house = houses_with_areas[0]
    assert isinstance(house, HouseWithAreas)
    assert house.id == house_id
    assert len(house.areas) == 2
    area_names = [area.name for area in house.areas]
    assert "Sala" in area_names
    assert "Cocina" in area_names
