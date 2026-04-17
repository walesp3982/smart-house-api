from typing import Optional

from sqlalchemy import Connection, delete, insert, join, select, update
from sqlalchemy.exc import IntegrityError

from app.entities.track_device import TrackDevice
from app.exceptions.database_exceptions import DatabaseConstraintException
from app.exceptions.track_device_exceptions import (
    TrackDeviceEntityIdNotStartedError,
    TrackDeviceNotFoundByIdError,
)
from app.infraestructure.models import installed_devices, track_devices
from app.repository.interfaces.track_device import FilterTrackDevices


class TrackDeviceRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def create(self, data: TrackDevice) -> int:
        query = insert(track_devices).values(**data.model_dump(exclude={"id"}))
        try:
            result = self.conn.execute(query)
            return result.lastrowid
        except IntegrityError as e:
            raise DatabaseConstraintException(str(e.orig))

    def get_by_id(self, id: int) -> TrackDevice | None:
        query = select(track_devices).where(track_devices.c.id == id)

        result = self.conn.execute(query).mappings().one_or_none()

        return TrackDevice(**result) if result is not None else None

    def get_all(self, filters: Optional[FilterTrackDevices] = None) -> list[TrackDevice]:
        query = select(track_devices)

        if filters is not None:
            if filters.house_id is not None or filters.user_id is not None:
                query = query.select_from(
                    join(
                        track_devices,
                        installed_devices,
                        track_devices.c.device_id == installed_devices.c.id,
                    )
                )

            if filters.device_id is not None:
                query = query.where(track_devices.c.device_id == filters.device_id)
            if filters.status is not None:
                query = query.where(track_devices.c.status == filters.status)
            if filters.house_id is not None:
                query = query.where(installed_devices.c.house_id == filters.house_id)
            if filters.user_id is not None:
                query = query.where(installed_devices.c.user_id == filters.user_id)

        result = self.conn.execute(query).mappings().all()

        return [TrackDevice(**row) for row in result]

    def update(self, data: TrackDevice) -> None:
        if data.id is None:
            raise TrackDeviceEntityIdNotStartedError()

        query = (
            update(track_devices)
            .values(**data.model_dump(exclude={"id"}))
            .where(track_devices.c.id == data.id)
        )

        try:
            result = self.conn.execute(query)
            if result.rowcount == 0:
                raise TrackDeviceNotFoundByIdError(data.id)
        except IntegrityError as err:
            raise DatabaseConstraintException(str(err.orig))

    def delete(self, id: int) -> None:
        query = delete(track_devices).where(track_devices.c.id == id)

        result = self.conn.execute(query)

        if result.rowcount == 0:
            raise TrackDeviceNotFoundByIdError(id)
