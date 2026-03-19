from pydantic import BaseModel, EmailStr


class CredencialsUser(BaseModel):
    email: EmailStr
    password: str


class VisibleDataUser(BaseModel):
    id: int
    name: str
    email: EmailStr


class UserRegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
