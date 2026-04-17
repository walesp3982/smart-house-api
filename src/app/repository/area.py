from typing import Optional

from sqlalchemy import Connection, delete, insert, select, update
from sqlalchemy.exc import IntegrityError

from app.entities import AreaEntity
from app.exceptions.areas_exceptions import (
    AreaEntityIdNotStartedError,
    AreaNotFoundByIdError,
)
from app.exceptions.database_exceptions import DatabaseConstraintException
from app.infraestructure.models import areas
from app.repository.interfaces.area import FilterAreas


class AreaRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def create(self, data: AreaEntity) -> int:
        query = insert(areas).values(**data.model_dump(exclude={"id"}))
        try:
            result = self.conn.execute(query)
            return result.lastrowid
        except IntegrityError as e:
            raise DatabaseConstraintException(str(e.orig))

    def get_by_id(self, id: int) -> AreaEntity | None:
        query = select(areas).where(areas.c.id == id)

        result = self.conn.execute(query).mappings().one_or_none()

        return AreaEntity(**result) if result is not None else None

    def get_all(self, filters: Optional[FilterAreas] = None) -> list[AreaEntity]:
        query = select(areas)

        if filters is not None:
            if filters.house_id is not None:
                query = query.where(areas.c.house_id == filters.house_id)
            if filters.name is not None:
                query = query.where(areas.c.name.ilike(f"%{filters.name}%"))

        result = self.conn.execute(query).mappings().all()

        return [AreaEntity(**row) for row in result]

    def update(self, data: AreaEntity) -> None:
        if data.id is None:
            raise AreaEntityIdNotStartedError()

        query = update(areas).values(**data.model_dump(exclude={"id"})).where(areas.c.id == data.id)

        try:
            result = self.conn.execute(query)
            if result.rowcount == 0:
                raise AreaNotFoundByIdError(data.id)
        except IntegrityError as err:
            raise DatabaseConstraintException(str(err.orig))

    def delete(self, id: int) -> None:
        query = delete(areas).where(areas.c.id == id)

        result = self.conn.execute(query)

        if result.rowcount == 0:
            raise AreaNotFoundByIdError(id)
