from pydantic import BaseModel, Field

from app.entities import AreaEntity, AreaType
from app.exceptions.areas_exceptions import AreaEntityIdNotStartedError


class UpdateAreaRequest(BaseModel):
    name: str | None = Field(default=None, max_length=50)
    type: AreaType | None = None


class CreateAreaRequest(BaseModel):
    name: str = Field(max_length=50)
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
