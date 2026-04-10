from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.infraestructure.mqtt.client import MQTTClient
from app.infraestructure.mqtt.provider import MQTTProvider


@lru_cache(maxsize=1)
def get_mqtt_provider() -> MQTTProvider:
    """
    lru_cache garantiza que solo se crea UNA instancia durante
    all the lifetime de la aplicación (singleton)
    """
    client = MQTTClient.get()
    return MQTTProvider(client)


MQTTProviderDep = Annotated[MQTTProvider, Depends(get_mqtt_provider)]
