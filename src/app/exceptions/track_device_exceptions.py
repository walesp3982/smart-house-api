class TrackDeviceException(Exception):
    """Base exception for TrackDevice errors"""

    pass


class TrackDeviceNotFoundByIdError(TrackDeviceException):
    """Exception raised when a track device is not found by id"""

    def __init__(self, id: int):
        self.id = id
        super().__init__(f"Track device with id {id} not found")


class TrackDeviceEntityIdNotStartedError(TrackDeviceException):
    """Exception raised when trying to update a track device without an id"""

    def __init__(self):
        super().__init__("Track device entity id not started")
