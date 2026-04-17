from fastapi_mail import ConnectionConfig
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class EmailSettings(BaseSettings):
    SERVER: str
    PORT: int
    USERNAME: str
    PASSWORD: str
    STARTTLS: bool
    SSL_TLS: bool
    USE_CREDENTIALS: bool
    FROM: str
    model_config = SettingsConfigDict(env_file=".env", env_prefix="EMAIL_", extra="ignore")


email_settings = EmailSettings()  # pyright: ignore[reportCallIssue]

connection_config_email = ConnectionConfig(
    MAIL_USERNAME=email_settings.USERNAME,
    MAIL_PASSWORD=SecretStr(email_settings.PASSWORD),
    MAIL_SSL_TLS=email_settings.SSL_TLS,
    MAIL_SERVER=email_settings.SERVER,
    MAIL_PORT=email_settings.PORT,
    MAIL_STARTTLS=email_settings.STARTTLS,
    MAIL_FROM=email_settings.FROM,
    USE_CREDENTIALS=email_settings.USE_CREDENTIALS,
)
