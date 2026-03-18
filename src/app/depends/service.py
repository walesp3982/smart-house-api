from typing import Annotated

from fastapi import Depends

from app.depends.database import UserRepositoryDep
from app.services import TokenJWTService, UserService


def get_user_service(
    user_repository: UserRepositoryDep,
) -> UserService:
    return UserService(user_repository)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]

TokenJWTServiceDep = Annotated[TokenJWTService, Depends()]
