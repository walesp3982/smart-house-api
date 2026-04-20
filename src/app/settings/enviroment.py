from enum import StrEnum
from typing import Literal

from pydantic import AnyUrl, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class AvailableDatabases(StrEnum):
    sqlite = "sqlite"
    mysql = "mysql"
    postgresql = "postgresql"


class DatabaseSettings(BaseSettings):
    type: AvailableDatabases
    host: str
    port: int
    user: str
    password: str
    name_db: str

    model_config = SettingsConfigDict(env_prefix="DB_", env_file=".env", extra="ignore")


database_settings = DatabaseSettings()  # pyright: ignore[reportCallIssue]


class GeneralSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    debug: bool = False
    sql_debug: bool = False
    cors_origins: set[str] = set()
    validation_email: bool = False
    expiration_minutes_email_verification: int = (
        120  # 2 horas para tener válidar el expiration minutes
    )
    expiration_minutes_password_reset: int = (
        60  # 1 hora para restablecimiento de contraseña
    )
    app_host: AnyUrl = AnyUrl("http://localhost:8000")
    app_name: str = "Application"
    frontend_url: HttpUrl = HttpUrl("http:localhost:3000")


general_settings = GeneralSettings()  # pyright: ignore[reportCallIssue]


class JWTSettings(BaseSettings):
    secret_key: str
    expiration_minutes: int = 30

    model_config = SettingsConfigDict(
        env_prefix="JWT_", env_file=".env", extra="ignore"
    )


jwt_settings = JWTSettings()  # pyright: ignore[reportCallIssue]

"""
Helpers para url de frontend verification-email
"""
QueryVerifyEmail = Literal["success", "expired", "invalid"]


def helper_url_verify_check_email(query: QueryVerifyEmail):
    """
    Helper que ayuda al buildar la url para obtener el resultado del email
    """
    global general_settings

    final_url = f"{general_settings.frontend_url}/verify-email/callback?status={query}"

    return final_url


def helper_url_reset_password() -> str:
    """
    Helper para construir la URL pública de restablecimiento de contraseña.
    """
    return f"{general_settings.frontend_url}/reset-password"
