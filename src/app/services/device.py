from pwdlib import PasswordHash

from app.entities import DeviceEntity
from app.exceptions.device_exception import DeviceDuplicateUUIDError
from app.repository.interfaces import DeviceRepositoryProtocol
from app.schemas.device import CreateDeviceRequest


class DeviceService:
    def __init__(self, repository: DeviceRepositoryProtocol) -> None:
        self.repository = repository
        self.password_hash = PasswordHash.recommended()

    def create(self, request: CreateDeviceRequest) -> None:
        # Encriptamos el código de activación para más seguridad
        encrip_activation_code = self.password_hash.hash(request.activation_code)

        if self.repository.get_by_uuid(request.uuid):
            raise DeviceDuplicateUUIDError()

        data_device = DeviceEntity(
            activation_code=encrip_activation_code,
            device_uuid=request.uuid,
            type=request.type,
        )

        self.repository.create(data_device)
