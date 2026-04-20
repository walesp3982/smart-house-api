from typing import Generator, Literal

from pydantic import BaseModel

from app.entities.installed_device import InstalledDeviceWithDevice
from app.entities.track_device import StatusDevice, TrackDevice
from app.infraestructure.llm.llm_provider import LLMFactoryProvider
from app.infraestructure.mqtt.provider import MQTTProvider
from app.services.installed_device import InstalledDeviceService
from app.services.track_device import TrackDeviceService
from app.settings.time import utcnow

"""
Creación del request que tiene que devolver el orquestador
"""


class OrquestatorResponse(BaseModel):
    mode: Literal["order", "query"]


SYSTEM_MESSAGE_ORQUESTADOR = """
Eres un asistente inteligente para una casa con dispositivos IoT.
Analiza la siguiente del usuario y responde a si es orden(order)
o consulta(query) con un JSON válido.
"""

"""
Desde aquí es todo respecto a order send
"""


class OrderDevice(BaseModel):
    id: int
    action: Literal["on", "off"]
    valid_action: bool


class ListOrderDevice(BaseModel):
    devices: list[OrderDevice]


SYSTEM_MESSAGE_ORDER_SEND = """
Eres un asistente inteligente para una casa con dispositivos Iot,
Necesito que respondas un usuario para decirle que se va a ejecutar
el comando con un tono formal y caballezco
"""

SYSTEM_MESSAGE_JSON_ORDER = """
Eres un asistente inteligente para una casa con dispositivos Iot
Necesito que resposne al mensaje del usuario con un json
válido compuesto por un listado de id y la
action correspondiente "on" | "off" del listado de json que
se te va a obtener analizando el chat del usuario
pueden ser acciones para un o varios dispositivos
si el comando no corresponde a los estipulado no lo agregues al json
"""

SYSTEM_MESSAGE_ORDER_FAILED = """
Eres el asistente inteligente para una casa con dispsitivos Iot
Necesito que a partir del mensaje que mande el usuario le notifiques
que no pudiste cumplir con la petición
"""

SYSTEM_MESSAGE_ORDER_SUCCESS = """
Eres un asistente inteligente para una casa con dispositivos Iot
Necesito que a partir del mensaje que mande al usuario se le notifique
que se pudo cumplir con las ordenes, te voy a pasar un json con los
dispositivos modificados para que indagues si existe un dispositivo
que no puedo ser encontrado
"""


def generate_user_success(order_device: str, user_message: str):
    return f"""
DISPOSITIVOS QUE CAMBIARON DE ESTADO:
{order_device}
MENSAJE DEL USUARIO:
{user_message}
"""


def generate_user_order(installed_devices: str, user_message: str):
    return f"""
DISPOSITIVOS DEL USUARIO:
{installed_devices}
MENSAJE DEL USUARIO:
{user_message}
"""


"""
ESTO ES PARA EL MODO CONSULTA
"""
SYSTEM_MESSAGE_QUERY = """
Eres un asistente inteligente para una casa con dispositivos IoT.
El usuario va consultar el resultado de ciertos dispositivos
por lo que vas a analizar la información de dispositivo que
se te va a proporcionar
"""


def get_prompt(device_states_summary: str, user_message: str):
    prompt = f"""

INFORMACIÓN DE DISPOSITIVOS:
{device_states_summary}

PREGUNTAS/ÓRDENES DEL USUARIO:
{user_message}

"""

    return prompt


class ChatConversationService:
    def __init__(
        self,
        installed_device_service: InstalledDeviceService,
        track_device_service: TrackDeviceService,
        mqtt_provider: MQTTProvider,
    ):
        self.installed_device_service = installed_device_service
        self.mqtt_provider = mqtt_provider
        self.track_device_service = track_device_service
        self.json_chat = LLMFactoryProvider.get_provider("gemini")
        self.stream_chat = LLMFactoryProvider.get_provider("groq")

    def chat(self, user_message: str, user_id: int) -> Generator[str, None, None]:
        response = self.json_chat.structured_chat(
            system_message=SYSTEM_MESSAGE_ORQUESTADOR,
            user_message=user_message,
            size_response="MEDIUM",
            creativity="LOW",
            schema=OrquestatorResponse,
        )

        match response.mode:
            case "order":
                for response in self.mode_order_chat(user_message, user_id):
                    yield response
            case "query":
                for response in self.mode_query_chat(user_message, user_id):
                    yield response

    def mode_order_chat(self, user_message: str, user_id) -> Generator[str, None, None]:
        """
        Aquí se trabaja con la lógica de que el mensaje del usuario se
        considere como orden
        """
        # Mandamos un mensaje al usuario para confirmar que se va
        # ejecutar el comando
        for response_send in self.stream_chat.stream_chat(
            system_message=SYSTEM_MESSAGE_ORDER_SEND,
            user_message=user_message,
            creativity="MEDIUM",
            size_response="MEDIUM",
        ):
            yield response_send
        yield "\n"

        # Obtenemos los dispositivos actuales del usuario
        installed_devices = self.installed_device_service.get_all_with_device(user_id)
        str_installed_devices: str = "\n".join(
            [device.model_dump_json() for device in installed_devices]
        )
        response = self.json_chat.structured_chat(
            system_message=SYSTEM_MESSAGE_JSON_ORDER,
            user_message=generate_user_order(str_installed_devices, user_message=user_message),
            creativity="LOW",
            size_response="MEDIUM",
            schema=ListOrderDevice,
        )

        if len(response.devices) == 0:
            for chunk in self.stream_chat.stream_chat(
                system_message=SYSTEM_MESSAGE_ORDER_FAILED,
                user_message=user_message,
                creativity="MEDIUM",
                size_response="MEDIUM",
            ):
                yield chunk
            return

        publish_installed_devices = self.execute_orders(response, installed_devices)
        str_pub_isntalled_devices = "\n".join(
            [device.model_dump_json() for device in publish_installed_devices]
        )
        for chunk in self.stream_chat.stream_chat(
            system_message=SYSTEM_MESSAGE_ORDER_SUCCESS,
            user_message=generate_user_success(str_pub_isntalled_devices, user_message),
            creativity="MEDIUM",
            size_response="MEDIUM",
        ):
            yield chunk

    def execute_orders(
        self, orders: ListOrderDevice, installed_devices: list[InstalledDeviceWithDevice]
    ) -> list[InstalledDeviceWithDevice]:
        # Obtenemos los id de los dispositivos
        id_installed_devices: list[int] = [device.id for device in orders.devices]

        # Obtenemos los installed_devices a ejecutar comandos
        order_installed_devices = [
            device for device in installed_devices if device in id_installed_devices
        ]

        for device in order_installed_devices:
            # obtenemos el nuevo estado según la order
            device_order = [device for device in orders.devices if device == device.id][0]
            self.publish_set_device(device, device_order.action)

            match device_order.action:
                case "off":
                    status = StatusDevice.OFF
                case "on":
                    status = StatusDevice.ON
            device_id = device.id
            if device_id is None:
                break
            self.track_device_service.create_track_device(
                TrackDevice(device_id=device_id, status=status, timestamp=utcnow())
            )
        return order_installed_devices

    def publish_set_device(self, device: InstalledDeviceWithDevice, state: Literal["on", "off"]):
        topic = f"/{device.device.device_uuid}/set"

        self.mqtt_provider.publish(topic=topic, payload={"state": state})

    def _state_device(self, device: InstalledDeviceWithDevice):
        topic = f"/{device.device.device_uuid}/value"
        state = self.mqtt_provider.get_topic(topic)
        return state

    def mode_query_chat(self, user_message: str, user_id) -> Generator[str, None, None]:
        devices_state = self._get_device_states_summary(user_id)

        for chunk in self.stream_chat.stream_chat(
            system_message=SYSTEM_MESSAGE_QUERY,
            user_message=get_prompt(device_states_summary=devices_state, user_message=user_message),
            creativity="MEDIUM",
            size_response="MEDIUM",
        ):
            yield chunk

    def _get_device_states_summary(self, user_id: int) -> str:
        try:
            devices = self.installed_device_service.get_all_with_device(user_id)
            if not devices:
                return "No hay dispositivos instalados."

            summary_lines = []
            device_type_count = {}

            for device in devices:
                device_type = device.device.type.value
                device_type_count[device_type] = device_type_count.get(device_type, 0) + 1

                try:
                    if device.id is None:
                        raise Exception("Id device not started")
                    state = self._state_device(device)
                    summary_lines.append(
                        f"- {device.name} ({device_type}): {state if state is not None else 'estado desconocido'}"
                    )
                except Exception:
                    summary_lines.append(f"- {device.name} ({device_type}): estado desconocido")

            summary = "Dispositivos instalados:\n" + "\n".join(summary_lines)
            summary += f"\n\nResumen: {device_type_count}"
            return summary
        except Exception as e:
            return f"Error obteniendo dispositivos: {str(e)}"
