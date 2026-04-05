import secrets
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

from pwdlib import PasswordHash
from pydantic import NameEmail

from app.api.schemas import CredencialsUserRequest, UserRegisterRequest
from app.entities import UserEntity
from app.exceptions import (
    CredencialsUserIncorrectError,
    EmailAlreadyRegisterError,
    UserNotCreatedError,
    UserNotFoundByEmailError,
    UserNotFoundByIdError,
    UserNotFoundError,
)
from app.exceptions.user_exceptions import UserNotFoundByToken, VerificationEmailInvalid
from app.repository.interfaces import UserRepositoryProtocol
from app.settings import general_settings
from app.settings.time import normalize, utcnow

from ..infraestructure.email.email import (
    EmailSender,
    FactoryEmailContent,
)


class UserService:
    """
    Clase que administra toda la lógica de negocio que
    tiene el Usuario
    """

    def __init__(self, repository: UserRepositoryProtocol):
        self.repository = repository
        self.password_hash = PasswordHash.recommended()
        self.email_sender = EmailSender()

    @staticmethod
    def generate_token(dto: UserEntity):
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
    def set_validation_user(user_create_dto: UserEntity):
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

    async def send_email_verification(self, user: UserEntity, url_verification: str):
        """
        Enviamos una verificación de email

        Args:
        user: UserEntity necesario para sacar las variables
        url_verificación: url relativo
        """
        if not user.is_verified:
            if user.verification_token is None:
                return
            host = str(general_settings.app_host).rstrip("/")
            url_verification = url_verification.lstrip("/").rstrip("/")
            safe_token = quote(user.verification_token, safe="")
            final_url = f"{str(host)}/{url_verification}/{safe_token}"
            content = FactoryEmailContent.create(
                type="verification",
                url=final_url,
                name=user.name,
            ).generate()
            await self.email_sender.execute(
                html=content,
                email_address=[NameEmail(name=user.name, email=user.email)],
            )

    def create_user(self, data: UserRegisterRequest) -> UserEntity:
        """
        Crea un usuario dentro de la base de datos

        Args:
            data: UserRegisterRequest con información
            necesaria para crear el usuario

        Returns:
            UserEntity: Domain del usuario

        Nota:
        -   Se revisa que el email no haya sido registrado anteriormente
        -   Aquí se hashea la password antes de guardarla en el Repositorio

        """
        # Verificamos que el usuario no esté en la db
        if self.repository.get_by_email(data.email.lower()) is not None:
            raise EmailAlreadyRegisterError

        # Encriptación de contrasenia
        data.password = self.password_hash.hash(data.password)

        # Creación de UserCreateDTO
        user_create_dto = UserEntity(
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

    async def register_user(self, data: UserRegisterRequest, url: str) -> UserEntity:
        """
        Guardamos el usuario en el Repositorio y mandamos un email de confirmación
        (Depende de las variables de entorno)

        Args:
        data: Request que se procesa en el Servicio
        url: url relativa para verificar el email
        """
        user = self.create_user(data)
        await self.send_email_verification(user, url)
        return user

    def get_user_by_credencials(
        self, credencials: CredencialsUserRequest
    ) -> UserEntity:
        """
        Obtener el usuario mediante las credenciales

        Args:
        credencials: email y password para verificar el usuario

        Returns:
        - UserEntity: almacenada anteriormente en la DB

        Note:
        - Si el email no existe se manda una Exception
        - Si la password no coincide con la DB se lanza una Exception
        """
        user = self.repository.get_by_email(credencials.email)

        if user is None:
            raise UserNotFoundByEmailError(credencials.email)

        # Comparación de contrasenia de las credenciales con la db
        if self.password_hash.verify(credencials.password, user.password):
            return user
        raise CredencialsUserIncorrectError()

    def get_user_by_id(self, user_id: int) -> UserEntity:
        """
        Obtenemos un Usuario mediante el user_id
        """
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundByIdError(user_id)
        return user

    def verified(self, token: str) -> None:
        """
        Verificamos al usuario mediante el token
        """
        user = self.repository.get_by_token(token)
        if user is None:
            raise UserNotFoundByToken()
        if user.verification_token_expired_at is None:
            raise VerificationEmailInvalid()
        if utcnow() < normalize(user.verification_token_expired_at):
            raise VerificationEmailInvalid()
        user.is_verified = True
        self.repository.update(user)

    def user_is_verified(self, user_id: int) -> bool:
        """
        Vemos que el usuario esté verificado
        """
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)

        return user.is_verified
