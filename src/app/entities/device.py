import copy
from dataclasses import dataclass
from enum import StrEnum

from pydantic import BaseModel


@dataclass
class Action:
    """
    Es una representación de una action del device
    en el MQTT broker
    """

    naming_broker: str
    actions: list[str]


ON_ACTION = Action(
    "on",
    ["prender", "prende", "encender", "enciende", "activar", "activa"],
)

OFF_ACTION = Action(
    "off",
    ["apaga", "apagar", "desactivar", "desactiva"],
)

VALUE_ACTION = Action(
    "value",
    ["valor", "estado"],
)


class DeviceType(StrEnum):
    LIGHT = "light"
    THERMOSTAT = "thermostat"
    CAMERA = "camera"
    LOCK = "lock"
    SENSOR = "sensor"

    def command(self) -> list[Action]:
        """
        Va a dar los comandos validos en spanish
        que puede realizar el device
        """
        match self:
            case self.LIGHT:
                return [
                    ON_ACTION,
                    OFF_ACTION,
                ]
            case self.THERMOSTAT:
                own_value_action = copy.deepcopy(VALUE_ACTION)
                own_value_action.actions.append("temperature")
                return [
                    ON_ACTION,
                    OFF_ACTION,
                    own_value_action,
                ]
            case self.CAMERA:
                return [
                    ON_ACTION,
                    OFF_ACTION,
                ]
            case self.LOCK:
                own_off_action = copy.deepcopy(OFF_ACTION)
                own_off_action.actions.append("cerrar")
                own_off_action.actions.append("cierra")
                own_on_action = copy.deepcopy(ON_ACTION)
                own_on_action.actions.append("abrir")
                own_on_action.actions.append("abre")
                return [
                    own_off_action,
                    own_on_action,
                ]
            case self.SENSOR:
                return [
                    ON_ACTION,
                    OFF_ACTION,
                ]


class DeviceEntity(BaseModel):
    id: None | int = None
    device_uuid: str
    activation_code: str
    type: DeviceType
