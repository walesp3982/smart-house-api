from fastapi import APIRouter, HTTPException, status

from app.api.depends.auth import UserVerifyDep
from app.api.depends.service import TrackDeviceServiceDep
from app.api.schemas.general import ErrorResponse
from app.api.schemas.track_device import TrackDeviceResponse

router = APIRouter(prefix="/track_devices", tags=["Track Devices"])


@router.get(
    "/device/{device_id}",
    response_model=list[TrackDeviceResponse],
    responses={
        200: {
            "model": list[TrackDeviceResponse],
            "description": "Lista de seguimientos del dispositivo",
        },
        400: {"model": ErrorResponse, "description": "ID de usuario no encontrado"},
        404: {
            "model": ErrorResponse,
            "description": "Dispositivo no encontrado o no autorizado",
        },
    },
)
def get_track_by_device_id(
    device_id: int,
    user: UserVerifyDep,
    service: TrackDeviceServiceDep,
):
    """Obtiene el seguimiento de un dispositivo específico del usuario autenticado."""
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id de usuario no encontrado",
        )

    return service.get_by_device_id(device_id, user.id)


@router.get(
    "/house/{house_id}",
    response_model=list[TrackDeviceResponse],
    responses={
        200: {
            "model": list[TrackDeviceResponse],
            "description": "Lista de seguimientos de los dispositivos de la casa",
        },
        400: {"model": ErrorResponse, "description": "ID de usuario no encontrado"},
        404: {
            "model": ErrorResponse,
            "description": "Casa no encontrada o no autorizada",
        },
    },
)
def get_track_by_house_id(
    house_id: int,
    user: UserVerifyDep,
    service: TrackDeviceServiceDep,
):
    """Obtiene el seguimiento de los dispositivos de una casa."""
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id de usuario no encontrado",
        )

    return service.get_by_house_id(house_id, user.id)


@router.get(
    "/user",
    response_model=list[TrackDeviceResponse],
    responses={
        200: {
            "model": list[TrackDeviceResponse],
            "description": "Seguimientos de todos los dispositivos del usuario",
        },
        400: {"model": ErrorResponse, "description": "ID de usuario no encontrado"},
    },
)
def get_track_by_user_id(
    user: UserVerifyDep,
    service: TrackDeviceServiceDep,
):
    """Obtiene el seguimiento de todos los dispositivos del usuario autenticado."""
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id de usuario no encontrado",
        )

    return service.get_by_user_id(user.id)
