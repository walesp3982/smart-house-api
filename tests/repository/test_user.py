# Estamos testeando el repositorio de usuario,
# que es el encargado de manejar la lógica de negocio
# relacionada con los usuarios, como crear un nuevo usuario,
# #obtener un usuario por su ID, etc.
from app.dto import UserDTO


def test_create_user(user_repo):
    user_dto = UserDTO(
        name="John Doe", email="john.doe@example.com", password="password"
    )
    user_id = user_repo.create(user_dto)
    assert user_id is not None
    users = user_repo.getAll()
    assert len(users) == 1
