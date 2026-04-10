from typing import Optional


class DeviceNotFoundError(Exception):
    def __init__(self, error: Optional[str]) -> None:
        if error is None:
            text = "No se encontró el dispositivo"
        else:
            text = error
        return super().__init__(text)


class DeviceNotFoundByIdError(DeviceNotFoundError):
    def __init__(self, id) -> None:
        super().__init__(f"No se encontró el dispositivo con id {id}")


class DeviceDuplicateUUIDError(Exception):
    def __init__(self):
        super().__init__("Device ya encontrado en la DB")


class ActionDeviceNotFound(Exception):
    def __init__(self):
        super().__init__("La action para el dispositivo no fue encontrado")
