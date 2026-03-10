from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    name: str

    model_config = SettingsConfigDict(env_prefix="DB_")
