from fastapi import APIRouter, HTTPException, status

from app.api.depends import DeviceServiceDep
from app.api.schemas import CreateDeviceRequest
from app.api.schemas.device import CreateDeviceResponse
from app.exceptions.device_exception import DeviceDuplicateUUIDError

router = APIRouter(prefix="/devices", tags=["dispositivos"])


@router.post("")
def create_device(
    data: CreateDeviceRequest,
    device_service: DeviceServiceDep,
) -> CreateDeviceResponse:
    try:
        uuid = device_service.create(data)
        return CreateDeviceResponse(
            message=f"El dispositivo con uuid: {uuid} fue registrado existosamente"
        )
    except DeviceDuplicateUUIDError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Ya se registró el device"
        )
