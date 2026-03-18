from datetime import datetime, timedelta, timezone

import jwt

from app.schemas import Payload
from app.settings import jwt_settings


class TokenJWTService:
    def __init__(self):
        self.secret_key = jwt_settings.secret_key
        self.algorithm = "HS256"
        self.expiration_minutes = jwt_settings.expiration_minutes

    def get_datetime_expiration(self) -> datetime:
        datetime_expiration = datetime.now(tz=timezone.utc) + timedelta(
            minutes=self.expiration_minutes
        )

        return datetime_expiration

    def encode(self, user_id: int, name: str) -> str:
        exp = self.get_datetime_expiration()
        iat = datetime.now(timezone.utc)
        payload = Payload(sub=str(user_id), name=name, exp=exp, iat=iat)
        encoded = jwt.encode(
            payload.model_dump(),
            self.secret_key,
            algorithm=self.algorithm,
        )
        return encoded

    def decode(self, encoded: str) -> Payload:
        try:
            decode = jwt.decode(encoded, self.secret_key, algorithms=[self.algorithm])
            payload = Payload(**decode)
            return payload
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError("Jwt Ya expirada")
        except jwt.InvalidTokenError as e:
            raise jwt.InvalidTokenError(f"Token inválido: {e}")
