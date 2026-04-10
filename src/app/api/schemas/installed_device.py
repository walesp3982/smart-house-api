from pydantic import BaseModel, Field


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
    id: int | None = None
    name: str
    device_id: int
    house_id: int | None = None
    area_id: int | None = None


class DeviceResponse(BaseModel):
    id: int | None = None
    device_uuid: str
    type: str


class InstalledDeviceWithDeviceResponse(InstalledDeviceResponse):
    device: DeviceResponse
