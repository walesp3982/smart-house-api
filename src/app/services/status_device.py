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
        return f"/{uuid}/value"

    @staticmethod
    def building_json_response(
        installed_device: InstalledDeviceWithDevice, json_mqtt: Any
    ) -> StateDeviceOption:
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

    def execute(self, user_id: int, installed_device_id: int) -> StateDeviceOption:
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
