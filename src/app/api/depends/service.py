from typing import Annotated

from fastapi import Depends

from app.api.depends.database import DeviceRepositoryDep, UserRepositoryDep
from app.services import DeviceService, TokenJWTService, UserService


def get_user_service(
    user_repository: UserRepositoryDep,
) -> UserService:
    return UserService(user_repository)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


def get_device_service(
    device_repository: DeviceRepositoryDep,
) -> DeviceService:
    return DeviceService(device_repository)


DeviceServiceDep = Annotated[DeviceService, Depends(get_device_service)]

TokenJWTServiceDep = Annotated[TokenJWTService, Depends()]
