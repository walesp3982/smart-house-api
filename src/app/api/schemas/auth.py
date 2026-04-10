from datetime import datetime

from pydantic import BaseModel


class Payload(BaseModel):
    sub: str
    name: str
    exp: datetime
    iat: datetime


class Token(BaseModel):
    access_token: str
    token_type: str
