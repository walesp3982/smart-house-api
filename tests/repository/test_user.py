# Estamos testeando el repositorio de usuario,
import pytest

from app.dto import UserCreateDTO
from app.entities import UserEntity
from app.exceptions import DatabaseConstraintException, UserNotFoundError


def test_create_user(user_repo):
    user_dto = UserCreateDTO(
        name="John Doe", email="john.doe@example.com", password="password"
    )
    user_id = user_repo.create(user_dto)
    assert user_id is not None
    users = user_repo.get_all()
    assert len(users) == 1


def test_verify_create_user(user_repo):
    user_dto = UserCreateDTO(
        name="Jhon Doe", email="john.doe@example.com", password="password"
    )
    user_id = user_repo.create(user_dto)
    assert isinstance(user_repo.get_by_id(user_id), UserEntity)


def test_raise_doble_email_create_users(user_repo):
    email = "j@gmail.com"
    user_dto_1 = UserCreateDTO(name="Juan", email=email, password="1234")
    user_dto_2 = UserCreateDTO(name="Estaban", email=email, password="4132")
    with pytest.raises(DatabaseConstraintException):
        user_repo.create(user_dto_1)
        user_repo.create(user_dto_2)


def test_type_get_all(user_repo):
    users = user_repo.get_all()

    assert isinstance(users, list)


def test_cero_users_in_get_all(user_repo):
    users = user_repo.get_all()

    # Se verifica que users esté vació
    # o también ->  assert len(users) == 0
    assert users == []


def test_n_users_in_get_all(user_repo):
    user_repo.create(UserCreateDTO(name="Juan", email="j@gmail.com", password="asdf"))
    user_repo.create(UserCreateDTO(name="Perez", email="p@gmail.com", password="qewr"))
    user_repo.create(
        UserCreateDTO(name="Velazco", email="v@gmail.com", password="zcxv")
    )

    users = user_repo.get_all()

    assert len(users) == 3


def test_get_user_exist_by_id(user_repo):
    id_user = user_repo.create(
        UserCreateDTO(name="Juan", email="j@gmail.com", password="asdf")
    )

    user = user_repo.get_by_id(id_user)

    assert isinstance(user, UserEntity)

    assert user.id == id_user


def test_any_user_exist_get_by_id(user_repo):
    user = user_repo.get_by_id(12)

    assert user is None


def test_cmp_userdto_in_user_get_by_id(user_repo):
    userdto = UserCreateDTO(name="Juan", email="email@gmail.com", password="password")

    # Creación de de usuario en db
    user_id = user_repo.create(userdto)

    user = user_repo.get_by_id(user_id)

    assert user is not None

    user_dict = user.model_dump()
    user_dict.pop("id")
    assert user_dict == userdto.model_dump()


def test_find_user_by_email(user_repo):
    email = "j@gmail.com"
    user_dto = UserCreateDTO(name="Juan", email=email, password="password")

    user_repo.create(user_dto)

    user = user_repo.get_by_email(email)

    assert isinstance(user, UserEntity)

    assert user.email == email


def test_not_found_user_by_email(user_repo):
    email = "j@gmail.com"
    user_dto = UserCreateDTO(name="juan", email="t@gmail.com", password="1234")

    user_repo.create(user_dto)

    user = user_repo.get_by_email(email)

    assert user is None


def test_cmp_dto_user_with_user_repo(user_repo):
    email = "j@gmail.com"
    user_dto = UserCreateDTO(name="juan", email=email, password="1234")

    user_repo.create(user_dto)

    user = user_repo.get_by_email(email)
    user_dict = user.model_dump()
    user_dict.pop("id")

    assert user_dict == user_dto.model_dump()


def test_update_user_value(user_repo):
    user_id = user_repo.create(
        UserCreateDTO(name="juan", email="esteban@gmail.com", password="password")
    )

    before_user = user_repo.get_by_id(user_id)

    copy_user = before_user.model_copy()
    copy_user.name = "esteban"

    user_repo.update(copy_user)

    after_user = user_repo.get_by_id(copy_user.id)

    assert after_user.name == "esteban"


def test_raise_update_user_not_found(user_repo):
    user_id = user_repo.create(
        UserCreateDTO(name="esteban", email="esteban@gmail.com", password="1234")
    )
    user = user_repo.get_by_id(user_id)
    user_repo.delete(user.id)

    with pytest.raises(UserNotFoundError):
        user_repo.update(user)


def test_raise_delete_user_not_found(user_repo):
    with pytest.raises(UserNotFoundError):
        user_repo.delete(1)


def test_delete_user(user_repo):
    user_id = user_repo.create(
        UserCreateDTO(name="juan", email="j@gmail.com", password="password")
    )
    user_repo.delete(user_id)
    assert user_repo.get_by_id(user_id) is None
