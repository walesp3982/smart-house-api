import json
import subprocess
from typing import Any

from app.api.schemas.command import (
    Camera,
    Door,
    Light,
    MovementSensor,
    TemperatureSensor,
)
from app.entities.device import DeviceType
from app.entities.installed_device import InstalledDeviceWithDevice
from app.entities.track_device import StatusDevice, TrackDevice
from app.infraestructure.mqtt.provider import MQTTProvider
from app.services.command_device import CommandDeviceService
from app.services.installed_device import InstalledDeviceService
from app.services.status_device import StateDeviceService
from app.services.track_device import TrackDeviceService
from app.settings.time import utcnow


class OllamaConversationService:
    def __init__(
        self,
        installed_device_service: InstalledDeviceService,
        state_device_service: StateDeviceService,
        command_device_service: CommandDeviceService,
        track_device_service: TrackDeviceService,
        mqtt_provider: MQTTProvider,
    ):
        self.installed_device_service = installed_device_service
        self.state_device_service = state_device_service
        self.command_device_service = command_device_service
        self.track_device_service = track_device_service
        self.mqtt_provider = mqtt_provider
        self.conversation_history: list[dict[str, str]] = []

    def _call_ollama(self, prompt: str, model: str = "llama2") -> str:
        try:
            resultado = subprocess.run(
                ["ollama", "run", model, prompt],
                capture_output=True,
                text=True,
                timeout=30,
            )
            return resultado.stdout.strip()
        except subprocess.TimeoutExpired:
            return "Error: Ollama tardó demasiado en responder"
        except FileNotFoundError:
            return "Error: Ollama no está instalado o no está en el PATH"

    def _get_device_states_summary(self, user_id: int) -> str:
        try:
            devices = self.installed_device_service.get_all_with_device(user_id)
            if not devices:
                return "No hay dispositivos instalados."

            summary_lines = []
            device_type_count = {}

            for device in devices:
                device_type = device.device.type.value
                device_type_count[device_type] = (
                    device_type_count.get(device_type, 0) + 1
                )

                try:
                    if device.id is None:
                        raise Exception("Id device not started")
                    state = self.state_device_service.execute(user_id, device.id)
                    summary_lines.append(
                        f"- {device.name} ({device_type}): {state.model_dump()}"
                    )
                except Exception:
                    summary_lines.append(
                        f"- {device.name} ({device_type}): estado desconocido"
                    )

            summary = "Dispositivos instalados:\n" + "\n".join(summary_lines)
            summary += f"\n\nResumen: {device_type_count}"
            return summary
        except Exception as e:
            return f"Error obteniendo dispositivos: {str(e)}"

    def _analyze_intent(self, user_message: str, user_id: int) -> dict[str, Any]:
        device_states_summary = self._get_device_states_summary(user_id)

        prompt = f"""Eres un asistente inteligente para una casa con dispositivos IoT.
Analiza la siguiente pregunta/orden del usuario y responde SOLO con un JSON válido.

INFORMACIÓN DE DISPOSITIVOS:
{device_states_summary}

PREGUNTAS/ÓRDENES DEL USUARIO:
{user_message}

Responde con exactamente este JSON (sin explicaciones adicionales):
{{
    "intent": "query" si es una pregunta, "command" si es una orden,
    "device_types": ["light", "door", "camera", "movement", "temperature"] mencionados (puede haber múltiples),
    "action": "on" si quiere encender, "off" si quiere apagar, null si no aplica,
    "attribute": "brightness", "temperature", etc. o null,
    "value": número si especifica un valor, o null,
    "description": "traducción clara de lo que el usuario pide"
}}"""

        response = self._call_ollama(prompt)

        try:
            if "{" in response and "}" in response:
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                return json.loads(response)
        except json.JSONDecodeError:
            return {
                "intent": "unknown",
                "device_types": [],
                "action": None,
                "description": f"No pude entender: {response[:200]}",
            }

    def _find_devices_by_type(
        self, user_id: int, device_types: list[str]
    ) -> list[InstalledDeviceWithDevice]:
        all_devices = self.installed_device_service.get_all_with_device(user_id)
        matching = []

        for device in all_devices:
            device_type_value = device.device.type.value
            if device_type_value in device_types:
                matching.append(device)

        return matching

    def _execute_command_on_device(
        self, device: InstalledDeviceWithDevice, action: str, user_id: int
    ) -> bool:
        try:
            command_data: Any = None

            if not (action == "on" or action == "off"):
                raise
            match device.device.type:
                case DeviceType.LIGHT:
                    command_data = Light(action=action)
                case DeviceType.DOOR:
                    command_data = Door(action=action)
                case DeviceType.CAMERA:
                    command_data = Camera(action=action)
                case DeviceType.MOVEMENT:
                    command_data = MovementSensor(action=action)
                case DeviceType.THERMOSTAT:
                    command_data = TemperatureSensor(
                        action=action,
                        enable_auto=False,
                        has_limit=25,
                    )
                case _:
                    return False

            if command_data is None:
                return False

            topic = f"/{device.device.device_uuid}/action"
            self.mqtt_provider.publish(topic, command_data.model_dump())

            if device.id is None:
                return False

            status = StatusDevice.ON if action == "on" else StatusDevice.OFF
            track = TrackDevice(
                device_id=device.id,
                status=status,
                timestamp=utcnow(),
            )
            self.track_device_service.create_track_device(track)

            return True
        except Exception as e:
            print(f"Error ejecutando comando: {e}")
            return False

    def _generate_response(self, intent_analysis: dict[str, Any], user_id: int) -> str:
        intent = intent_analysis.get("intent")
        device_types = intent_analysis.get("device_types", [])
        action = intent_analysis.get("action")
        description = intent_analysis.get("description", "Tu solicitud")

        if intent == "query":
            devices = self._find_devices_by_type(user_id, device_types)

            if not devices:
                return f"No encontré dispositivos de tipo {', '.join(device_types)}"

            response_lines = [f"Respecto a tu pregunta: {description}\n"]

            for device in devices:
                try:
                    if device.id is None:
                        raise Exception("Device id not started")
                    state = self.state_device_service.execute(user_id, device.id)
                    state_dict = state.model_dump()
                    response_lines.append(
                        f"• {device.name}: {json.dumps(state_dict, ensure_ascii=False)}"
                    )
                except Exception as e:
                    response_lines.append(
                        f"• {device.name}: no pude obtener el estado ({e})"
                    )

            return "\n".join(response_lines)

        elif intent == "command":
            if not action:
                return f"No entendí qué acción ejecutar. {description}"

            devices = self._find_devices_by_type(user_id, device_types)

            if not devices:
                return f"No encontré dispositivos de tipo {', '.join(device_types)} para controlar"

            successfully_executed = []
            failed = []

            for device in devices:
                if self._execute_command_on_device(device, action, user_id):
                    successfully_executed.append(device.name)
                else:
                    failed.append(device.name)

            response_parts = []
            if successfully_executed:
                action_desc = "encendido" if action == "on" else "apagado"
                response_parts.append(
                    f"✓ He {action_desc} correctamente: {', '.join(successfully_executed)}"
                )

            if failed:
                response_parts.append(f"✗ No pude controlar: {', '.join(failed)}")

            return (
                "\n".join(response_parts)
                if response_parts
                else "No se ejecutó ninguna acción"
            )

        else:
            return f"No entendí tu solicitud: {description}"

    def process_message(self, user_message: str, user_id: int) -> str:
        self.conversation_history.append({"role": "user", "content": user_message})
        intent_analysis = self._analyze_intent(user_message, user_id)
        response = self._generate_response(intent_analysis, user_id)
        self.conversation_history.append({"role": "assistant", "content": response})
        return response

    def get_conversation_history(self) -> list[dict[str, str]]:
        return self.conversation_history.copy()

    def clear_history(self) -> None:
        self.conversation_history = []
