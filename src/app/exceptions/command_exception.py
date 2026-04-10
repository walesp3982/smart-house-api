class IncorrectRequestCommandError(Exception):
    def __init__(self):
        super().__init__("El dispositivo no acepta los comandos correspondiente")


class StateNotFoundDeviceError(Exception):
    def __init__(self) -> None:
        super().__init__("No se encontró el estado actual del dispositivo")
