from fastapi import APIRouter, HTTPException, status

from app.depends import DeviceServiceDep
from app.exceptions.device_exception import DeviceDuplicateUUIDError
from app.schemas import CreateDeviceRequest

router = APIRouter(prefix="/devices", tags=["dispositivos"])


@router.post("/")
def create_device(
    data: CreateDeviceRequest,
    device_service: DeviceServiceDep,
):
    try:
        device_service.create(data)
    except DeviceDuplicateUUIDError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Ya se registró el device"
        )
