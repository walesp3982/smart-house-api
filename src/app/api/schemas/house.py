from typing import Optional

from pydantic import BaseModel


class UpdateHouseRequest(BaseModel):
    location: Optional[str]
    name: Optional[str]


class CreateHouseRequest(BaseModel):
    name: str
    location: str | None = None
    invitation_validation: bool = True


class UpdateHouseResponse(BaseModel):
    message: str
    updated: bool
