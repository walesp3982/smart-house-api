from typing import Protocol

from pydantic import BaseModel

from app.entities import HouseEntity


class FilterGetAllHouse(BaseModel):
    user_id: int | None = None


class HouseRepositoryProtocol(Protocol):
    def create(self, data: HouseEntity) -> int: ...
    def get_all(
        self, filters: FilterGetAllHouse | None = None
    ) -> list[HouseEntity]: ...
    def get_by_id(self, house_id: int) -> HouseEntity | None: ...
    def update(self, data: HouseEntity) -> None: ...
    def delete(self, house_id: int) -> None: ...
