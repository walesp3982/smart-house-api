from typing import Optional, Protocol

from pydantic import BaseModel

from app.entities import AreaEntity


class FilterAreas(BaseModel):
    with_devices = True


class AreaProtocol(Protocol):
    def create(self, data: AreaEntity) -> int: ...
    def get_by_id(self, id: int) -> AreaEntity | None: ...
    def get_all(self, filters: Optional[FilterAreas] = None) -> list[AreaEntity]: ...
    def update(self, data: AreaEntity) -> None: ...
    def delete(self, id: int) -> None: ...
