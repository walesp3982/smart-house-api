from pydantic import BaseModel, EmailStr


class CredencialsUserRequest(BaseModel):
    email: EmailStr
    password: str


class VisibleDataUserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_verified: bool


class UserRegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserVerifiedStatusResponse(BaseModel):
    status: bool
