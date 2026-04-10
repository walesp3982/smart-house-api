from pydantic import BaseModel

from .areas import AreaEntity


class HouseEntity(BaseModel):
    id: int | None = None
    name: str
    user_id: int
    location: str | None = None
    invitation_validation: bool


class HouseWithAreas(BaseModel):
    id: int | None = None
    name: str
    user_id: int
    location: str | None = None
    invitation_validation: bool
    areas: list[AreaEntity]
