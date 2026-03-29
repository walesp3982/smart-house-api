import paho.mqtt.client as mqtt

from app.settings.mqtt import mqtt_broker_settings


class MQTTClient(object):
    _client: mqtt.Client | None = None

    @classmethod
    def connect(cls):
        if cls._client is not None:
            return
        cls._client = mqtt.Client(
            client_id=mqtt_broker_settings.client_id,
        )

        if mqtt_broker_settings.username:
            cls._client.username_pw_set(
                mqtt_broker_settings.username,
                mqtt_broker_settings.password,
            )

        cls._client.connect(
            mqtt_broker_settings.host,
            mqtt_broker_settings.port,
            mqtt_broker_settings.keepalive,
        )

        cls._client.loop_start()

    @classmethod
    def disconnect(cls):
        if cls._client:
            cls._client.loop_stop()
            cls._client.disconnect()
            cls._client = None

    @classmethod
    def get(cls) -> mqtt.Client:
        if cls._client is None:
            raise RuntimeError("Cliente MQTT no fue inicializado")
        return cls._client
