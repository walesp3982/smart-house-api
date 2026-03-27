from pydantic import BaseModel

from app.entities import AreaType


class UpdateAreaRequest(BaseModel):
    name: str | None = None
    type: AreaType | None = None


class CreateAreaRequest(BaseModel):
    name: str
    type: AreaType
