from pydantic import BaseModel


class HouseEntity(BaseModel):
    id: int | None = None
    name: str
    user_id: int
    location: str | None = None
    invitation_validation: bool
