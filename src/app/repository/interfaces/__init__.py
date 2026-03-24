from .device import DeviceRepositoryProtocol
from .house import FilterGetAllHouse, HouseRepositoryProtocol
from .user import UserRepositoryProtocol

__all__ = [
    "UserRepositoryProtocol",
    "DeviceRepositoryProtocol",
    "HouseRepositoryProtocol",
    "FilterGetAllHouse",
]
