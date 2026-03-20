from enum import StrEnum

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


general_settings = GeneralSettings()


class JWTSettings(BaseSettings):
    secret_key: str
    expiration_minutes: int = 30

    model_config = SettingsConfigDict(
        env_prefix="JWT_", env_file=".env", extra="ignore"
    )


jwt_settings = JWTSettings()  # pyright: ignore[reportCallIssue]
