from typing import Optional

from pydantic import BaseModel, Field

from app.api.schemas.area import AreaResponse
from app.entities.house import HouseEntity, HouseWithAreas


class UpdateHouseRequest(BaseModel):
    location: Optional[str] = Field(default=None, max_length=50)
    name: Optional[str] = Field(default=None, max_length=50)


class CreateHouseRequest(BaseModel):
    name: str = Field(max_length=50)
    location: str | None = Field(default=None, max_length=50)
    invitation_validation: bool = True


class UpdateHouseResponse(BaseModel):
    message: str
    updated: bool


class HouseResponse(BaseModel):
    id: int
    name: str
    user_id: int
    location: str | None = None
    invitation_validation: bool

    @staticmethod
    def from_entity(entity: HouseEntity):
        if entity.id is None:
            raise Exception("Id is none: internal error")
        return HouseResponse(
            id=entity.id,
            name=entity.name,
            invitation_validation=entity.invitation_validation,
            location=entity.location,
            user_id=entity.user_id,
        )


class HouseWithAreasResponse(BaseModel):
    id: int
    name: str
    user_id: int
    location: str | None
    invitation_validation: bool
    areas: list[AreaResponse]

    @staticmethod
    def from_entity(entity: HouseWithAreas):
        if entity.id is None:
            raise Exception("Id not started")

        return HouseWithAreasResponse(
            id=entity.id,
            name=entity.name,
            user_id=entity.user_id,
            location=entity.location,
            invitation_validation=entity.invitation_validation,
            areas=[AreaResponse.from_entity(area) for area in entity.areas],
        )
