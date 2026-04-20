from sqlalchemy import Connection, delete, insert, select, update
from sqlalchemy.exc import IntegrityError

from app.entities.house import HouseEntity, HouseWithAreas
from app.exceptions.database_exceptions import DatabaseConstraintException
from app.exceptions.house_exception import HouseIdNotStarted, HouseNotFoundByIdError
from app.infraestructure.models import areas, houses
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

    def get_all(
        self, filters: FilterGetAllHouse | None = None
    ) -> list[HouseEntity] | list[HouseWithAreas]:
        if filters is not None and filters.include_areas:
            # Join with areas
            query = select(
                houses.c.id,
                houses.c.name,
                houses.c.user_id,
                houses.c.location,
                houses.c.invitation_validation,
                areas.c.id.label("area_id"),
                areas.c.name.label("area_name"),
                areas.c.type.label("area_type"),
                areas.c.house_id.label("area_house_id"),
            ).select_from(houses.outerjoin(areas, houses.c.id == areas.c.house_id))

            if filters.user_id is not None:
                query = query.where(houses.c.user_id == filters.user_id)

            result = self.conn.execute(query)
            rows = result.mappings().all()

            # Group by house
            houses_dict = {}
            for row in rows:
                house_id = row["id"]
                if house_id not in houses_dict:
                    houses_dict[house_id] = {
                        "id": row["id"],
                        "name": row["name"],
                        "user_id": row["user_id"],
                        "location": row["location"],
                        "invitation_validation": row["invitation_validation"],
                        "areas": [],
                    }
                if row["area_id"] is not None:
                    houses_dict[house_id]["areas"].append(
                        {
                            "id": row["area_id"],
                            "name": row["area_name"],
                            "type": row["area_type"],
                            "house_id": row["area_house_id"],
                        }
                    )

            return [HouseWithAreas(**house_data) for house_data in houses_dict.values()]
        else:
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
