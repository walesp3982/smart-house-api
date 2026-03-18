from pydantic import BaseModel, EmailStr


class CredencialsUser(BaseModel):
    email: EmailStr
    password: str


class VisibleDataUser(BaseModel):
    id: int
    name: str
    email: EmailStr
