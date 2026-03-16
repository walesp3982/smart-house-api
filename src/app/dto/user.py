from pydantic import BaseModel


class UserDTO(BaseModel):
    name: str
    email: str
    password: str
