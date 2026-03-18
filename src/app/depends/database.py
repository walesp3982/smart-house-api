from typing import Annotated, Any, Generator

from fastapi import Depends
from sqlalchemy import Connection

from app.models import engine
from app.repository import UserRepository


def get_connection() -> Generator[Connection, Any, Any]:
    with engine.begin() as conn:
        yield conn


ConnectionDep = Annotated[Connection, Depends(get_connection)]


def get_user_repository(
    connection: ConnectionDep,
) -> UserRepository:
    return UserRepository(connection)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
