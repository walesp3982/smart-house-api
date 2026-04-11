from pwdlib import PasswordHash

from app.api.schemas.installed_device import (
    CreateInstalledDeviceRequest,
    UpdateInstalledDeviceRequest,
)
from app.entities.installed_device import (
    InstalledDeviceEntity,
    InstalledDeviceWithDevice,
)
from app.exceptions.installed_device_exceptions import (
    InstalledDeviceAlreadyRegisteredError,
    InstalledDeviceNotFoundByIdError,
    InstalledDeviceUnauthorizedError,
    InstalledDeviceVerificationError,
)
from app.repository.interfaces import DeviceRepositoryProtocol
from app.repository.interfaces.installed_device import InstalledDeviceRepositoryProtocol


class InstalledDeviceService:
    def __init__(
        self,
        installed_device_repository: InstalledDeviceRepositoryProtocol,
        device_repository: DeviceRepositoryProtocol,
    ) -> None:
        self.repository = installed_device_repository
        self.device_repository = device_repository
        self.password_hash = PasswordHash.recommended()

    def get_all(self, user_id: int) -> list[InstalledDeviceEntity]:
        """Obtiene todos los installed_devices del usuario.

        Args:
            user_id (int): ID del usuario propietario de los dispositivos.

        Returns:
            list[InstalledDeviceEntity]: Lista de dispositivos instalados del usuario.
        """
        return self.repository.get_all_by_user_id(user_id)

    def get_all_with_device(self, user_id: int) -> list[InstalledDeviceWithDevice]:
        """Obtiene todos los installed_devices con información del device.

        Args:
            user_id (int): ID del usuario propietario de los dispositivos.

        Returns:
            list[InstalledDeviceWithDevice]: Lista de dispositivos con info del
            device.
        """
        return self.repository.get_all_with_device(user_id)

    def get_by_id(
        self, installed_device_id: int, user_id: int
    ) -> InstalledDeviceWithDevice:
        """Obtiene un installed_device con la información del device asociado.

        Args:
            installed_device_id (int): ID del installed_device a obtener.
            user_id (int): ID del usuario (para verificar propiedad).

        Returns:
            InstalledDeviceWithDevice: El dispositivo instalado con información
            del device.

        Raises:
            InstalledDeviceNotFoundByIdError: Si el dispositivo no existe.
            InstalledDeviceUnauthorizedError: Si el dispositivo no pertenece al usuario.
        """
        device = self.repository.get_with_device(installed_device_id)
        if device is None:
            raise InstalledDeviceNotFoundByIdError(installed_device_id)

        if device.user_id != user_id:
            raise InstalledDeviceUnauthorizedError(installed_device_id)

        return device

    def create(self, user_id: int, request: CreateInstalledDeviceRequest) -> int:
        """Registra un nuevo installed_device para el usuario.

        El código de verificación se verifica contra el hash almacenado en el device.
        Se asegura que ningún otro usuario tenga registrado ese dispositivo.

        Args:
            user_id (int): ID del usuario que registra el dispositivo.
            request (CreateInstalledDeviceRequest): Datos del dispositivo a registrar
                (name, uuid, code_verification, house_id, area_id).

        Returns:
            int: ID del nuevo installed_device creado.

        Raises:
            InstalledDeviceNotFoundByIdError: Si el device con uuid no existe.
            InstalledDeviceAlreadyRegisteredError: Si el dispositivo ya está registrado
                por otro usuario.
            InstalledDeviceVerificationError: Si el código de verificación es inválido.
        """
        # Obtener el device por uuid
        device = self.device_repository.get_by_uuid(request.uuid)
        if device is None or device.id is None:
            raise InstalledDeviceNotFoundByIdError(0)

        # Verificar que el código de verificación es correcto
        try:
            is_valid = self.password_hash.verify(
                request.code_verification, device.activation_code
            )
            if not is_valid:
                raise InstalledDeviceVerificationError()
        except Exception:
            raise InstalledDeviceVerificationError()

        # Verificar que ningún otro usuario tenga este device registrado
        existing = self.repository.get_by_uuid(request.uuid)
        if existing is not None:
            raise InstalledDeviceAlreadyRegisteredError(request.uuid)

        # Crear el installed_device
        installed_device = InstalledDeviceEntity(
            name=request.name,
            device_id=device.id,
            house_id=request.house_id,
            area_id=request.area_id,
            user_id=user_id,
        )

        return self.repository.create(installed_device)

    def update(
        self,
        installed_device_id: int,
        user_id: int,
        request: UpdateInstalledDeviceRequest,
    ) -> None:
        """Actualiza parcialmente un installed_device.

        Los campos que NO pueden modificarse son: id y device_id (por reglas de
          negocio).

        Args:
            installed_device_id (int): ID del dispositivo a actualizar.
            user_id (int): ID del usuario (para verificar propiedad).
            request (UpdateInstalledDeviceRequest): Datos a actualizar (name, house_id,
            area_id).

        Raises:
            InstalledDeviceNotFoundByIdError: Si el dispositivo no existe.
            InstalledDeviceUnauthorizedError: Si el dispositivo no pertenece al usuario.
        """
        # Obtener el dispositivo actual
        device = self.repository.get_by_id(installed_device_id)
        if device is None:
            raise InstalledDeviceNotFoundByIdError(installed_device_id)

        if device.user_id != user_id:
            raise InstalledDeviceUnauthorizedError(installed_device_id)

        # Actualizar solo los campos permitidos
        update_data = request.model_dump(exclude_none=True)

        if len(update_data) == 0:
            return

        # Preparar la entidad actualizada
        updated_device = InstalledDeviceEntity(
            id=device.id,
            name=update_data.get("name", device.name),
            device_id=device.device_id,
            house_id=update_data.get("house_id", device.house_id),
            area_id=update_data.get("area_id", device.area_id),
            user_id=device.user_id,
        )

        self.repository.update(updated_device)

    def delete(self, installed_device_id: int, user_id: int) -> None:
        """Elimina un installed_device del usuario.

        Una vez eliminado, el device puede ser registrado por otro usuario.

        Args:
            installed_device_id (int): ID del dispositivo a eliminar.
            user_id (int): ID del usuario (para verificar propiedad).

        Raises:
            InstalledDeviceNotFoundByIdError: Si el dispositivo no existe.
            InstalledDeviceUnauthorizedError: Si el dispositivo no pertenece al usuario.
        """
        # Obtener el dispositivo
        device = self.repository.get_by_id(installed_device_id)
        if device is None:
            raise InstalledDeviceNotFoundByIdError(installed_device_id)

        if device.user_id != user_id:
            raise InstalledDeviceUnauthorizedError(installed_device_id)

        self.repository.delete(installed_device_id)
