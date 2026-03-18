from pydantic import BaseModel, EmailStr


class CredencialsUser(BaseModel):
    email: EmailStr
    password: str
