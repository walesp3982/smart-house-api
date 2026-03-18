from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

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

    def encode(self, data: dict[str, Any]) -> str:
        payload = data.copy()
        payload["exp"] = self.get_datetime_expiration()
        payload["iat"] = datetime.now(timezone.utc)
        encoded = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return encoded

    def decode(self, encoded: str) -> dict[str, Any]:
        try:
            decode = jwt.decode(encoded, self.secret_key, algorithms=[self.algorithm])
            return decode
        except jwt.ExpiredSignatureError:
            raise Exception("Jwt Ya expirada")
        except jwt.InvalidTokenError as e:
            raise Exception(f"Token inválido: {e}")
