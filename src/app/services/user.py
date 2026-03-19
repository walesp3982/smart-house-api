from datetime import datetime

from pwdlib import PasswordHash

from app.dto import UserCreateDTO
from app.entities import UserEntity
from app.exceptions import (
    CredencialsUserIncorrectError,
    EmailAlreadyRegisterError,
    UserNotCreatedError,
    UserNotFoundByEmailError,
    UserNotFoundByIdError,
)
from app.repository.interfaces import UserRepositoryProtocol
from app.schemas import CredencialsUser, UserRegisterRequest


class UserService:
    def __init__(self, repository: UserRepositoryProtocol):
        self.repository = repository
        self.password_hash = PasswordHash.recommended()

    def create_user(self, data: UserRegisterRequest) -> UserEntity:
        # Encriptación de contrasenia
        data.password = self.password_hash.hash(data.password)

        # Creación de UserCreateDTO en la db
        user_create_dto = UserCreateDTO(
            name=data.name,
            email=data.email,
            password=data.password,
            is_verified=True,
            verification_token="asdfasdf",
            verification_token_expired_at=datetime.now(),
        )
        # Creación del usuario en la db
        user_id = self.repository.create(user_create_dto)
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise UserNotCreatedError()
        return user

    def get_user_by_credencials(self, credencials: CredencialsUser) -> UserEntity:
        user = self.repository.get_by_email(credencials.email)

        if user is None:
            raise UserNotFoundByEmailError(credencials.email)

        # Comparación de contrasenia de las credenciales con la db
        if self.password_hash.verify(credencials.password, user.password):
            return user
        raise CredencialsUserIncorrectError()

    def get_user_by_id(self, user_id: int) -> UserEntity:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundByIdError(user_id)
        return user

    def register(self, user_dto: UserCreateDTO) -> UserEntity:

        # Vemos que el usuario no exista en la db
        if self.repository.get_by_email(user_dto.email) is None:
            raise EmailAlreadyRegisterError

        # Creamos el usuario
        user_id = self.repository.create(user_dto)

        return self.get_user_by_id(user_id)
