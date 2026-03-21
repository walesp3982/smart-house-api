from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreateDTO(BaseModel):
    name: str
    email: EmailStr
    password: str
    is_verified: bool = False
    verification_token: Optional[str] = None
    verification_token_expired_at: Optional[datetime] = None
