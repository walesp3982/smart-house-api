import secrets
from datetime import datetime, timedelta, timezone

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
from app.schemas import CredencialsUserResponse, UserRegisterRequest
from app.settings import general_settings


class UserService:
    """
    Clase que administra toda la lógica de negocio que
    tiene el Usuario
    """

    def __init__(self, repository: UserRepositoryProtocol):
        self.repository = repository
        self.password_hash = PasswordHash.recommended()

    @staticmethod
    def generate_token(dto: UserCreateDTO):
        """
        Modifica un dto ya existente para agregar el token de verificación
        y la fecha de expiration del token

        Args:
            dto: clase transportadora perteneciente a UserCreateDTO a
            modificarse

        Returns:
            No retorna nada :)
        """
        dto.verification_token = secrets.token_urlsafe(32)
        dto.verification_token_expired_at = datetime.now(timezone.utc) - timedelta(
            minutes=general_settings.expiration_minutes_email_verification
        )

    @staticmethod
    def set_validation_user(user_create_dto: UserCreateDTO):
        """
        Configuramos la validation del usuario en un user_create_dto


        Args:
            user_create_dto: clase transportadora perteneciente
            a UserCreateDTO que va a ser modificada

        Returns:
            No retorna nada


        Nota:
            Para configurar la validación de email usar las variables
            de entorno de general_settings
        """
        if general_settings.validation_email:
            UserService.generate_token(user_create_dto)
            user_create_dto.is_verified = False
        else:
            user_create_dto.is_verified = True

    def create_user(self, data: UserRegisterRequest) -> UserEntity:
        # Verificamos que el usuario no esté en la db
        if self.repository.get_by_email(data.email.lower()) is None:
            raise EmailAlreadyRegisterError

        # Encriptación de contrasenia
        data.password = self.password_hash.hash(data.password)

        # Creación de UserCreateDTO
        user_create_dto = UserCreateDTO(
            name=data.name,
            email=data.email.lower(),
            password=data.password,
            is_verified=False,
        )

        # Creamos la verificación (Se modifica según variable de entorno)
        self.set_validation_user(user_create_dto)

        # Creación del usuario en la db
        user_id = self.repository.create(user_create_dto)
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise UserNotCreatedError()
        return user

    def get_user_by_credencials(
        self, credencials: CredencialsUserResponse
    ) -> UserEntity:
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
