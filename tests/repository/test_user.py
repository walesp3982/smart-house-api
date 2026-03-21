# Estamos testeando el repositorio de usuario,
from datetime import datetime

import pytest

from app.dto import UserCreateDTO
from app.entities import UserEntity
from app.exceptions import DatabaseConstraintException, UserNotFoundError


def create_false_dto(name: str, verified: bool):
    return UserCreateDTO(
        name=name,
        email=f"{'.'.join(name.split(' ')).lower()}@gmail.com",
        password="password",
        is_verified=verified,
        verification_token="12345",
        verification_token_expired_at=datetime.now(),
    )


def test_create_user(user_repo):
    user_dto = create_false_dto("juan", True)
    user_id = user_repo.create(user_dto)
    assert user_id is not None
    users = user_repo.get_all()
    assert len(users) == 1


def test_verify_create_user(user_repo):
    user_dto = create_false_dto("juan", True)
    user_id = user_repo.create(user_dto)
    assert isinstance(user_repo.get_by_id(user_id), UserEntity)


def test_raise_doble_email_create_users(user_repo):
    user_dto_1 = create_false_dto("juan", True)
    user_dto_2 = create_false_dto("juan", True)
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
    user_repo.create(create_false_dto("juan", True))
    user_repo.create(create_false_dto("doe", True))
    user_repo.create(create_false_dto("marcel", True))

    users = user_repo.get_all()

    assert len(users) == 3


def test_get_user_exist_by_id(user_repo):
    id_user = user_repo.create(create_false_dto("jhon", True))

    user = user_repo.get_by_id(id_user)

    assert isinstance(user, UserEntity)

    assert user.id == id_user


def test_any_user_exist_get_by_id(user_repo):
    user = user_repo.get_by_id(12)

    assert user is None


def test_cmp_userdto_in_user_get_by_id(user_repo):
    userdto = create_false_dto("jhon", True)

    # Creación de de usuario en db
    user_id = user_repo.create(userdto)

    user = user_repo.get_by_id(user_id)

    assert user is not None

    user_dict = user.model_dump()
    user_dict.pop("id")
    assert user_dict == userdto.model_dump()


def test_find_user_by_email(user_repo):
    user_dto = create_false_dto("jhon", True)

    user_repo.create(user_dto)

    user = user_repo.get_by_email(user_dto.email)

    assert isinstance(user, UserEntity)

    assert user.email == user_dto.email


def test_not_found_user_by_email(user_repo):
    user_dto = create_false_dto("jhon", True)

    user_repo.create(user_dto)

    user = user_repo.get_by_email(user_dto.email + ".es")

    assert user is None


def test_cmp_dto_user_with_user_repo(user_repo):
    user_dto = create_false_dto("jhon", True)

    user_repo.create(user_dto)

    user = user_repo.get_by_email(user_dto.email)
    user_dict = user.model_dump()
    user_dict.pop("id")

    assert user_dict == user_dto.model_dump()


def test_update_user_value(user_repo):
    user_id = user_repo.create(create_false_dto("jhon", True))

    before_user = user_repo.get_by_id(user_id)

    copy_user = before_user.model_copy()
    copy_user.name = "esteban"

    user_repo.update(copy_user)

    after_user = user_repo.get_by_id(copy_user.id)

    assert after_user.name == "esteban"


def test_raise_update_user_not_found(user_repo):
    user_id = user_repo.create(create_false_dto("jhon", True))
    user = user_repo.get_by_id(user_id)
    user_repo.delete(user.id)

    with pytest.raises(UserNotFoundError):
        user_repo.update(user)


def test_raise_delete_user_not_found(user_repo):
    with pytest.raises(UserNotFoundError):
        user_repo.delete(1)


def test_delete_user(user_repo):
    user_id = user_repo.create(create_false_dto("jhon", True))
    user_repo.delete(user_id)
    assert user_repo.get_by_id(user_id) is None
