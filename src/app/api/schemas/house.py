from typing import Optional

from pydantic import BaseModel


class UpdateHouseRequest(BaseModel):
    location: Optional[str]
    name: Optional[str]


class CreateHouseRequest(BaseModel):
    name: str
    location: str
    invitation_validation: bool = True
