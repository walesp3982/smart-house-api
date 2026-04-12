from pydantic import BaseModel, EmailStr, Field


class CredencialsUserRequest(BaseModel):
    email: EmailStr = Field(max_length=50)
    password: str = Field(max_length=64)


class VisibleDataUserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_verified: bool


class UserRegisterRequest(BaseModel):
    name: str = Field(max_length=50)
    email: EmailStr = Field(max_length=50)
    password: str = Field(max_length=64)


class UserVerifiedStatusResponse(BaseModel):
    status: bool
