from enum import StrEnum

from pydantic import BaseModel


class DeviceType(StrEnum):
    LIGHT = "light"
    THERMOSTAT = "thermostat"
    CAMERA = "camera"
    DOOR = "door"
    MOVEMENT = "movement"


class DeviceEntity(BaseModel):
    id: None | int = None
    device_uuid: str
    activation_code: str
    type: DeviceType
