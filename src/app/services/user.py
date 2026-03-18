from pwdlib import PasswordHash

from app.dto import UserDTO
from app.entities import User
from app.exceptions import (
    CredencialsUserIncorrect,
    UserNotCreated,
    UserNotFoundByEmailException,
)
from app.repository.interfaces import UserRepositoryProtocol
from app.schemas import CredencialsUser


class UserService:
    def __init__(self, repository: UserRepositoryProtocol):
        self.repository = repository
        self.password_hash = PasswordHash.recommended()

    def create_user(self, data: UserDTO) -> User:
        # Encriptación de contrasenia
        data.password = self.password_hash.hash(data.password)

        # Creación del usuario en la db
        user_id = self.repository.create(data)
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise UserNotCreated()
        return user

    def get_user_by_credencials(self, credencials: CredencialsUser) -> User:
        user = self.repository.get_by_email(credencials.email)

        if user is None:
            raise UserNotFoundByEmailException(credencials.email)

        # Comparación de contrasenia de las credenciales con la db
        if self.password_hash.verify(user.password, credencials.password):
            return user
        raise CredencialsUserIncorrect()
