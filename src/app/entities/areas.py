from enum import StrEnum

from pydantic import BaseModel


class AreaType(StrEnum):
    living_room = "living_room"
    bedroom = "bedroom"
    kitchen = "kitchen"
    outside = "outside"


class AreaEntity(BaseModel):
    id: int | None
    name: str
    type: AreaType
    house_id: int
