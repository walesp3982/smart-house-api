from pydantic import BaseModel

from app.entities import DeviceEntity


class InstalledDeviceEntity(BaseModel):
    id: int | None = None
    name: str
    device_id: int
    house_id: int | None
    area_id: int | None
    user_id: int


class InstalledDeviceWithDevice(InstalledDeviceEntity):
    device: DeviceEntity
