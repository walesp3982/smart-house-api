from typing import Annotated, Any, Generator

from fastapi import Depends, HTTPException
from sqlalchemy import Connection

from app.database import get_engine
from app.repository import DeviceRepository, UserRepository


def get_connection() -> Generator[Connection, Any, Any]:
    with get_engine().begin() as conn:
        try:
            yield conn
        except HTTPException:
            raise
        # Solo hace rollback en error inesperados 505
        except Exception:
            conn.rollback()
            raise


ConnectionDep = Annotated[Connection, Depends(get_connection)]


def get_user_repository(
    connection: ConnectionDep,
) -> UserRepository:
    return UserRepository(connection)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


def get_device_repository(connection: ConnectionDep) -> DeviceRepository:
    return DeviceRepository(connection)


DeviceRepositoryDep = Annotated[DeviceRepository, Depends(get_device_repository)]
