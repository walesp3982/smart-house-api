from pydantic import BaseModel, EmailStr


class UserDTO(BaseModel):
    name: str
    email: EmailStr
    password: str
