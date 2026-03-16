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


general_settings = GeneralSettings()
