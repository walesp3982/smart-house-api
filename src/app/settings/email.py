from fastapi_mail import ConnectionConfig
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class SMTPSettings(BaseSettings):
    SERVER: str
    PORT_TLS: int
    USERNAME: str
    PASSWORD: str

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="SMTP_", extra="ignore"
    )


smtp_settings = SMTPSettings()  # pyright: ignore[reportCallIssue]

connection_config_smtp = ConnectionConfig(
    MAIL_USERNAME=smtp_settings.USERNAME,
    MAIL_PASSWORD=SecretStr(smtp_settings.PASSWORD),
    MAIL_SSL_TLS=False,
    MAIL_SERVER=smtp_settings.SERVER,
    MAIL_PORT=smtp_settings.PORT_TLS,
    MAIL_STARTTLS=True,
    MAIL_FROM=smtp_settings.USERNAME,
)
