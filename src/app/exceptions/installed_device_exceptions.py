class InstalledDeviceException(Exception):
    """Base exception for InstalledDevice errors"""

    pass


class InstalledDeviceNotFoundByIdError(InstalledDeviceException):
    """Exception raised when an installed device is not found by id"""

    def __init__(self, id: int):
        self.id = id
        super().__init__(f"Dispositivo con {id} not encontrado")


class InstalledDeviceEntityIdNotStartedError(InstalledDeviceException):
    """Exception raised when trying to update an installed device without an id"""

    def __init__(self):
        super().__init__("Id del dispositivo no fue inicializado")


class InstalledDeviceAlreadyRegisteredError(InstalledDeviceException):
    """Exception raised when trying to register a device already registered by
    another user"""

    def __init__(self, uuid: str):
        self.uuid = uuid
        super().__init__(f"El dispositivo con uuid {uuid} ya fue registrado por otro usuario")


class InstalledDeviceVerificationError(InstalledDeviceException):
    """Exception raised when verification code is invalid"""

    def __init__(self):
        super().__init__("Código de verificación inválido")


class InstalledDeviceUnauthorizedError(InstalledDeviceException):
    """Exception raised when user is not the owner of the installed device"""

    def __init__(self, installed_device_id: int):
        self.id = installed_device_id
        super().__init__(
            "No tienes permiso para manejar este dispositivo" + f"con id {installed_device_id}"
        )
