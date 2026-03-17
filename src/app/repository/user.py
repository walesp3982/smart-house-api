from sqlalchemy import Connection, insert, select
from sqlalchemy.exc import IntegrityError

from app.dto import UserDTO
from app.entities import User
from app.exceptions import DatabaseConstraintException, UserNotFoundException
from app.models import users


class UserRepository:
    """Repository for user operations."""

    def __init__(self, connection: Connection):
        self.connection = connection

    # Todo: Implementar filtros si es necesario
    def get_all(self, **filters) -> list[User]:
        query = select(users)
        result = self.connection.execute(query)
        return [
            User(id=row.id, name=row.name, email=row.email, password=row.password)
            for row in result.fetchall()
        ]

    def get_by_id(self, user_id: int) -> User | None:
        query = select(users).where(users.c.id == user_id)
        result = self.connection.execute(query).fetchone()
        if result:
            return User(
                id=result.id,
                name=result.name,
                email=result.email,
                password=result.password,
            )
        return None

    def get_by_email(self, email: str) -> User | None:
        query = select(users).where(users.c.email == email)
        result = self.connection.execute(query).fetchone()
        if result:
            return User(
                id=result.id,
                name=result.name,
                email=result.email,
                password=result.password,
            )
        return None

    def update(self, user: User) -> None:
        query = (
            users.update()
            .where(users.c.id == user.id)
            .values(name=user.name, email=user.email, password=user.password)
        )
        result = self.connection.execute(query)
        if result.rowcount == 0:
            raise UserNotFoundException(user.id)

    def delete(self, user_id: int) -> None:
        query = users.delete().where(users.c.id == user_id)
        result = self.connection.execute(query)
        if result.rowcount == 0:
            raise UserNotFoundException(user_id)

    def create(self, user: UserDTO) -> int:
        query = (
            insert(users)
            .values(name=user.name, email=user.email, password=user.password)
            .returning(users.c.id)
        )
        try:
            result = self.connection.execute(query)
            return result.scalar_one()
        except IntegrityError as e:
            raise DatabaseConstraintException(str(e.orig))
