from typing import Annotated

from fastapi import Depends

from app.api.depends.database import (
    AreaRepositoryDep,
    DeviceRepositoryDep,
    HouserRepositoryDep,
    UserRepositoryDep,
)
from app.services import (
    AreaService,
    DeviceService,
    HouseService,
    TokenJWTService,
    UserService,
)

TokenJWTServiceDep = Annotated[TokenJWTService, Depends()]


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


def get_house_service(house_repository: HouserRepositoryDep) -> HouseService:
    return HouseService(house_repository)


HouseServiceDep = Annotated[HouseService, Depends(get_house_service)]


def get_area_service(area_repository: AreaRepositoryDep) -> AreaService:
    return AreaService(area_repository)


AreaServiceDep = Annotated[AreaService, Depends(get_area_service)]
