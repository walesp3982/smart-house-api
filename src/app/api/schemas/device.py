from pydantic import BaseModel

from app.entities import DeviceType


class CreateDeviceRequest(BaseModel):
    uuid: str
    type: DeviceType
    activation_code: str
    chip_id: str | None


class CreateDeviceResponse(BaseModel):
    message: str
