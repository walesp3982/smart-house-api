from typing import Protocol, Union

from pydantic import BaseModel

from app.entities import HouseEntity
from app.entities.house import HouseWithAreas


class FilterGetAllHouse(BaseModel):
    user_id: int | None = None
    include_areas: bool = False


class HouseRepositoryProtocol(Protocol):
    def create(self, data: HouseEntity) -> int: ...
    def get_all(
        self, filters: FilterGetAllHouse | None = None
    ) -> Union[list[HouseEntity], list[HouseWithAreas]]: ...
    def get_by_id(self, house_id: int) -> HouseEntity | None: ...
    def update(self, data: HouseEntity) -> None: ...
    def delete(self, house_id: int) -> None: ...
