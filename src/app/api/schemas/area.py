from pydantic import BaseModel

from app.entities import AreaEntity, AreaType
from app.exceptions.areas_exceptions import AreaEntityIdNotStartedError


class UpdateAreaRequest(BaseModel):
    name: str | None = None
    type: AreaType | None = None


class CreateAreaRequest(BaseModel):
    name: str
    type: AreaType


class AreaResponse(BaseModel):
    id: int
    name: str
    type: AreaType
    house_id: int

    @classmethod
    def from_entity(cls, entity: AreaEntity) -> "AreaResponse":
        if entity.id is None:
            raise AreaEntityIdNotStartedError()
        return cls(
            id=entity.id, name=entity.name, type=entity.type, house_id=entity.house_id
        )
