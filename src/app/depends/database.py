from typing import Annotated, Any, Generator

from fastapi import Depends, HTTPException
from sqlalchemy import Connection

from app.models import engine
from app.repository import UserRepository


def get_connection() -> Generator[Connection, Any, Any]:
    with engine.begin() as conn:
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
