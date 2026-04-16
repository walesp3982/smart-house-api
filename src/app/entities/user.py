from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserEntity(BaseModel):
    id: int | None = None
    name: str
    email: EmailStr
    password: str
    is_verified: bool = False
    verification_token: Optional[str] = None
    verification_token_expired_at: Optional[datetime] = None
    password_reset_token: Optional[str] = None
    password_reset_token_expired_at: Optional[datetime] = None
