import json
import threading
from typing import Any

import paho.mqtt.client as mqtt


class MQTTProvider:
    def __init__(self, client: mqtt.Client):
        self._client = client
        self._topics: dict[str, Any] = {}
        self._lock = threading.Lock()

        # Registrar callbacks
        self._client.on_message = self._on_message
        self._client.on_connect = self._on_connect

    # ── Callbacks internos ──────────────────────────────────────────────

    def _on_connect(self, client: mqtt.Client, userdata, flags, rc):
        if rc == 0:
            # Suscribirse a TODOS los topics al conectar (y al reconectar)
            client.subscribe("#")

    def _on_message(self, client, userdata, msg: mqtt.MQTTMessage):
        payload_raw = msg.payload.decode("utf-8")

        # Intentar parsear JSON, si falla guardar como string
        try:
            payload = json.loads(payload_raw)
        except json.JSONDecodeError, ValueError:
            payload = payload_raw

        with self._lock:
            self._topics[msg.topic] = payload

    # ── API pública ─────────────────────────────────────────────────────

    def get_topic(self, topic: str) -> Any | None:
        """Retorna el último valor recibido para un topic."""
        with self._lock:
            return self._topics.get(topic)

    def get_all_topics(self) -> dict[str, Any]:
        """Retorna una copia de todos los topics y sus últimos valores."""
        with self._lock:
            return dict(self._topics)

    def publish(self, topic: str, payload: Any, qos: int = 1, retain: bool = True):
        """
        Publica un valor en un topic.
        - retain=True → el broker guarda el último valor y lo entrega
          inmediatamente a nuevos suscriptores (ideal para estado del ESP32).
        """
        if isinstance(payload, (dict, list)):
            payload = json.dumps(payload)

        self._client.publish(topic, payload, qos=qos, retain=retain)
