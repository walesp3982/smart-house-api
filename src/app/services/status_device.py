from typing import Any

from app.api.schemas.state_device import (
    CameraState,
    DoorState,
    LightState,
    MovementState,
    StateDeviceOption,
    TemperatureState,
)
from app.entities.device import DeviceType
from app.entities.installed_device import (
    InstalledDeviceWithDevice,
)
from app.exceptions.command_exception import StateNotFoundDeviceError
from app.infraestructure.mqtt.provider import MQTTProvider
from app.services.installed_device import InstalledDeviceService


class StateDeviceService:
    def __init__(
        self,
        installed_devices_service: InstalledDeviceService,
        mqtt_provider: MQTTProvider,
    ):
        self.installed_devices_service = installed_devices_service
        self.mqtt_provider = mqtt_provider

    @staticmethod
    def get_state_topics(uuid: str):
        """
        Generación del topic a consultar en el MQTT

        Args:
            uuid: ID del dispositivo

        Return:
            string: Topic del mqtt
        """
        return f"/{uuid}/value"

    @staticmethod
    def building_json_response(
        installed_device: InstalledDeviceWithDevice, json_mqtt: Any
    ) -> StateDeviceOption:
        """
        Generamos la response para el cliente
        Args:
            installed_device: dispositivo al que actualmente se está solicitando
            información
            json_mqtt: Respuesta del mqtt_broker

        Return:
            StateDeviceOption: Conjunto de response respecto a un dispositivo
        """
        match installed_device.device.type:
            case DeviceType.LIGHT:
                return LightState(**json_mqtt)
            case DeviceType.DOOR:
                return DoorState(**json_mqtt)
            case DeviceType.CAMERA:
                return CameraState(**json_mqtt)
            case DeviceType.THERMOSTAT:
                return TemperatureState(**json_mqtt)
            case DeviceType.MOVEMENT:
                return MovementState(**json_mqtt)

    @staticmethod
    def get_topic_online(chip_id: str) -> str:
        return f"/{chip_id}/status"

    def is_online(self, installed_device: InstalledDeviceWithDevice) -> bool:
        if installed_device.device.chip_id is None:
            return True

        status: str | None = self.mqtt_provider.get_topic(
            self.get_state_topics(installed_device.device.chip_id)
        )

        if status is None:
            return False
        if status == "online":
            return True
        return False

    def execute(self, user_id: int, installed_device_id: int) -> StateDeviceOption:
        """
        Obtenemos el estado actual del dispositivo en el MQTTBroker

        Args:
            user_id: Id del usuario que del dispositivo
            installed_device_id: Id del device

        Return:
            StateDeviceOption: Response buildada para el websocket

        Raises:
            StateNotFoundDeviceError: Cuando el dispositivo no
            tiene algún estado en el MQTT
        """
        installed_device = self.installed_devices_service.get_by_id(
            installed_device_id, user_id
        )

        data = self.mqtt_provider.get_topic(
            StateDeviceService.get_state_topics(
                installed_device.device.device_uuid,
            )
        )

        if data is None:
            raise StateNotFoundDeviceError

        response = self.building_json_response(installed_device, data)

        return response
