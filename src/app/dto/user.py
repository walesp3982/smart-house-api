from datetime import datetime

from pydantic import BaseModel, EmailStr


class CreateUserDTO(BaseModel):
    name: str
    email: EmailStr
    password: str
    is_verified: bool
    verification_token: str
    verification_token_expired_at: datetime
