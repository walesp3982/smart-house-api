from sqlalchemy import Connection, delete, insert, select, update
from sqlalchemy.exc import IntegrityError

from app.entities.house import HouseEntity
from app.exceptions.database_exceptions import DatabaseConstraintException
from app.exceptions.house_exception import HouseIdNotStarted, HouseNotFoundByIdError
from app.infraestructure.models import houses
from app.repository.interfaces import FilterGetAllHouse


class HouseRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def create(self, data: HouseEntity) -> int:
        query = insert(houses).values(data.model_dump(exclude={"id"}))

        try:
            result = self.conn.execute(query)
            return result.lastrowid

        except IntegrityError as e:
            raise DatabaseConstraintException(str(e.orig))

    def get_all(self, filters: FilterGetAllHouse | None = None) -> list[HouseEntity]:
        query = select(houses)

        if filters is not None:
            if filters.user_id is not None:
                query = query.where(houses.c.user_id == filters.user_id)

        result = self.conn.execute(query)

        return [HouseEntity(**row) for row in result.mappings().all()]

    def get_by_id(self, house_id: int) -> HouseEntity | None:
        query = select(houses).where(houses.c.id == house_id)

        result = self.conn.execute(query).mappings().one_or_none()

        return HouseEntity(**result) if result is not None else None

    def update(self, data: HouseEntity) -> None:
        if data.id is None:
            raise HouseIdNotStarted()
        query = (
            update(houses)
            .where(houses.c.id == data.id)
            .values(data.model_dump(exclude={"id"}))
        )
        result = self.conn.execute(query)
        if result.rowcount == 0:
            raise HouseNotFoundByIdError(data.id)

    def delete(self, house_id: int) -> None:
        query = delete(houses).where(houses.c.id == house_id)

        result = self.conn.execute(query)
        if result.rowcount == 0:
            raise HouseNotFoundByIdError(house_id)
