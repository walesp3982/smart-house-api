from app.api.schemas.command import CommandJson, correctParams
from app.exceptions.command_exception import IncorrectRequestCommandError
from app.infraestructure.mqtt.provider import MQTTProvider
from app.services.installed_device import InstalledDeviceService


class CommandDeviceService:
    def __init__(
        self,
        installed_device_service: InstalledDeviceService,
        mqtt_provider: MQTTProvider,
    ):
        self.installed_device_service = installed_device_service
        self.mqtt_provider = mqtt_provider

    def execute_command(
        self, installed_device_id: int, user_id: int, request: CommandJson
    ) -> None:
        """
        Obtenemos le installed_device_id y ejecutamos la acción utilizando mqtt broker

        Args:
            installed_device_id: id del dispositivo instalado a ejecutar el comando uwu
            request: el command que se va ejecutar

        Return:
            bool: Que significa que la acción ha sido realizada correctamente uwu

        Raises:
            InstalledDeviceNotFoundByIdError: Si el dispositivo no existe.
            InstalledDeviceUnauthorizedError: Si el dispositivo no pertenece al usuario.
        """
        installed_device = self.installed_device_service.get_by_id(
            installed_device_id, user_id
        )

        if not correctParams(installed_device.device.type, request):
            raise IncorrectRequestCommandError()

        topic = f"/{installed_device.device.device_uuid}/action"
        self.mqtt_provider.publish(topic, request.model_dump())
