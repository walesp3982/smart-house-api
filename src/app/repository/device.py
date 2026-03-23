from sqlalchemy import Connection, insert
from sqlalchemy.exc import IntegrityError

from app.entities import DeviceEntity
from app.exceptions.database_exceptions import DatabaseConstraintException
from app.models import devices_user


class DeviceRepository:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    def get_by_id(self, id: int) -> None | DeviceEntity:
        query = devices_user.select().where(devices_user.c.id == id)

        result = self.conn.execute(query).fetchone()

        if result:
            return DeviceEntity(
                id=result.id,
                device_uuid=result.device_uuid,
                activation_code=result.activation_code,
                type=result.type,
            )

        return None

    def create(self, device_data: DeviceEntity) -> int:
        data = device_data.model_dump()
        data.pop("id")
        query = insert(devices_user).values(data)

        try:
            result = self.conn.execute(query)
            return result.lastrowid
        except IntegrityError as e:
            raise DatabaseConstraintException(str(e.orig))
        pass
