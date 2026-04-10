from app.entities.track_device import TrackDevice
from app.repository.interfaces.track_device import (
    FilterTrackDevices,
    TrackDeviceRepositoryProtocol,
)


class TrackDeviceService:
    def __init__(self, track_device_repository: TrackDeviceRepositoryProtocol) -> None:
        self.repository = track_device_repository

    def create_track_device(self, data: TrackDevice) -> int:
        """Crea un registro de seguimiento de un dispositivo."""
        return self.repository.create(data)

    def get_by_device_id(self, device_id: int, user_id: int) -> list[TrackDevice]:
        """Obtiene el historial de seguimiento de un dispositivo para el usuario."""
        filters = FilterTrackDevices(device_id=device_id, user_id=user_id)
        return self.repository.get_all(filters)

    def get_by_house_id(self, house_id: int, user_id: int) -> list[TrackDevice]:
        """Obtiene el historial de seguimiento de los dispositivos de una casa."""
        filters = FilterTrackDevices(house_id=house_id, user_id=user_id)
        return self.repository.get_all(filters)

    def get_by_user_id(self, user_id: int) -> list[TrackDevice]:
        """Obtiene el historial de seguimiento de todos los dispositivos del usuario."""
        filters = FilterTrackDevices(user_id=user_id)
        return self.repository.get_all(filters)
