from typing import Optional, Protocol

from pydantic import BaseModel

from app.entities.installed_device import InstalledDeviceEntity


class FilterInstalledDevices(BaseModel):
    house_id: int | None = None
    area_id: int | None = None
    user_id: int | None = None
    name: str | None = None


class InstalledDeviceRepositoryProtocol(Protocol):
    def create(self, data: InstalledDeviceEntity) -> int: ...
    def get_by_id(self, id: int) -> InstalledDeviceEntity | None: ...
    def get_all(
        self, filters: Optional[FilterInstalledDevices] = None
    ) -> list[InstalledDeviceEntity]: ...
    def update(self, data: InstalledDeviceEntity) -> None: ...
    def delete(self, id: int) -> None: ...
