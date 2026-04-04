from typing import Optional

from sqlalchemy import Connection, delete, insert, join, select, update
from sqlalchemy.exc import IntegrityError

from app.entities.device import DeviceEntity
from app.entities.installed_device import (
    InstalledDeviceEntity,
    InstalledDeviceWithDevice,
)
from app.exceptions.database_exceptions import DatabaseConstraintException
from app.exceptions.installed_device_exceptions import (
    InstalledDeviceEntityIdNotStartedError,
    InstalledDeviceNotFoundByIdError,
)
from app.infraestructure.models import devices, installed_devices
from app.repository.interfaces.installed_device import FilterInstalledDevices


class InstalledDeviceRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def create(self, data: InstalledDeviceEntity) -> int:
        query = insert(installed_devices).values(**data.model_dump(exclude={"id"}))
        try:
            result = self.conn.execute(query)
            return result.lastrowid
        except IntegrityError as e:
            raise DatabaseConstraintException(str(e.orig))

    def get_by_id(self, id: int) -> InstalledDeviceEntity | None:
        query = select(installed_devices).where(installed_devices.c.id == id)

        result = self.conn.execute(query).mappings().one_or_none()

        return InstalledDeviceEntity(**result) if result is not None else None

    def get_all(
        self, filters: Optional[FilterInstalledDevices] = None
    ) -> list[InstalledDeviceEntity]:
        query = select(installed_devices)

        if filters is not None:
            if filters.house_id is not None:
                query = query.where(installed_devices.c.house_id == filters.house_id)
            if filters.area_id is not None:
                query = query.where(installed_devices.c.area_id == filters.area_id)
            if filters.user_id is not None:
                query = query.where(installed_devices.c.user_id == filters.user_id)
            if filters.name is not None:
                query = query.where(installed_devices.c.name.ilike(f"%{filters.name}%"))

        result = self.conn.execute(query).mappings().all()

        return [InstalledDeviceEntity(**row) for row in result]

    def update(self, data: InstalledDeviceEntity) -> None:
        if data.id is None:
            raise InstalledDeviceEntityIdNotStartedError()

        query = (
            update(installed_devices)
            .values(**data.model_dump(exclude={"id"}))
            .where(installed_devices.c.id == data.id)
        )

        try:
            result = self.conn.execute(query)
            if result.rowcount == 0:
                raise InstalledDeviceNotFoundByIdError(data.id)
        except IntegrityError as err:
            raise DatabaseConstraintException(str(err.orig))

    def delete(self, id: int) -> None:
        query = delete(installed_devices).where(installed_devices.c.id == id)

        result = self.conn.execute(query)

        if result.rowcount == 0:
            raise InstalledDeviceNotFoundByIdError(id)

    def get_with_device(self, id: int) -> InstalledDeviceWithDevice | None:
        """Obtiene un installed_device con su información de device asociada."""
        query = (
            select(installed_devices, devices)
            .select_from(
                join(
                    installed_devices,
                    devices,
                    installed_devices.c.device_id == devices.c.id,
                )
            )
            .where(installed_devices.c.id == id)
        )

        result = self.conn.execute(query).mappings().one_or_none()

        if result is None:
            return None

        installed_device_data = {
            "id": result.id,
            "name": result.name,
            "device_id": result.device_id,
            "house_id": result.house_id,
            "area_id": result.area_id,
            "user_id": result.user_id,
        }

        device_data = {
            "id": result.id_1,
            "device_uuid": result.device_uuid,
            "activation_code": result.activation_code,
            "type": result.type,
        }

        device = DeviceEntity(**device_data)
        return InstalledDeviceWithDevice(**installed_device_data, device=device)

    def get_by_uuid(self, uuid: str) -> InstalledDeviceEntity | None:
        """Obtiene un installed_device por el uuid del device."""
        query = (
            select(installed_devices)
            .select_from(
                join(
                    installed_devices,
                    devices,
                    installed_devices.c.device_id == devices.c.id,
                )
            )
            .where(devices.c.device_uuid == uuid)
        )

        result = self.conn.execute(query).mappings().one_or_none()

        return InstalledDeviceEntity(**result) if result is not None else None

    def get_all_by_user_id(self, user_id: int) -> list[InstalledDeviceEntity]:
        """Obtiene todos los installed_devices de un usuario específico."""
        filters = FilterInstalledDevices(user_id=user_id)
        return self.get_all(filters)
