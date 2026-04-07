from typing import Annotated, Literal

from pydantic import BaseModel, Field, HttpUrl, IPvAnyAddress


class StateDevice(BaseModel):
    state: Literal["on", "off"]


class DoorState(StateDevice):
    type: Literal["door"] = "door"


class LightState(StateDevice):
    type: Literal["light"] = "light"


class TemperatureState(StateDevice):
    type: Literal["temperature"] = "temperature"
    limit_temp: int
    enable_auto: bool


class MovementState(StateDevice):
    type: Literal["movement"] = "movement"


class CameraState(StateDevice):
    type: Literal["camera"] = "camera"
    stream_url: HttpUrl
    ip: IPvAnyAddress


StateDeviceOption = Annotated[
    DoorState | LightState | TemperatureState | MovementState | CameraState,
    Field(discriminator="type"),
]
