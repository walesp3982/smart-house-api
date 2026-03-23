from fastapi import APIRouter

from app.depends import DeviceServiceDep
from app.schemas import CreateDeviceRequest

router = APIRouter(prefix="/device", tags=["dispositivos"])


@router.post("/")
def create_device(
    data: CreateDeviceRequest,
    device_service: DeviceServiceDep,
):
    device_service.create(data)
