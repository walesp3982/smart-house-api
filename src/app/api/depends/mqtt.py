from typing import Annotated

from fastapi import Depends

from app.infraestructure.mqtt.client import MQTTClient
from app.infraestructure.mqtt.provider import MQTTProvider

_mqtt_provider: MQTTProvider | None = None


def init_mqtt_provider() -> None:
    """
    Inicializacióndel mqtt provider
    """
    global _mqtt_provider
    _mqtt_provider = MQTTProvider(MQTTClient.get())


def get_mqtt_provider() -> MQTTProvider:
    if _mqtt_provider is None:
        raise RuntimeError("MQTTProvider no fue inicializado")
    return _mqtt_provider


MQTTProviderDep = Annotated[MQTTProvider, Depends(get_mqtt_provider)]
