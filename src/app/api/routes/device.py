from fastapi import APIRouter, HTTPException, status

from app.api.depends import DeviceServiceDep
from app.api.schemas import CreateDeviceRequest
from app.exceptions.device_exception import DeviceDuplicateUUIDError

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
