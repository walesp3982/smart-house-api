from sqlalchemy import Connection, insert, select
from sqlalchemy.exc import IntegrityError

from app.entities import UserEntity
from app.exceptions import DatabaseConstraintException, UserNotFoundError
from app.infraestructure.models import users


class UserRepository:
    """Repository for user operations."""

    def __init__(self, connection: Connection):
        self.connection = connection

    # Todo: Implementar filtros si es necesario
    def get_all(self, **filters) -> list[UserEntity]:
        query = select(users)
        result = self.connection.execute(query)
        return [
            UserEntity(
                id=row.id,
                name=row.name,
                email=row.email,
                password=row.password,
                is_verified=row.is_verified,
                verification_token=row.verification_token,
                verification_token_expired_at=row.verification_token_expired_at,
            )
            for row in result.fetchall()
        ]

    def get_by_id(self, user_id: int) -> UserEntity | None:
        query = select(users).where(users.c.id == user_id)
        result = self.connection.execute(query).fetchone()
        if result:
            return UserEntity(
                id=result.id,
                name=result.name,
                email=result.email,
                password=result.password,
                is_verified=result.is_verified,
                verification_token=result.verification_token,
                verification_token_expired_at=result.verification_token_expired_at,
            )
        return None

    def get_by_email(self, email: str) -> UserEntity | None:
        query = select(users).where(users.c.email == email)
        result = self.connection.execute(query).fetchone()
        if result:
            return UserEntity(
                id=result.id,
                name=result.name,
                email=result.email,
                password=result.password,
                is_verified=result.is_verified,
                verification_token=result.verification_token,
                verification_token_expired_at=result.verification_token_expired_at,
            )
        return None

    def update(self, user: UserEntity) -> None:
        if user.id is None:
            raise Exception()
        query = users.update().where(users.c.id == user.id).values(user.model_dump())
        result = self.connection.execute(query)
        if result.rowcount == 0:
            raise UserNotFoundError(user.id)

    def delete(self, user_id: int) -> None:
        query = users.delete().where(users.c.id == user_id)
        result = self.connection.execute(query)
        if result.rowcount == 0:
            raise UserNotFoundError(user_id)

    def create(self, user: UserEntity) -> int:
        data = user.model_dump()
        data.pop("id")
        query = insert(users).values(**data)
        try:
            result = self.connection.execute(query)
            return result.lastrowid
        except IntegrityError as e:
            raise DatabaseConstraintException(str(e.orig))

    def get_by_token(self, token: str) -> UserEntity | None:
        query = select(users).where(users.c.verification_token == token)

        rows = self.connection.execute(query).fetchone()

        if rows is None:
            return None

        return UserEntity(**rows._mapping)
