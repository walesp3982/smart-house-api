class InstalledDeviceException(Exception):
    """Base exception for InstalledDevice errors"""

    pass


class InstalledDeviceNotFoundByIdError(InstalledDeviceException):
    """Exception raised when an installed device is not found by id"""

    def __init__(self, id: int):
        self.id = id
        super().__init__(f"Installed device with id {id} not found")


class InstalledDeviceEntityIdNotStartedError(InstalledDeviceException):
    """Exception raised when trying to update an installed device without an id"""

    def __init__(self):
        super().__init__("Installed device entity id not started")
