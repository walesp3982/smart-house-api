from typing import Optional

from pydantic import BaseModel, Field


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
