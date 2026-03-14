from enum import StrEnum

from pydantic_settings import BaseSettings, SettingsConfigDict


class AvailableDatabases(StrEnum):
    sqlite = "sqlite"
    mysql = "mysql"


class DatabaseSettings(BaseSettings):
    type: AvailableDatabases
    host: str
    port: int
    user: str
    password: str
    name_db: str

    model_config = SettingsConfigDict(env_prefix="DB_")


database_settings = DatabaseSettings()
