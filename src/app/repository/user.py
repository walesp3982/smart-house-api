from sqlalchemy import Engine, insert, select

from app.dto import UserDTO
from app.entities import User
from app.models import users


class UserRepository:
    """Repository for user operations."""

    def __init__(self, engine: Engine):
        self.engine = engine

    # Todo: Implementar filtros si es necesario
    def getAll(self, **filters) -> list[User]:
        with self.engine.connect() as connection:
            query = select(users)
            result = connection.execute(query)
            return [
                User(id=row.id, name=row.name, email=row.email, password=row.password)
                for row in result.fetchall()
            ]

    def getById(self, user_id: int) -> User | None:
        with self.engine.connect() as connection:
            query = select(users).where(users.c.id == user_id)
            result = connection.execute(query).fetchone()
            if result:
                return User(
                    id=result.id,
                    name=result.name,
                    email=result.email,
                    password=result.password,
                )
            return None

    def getByEmail(self, email: str) -> User | None:
        with self.engine.connect() as connection:
            query = select(users).where(users.c.email == email)
            result = connection.execute(query).fetchone()
            if result:
                return User(
                    id=result.id,
                    name=result.name,
                    email=result.email,
                    password=result.password,
                )
            return None

    def update(self, user: User) -> None:
        with self.engine.connect() as connection:
            query = (
                users.update()
                .where(users.c.id == user.id)
                .values(name=user.name, email=user.email, password=user.password)
            )
            connection.execute(query)
            connection.commit()

    def delete(self, user_id: int) -> None:
        with self.engine.connect() as connection:
            query = users.delete().where(users.c.id == user_id)
            connection.execute(query)
            connection.commit()

    def create(self, user: UserDTO) -> int:
        with self.engine.connect() as connection:
            query = (
                insert(users)
                .values(name=user.name, email=user.email, password=user.password)
                .returning(users.c.id)
            )
            result = connection.execute(query)
            connection.commit()
            return result.scalar_one()
