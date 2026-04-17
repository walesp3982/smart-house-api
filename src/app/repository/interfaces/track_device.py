from typing import Optional, Protocol

from pydantic import BaseModel

from app.entities.track_device import TrackDevice


class FilterTrackDevices(BaseModel):
    device_id: int | None = None
    house_id: int | None = None
    user_id: int | None = None
    status: str | None = None


class TrackDeviceRepositoryProtocol(Protocol):
    def create(self, data: TrackDevice) -> int: ...
    def get_by_id(self, id: int) -> TrackDevice | None: ...
    def get_all(self, filters: Optional[FilterTrackDevices] = None) -> list[TrackDevice]: ...
    def update(self, data: TrackDevice) -> None: ...
    def delete(self, id: int) -> None: ...
