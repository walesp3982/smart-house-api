from typing import Annotated, Literal

from pydantic import BaseModel, Field

from app.entities import DeviceType

ActionOption = Literal["on", "off"]


class DeviceBase(BaseModel):
    action: ActionOption


class Door(DeviceBase):
    type: Literal["door"] = "door"
    pass


class Light(DeviceBase):
    type: Literal["light"] = "light"
    pass


class MovementSensor(DeviceBase):
    type: Literal["movement"] = "movement"
    pass


class TemperatureSensor(DeviceBase):
    type: Literal["temperature"] = "temperature"
    enable_auto: bool
    has_limit: int


class Camera(DeviceBase):
    type: Literal["camera"] = "camera"
    pass


CommandJson = Annotated[
    Door | Light | MovementSensor | TemperatureSensor | Camera,
    Field(discriminator="type"),
]


def correctParams(type: DeviceType, json: CommandJson) -> bool:
    match type:
        case DeviceType.THERMOSTAT:
            return isinstance(json, TemperatureSensor)
        case DeviceType.LIGHT:
            return isinstance(json, Light)
        case DeviceType.MOVEMENT:
            return isinstance(json, MovementSensor)
        case DeviceType.DOOR:
            return isinstance(json, Door)
        case DeviceType.CAMERA:
            return isinstance(json, Camera)
