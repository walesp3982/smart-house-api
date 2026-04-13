from pydantic import BaseModel, Field

from app.entities.device import DeviceEntity, DeviceType
from app.entities.installed_device import (
    InstalledDeviceEntity,
    InstalledDeviceWithDevice,
)


class CreateInstalledDeviceRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    uuid: str
    code_verification: str
    house_id: int | None = None
    area_id: int | None = None


class UpdateInstalledDeviceRequest(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=50)
    house_id: int | None = None
    area_id: int | None = None


class InstalledDeviceResponse(BaseModel):
    id: int
    name: str
    device_id: int
    house_id: int | None = None
    area_id: int | None = None

    @staticmethod
    def from_entity(entity: InstalledDeviceEntity):
        if entity.id is None:
            raise Exception("Id not started")
        return InstalledDeviceResponse(
            id=entity.id,
            name=entity.name,
            device_id=entity.device_id,
            house_id=entity.house_id,
            area_id=entity.area_id,
        )


class DeviceResponse(BaseModel):
    id: int
    device_uuid: str
    type: DeviceType

    @staticmethod
    def from_entity(entity: DeviceEntity):
        if entity.id is None:
            raise Exception("Id not started")
        return DeviceResponse(
            id=entity.id,
            device_uuid=entity.device_uuid,
            type=entity.type,
        )


class InstalledDeviceWithDeviceResponse(InstalledDeviceResponse):
    device: DeviceResponse

    @staticmethod
    def from_entity_compound(entity: InstalledDeviceWithDevice):
        if entity.id is None:
            raise Exception("Id not started")
        return InstalledDeviceWithDeviceResponse(
            id=entity.id,
            name=entity.name,
            device_id=entity.device_id,
            house_id=entity.house_id,
            area_id=entity.area_id,
            device=DeviceResponse.from_entity(entity.device),
        )
