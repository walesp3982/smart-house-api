from pydantic_settings import BaseSettings, SettingsConfigDict


class MQTTBrokerSettings(BaseSettings):
    host: str = "localhose"
    port: int = 1883
    keepalive: int = 60
    username: str = ""
    password: str = ""
    client_id: str = "smart-house-api"

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_prefix="MQTT_"
    )


mqtt_broker_settings = MQTTBrokerSettings()
