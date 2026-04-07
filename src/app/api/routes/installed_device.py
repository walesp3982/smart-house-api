from fastapi import APIRouter, HTTPException, status

from app.api.depends.auth import UserVerifyDep
from app.api.depends.service import InstalledDeviceServiceDep
from app.api.schemas.command import CommandJson
from app.api.schemas.installed_device import (
    CreateInstalledDeviceRequest,
    UpdateInstalledDeviceRequest,
)
from app.exceptions.installed_device_exceptions import (
    InstalledDeviceAlreadyRegisteredError,
    InstalledDeviceNotFoundByIdError,
    InstalledDeviceUnauthorizedError,
    InstalledDeviceVerificationError,
)

router = APIRouter(prefix="/installed_devices", tags=["Installed Devices"])


@router.get("", response_model=list[dict])
def get_installed_devices(
    user: UserVerifyDep,
    service: InstalledDeviceServiceDep,
):
    """Obtiene todos los installed_devices del usuario autenticado."""
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id de usuario no encontrado",
        )

    devices = service.get_all(user.id)
    return [
        {
            "id": device.id,
            "name": device.name,
            "device_id": device.device_id,
            "house_id": device.house_id,
            "area_id": device.area_id,
        }
        for device in devices
    ]


@router.get("/{installed_device_id}", response_model=dict)
def get_installed_device(
    installed_device_id: int,
    user: UserVerifyDep,
    service: InstalledDeviceServiceDep,
):
    """Obtiene un installed_device con join a device."""
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id de usuario no encontrado",
        )

    try:
        device = service.get_by_id(installed_device_id, user.id)
        return {
            "id": device.id,
            "name": device.name,
            "device_id": device.device_id,
            "house_id": device.house_id,
            "area_id": device.area_id,
            "device": {
                "id": device.device.id,
                "device_uuid": device.device.device_uuid,
                "type": device.device.type.value,
            },
        }
    except InstalledDeviceNotFoundByIdError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Installed device no encontrado",
        )
    except InstalledDeviceUnauthorizedError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a este dispositivo",
        )


@router.post("", status_code=status.HTTP_201_CREATED, response_model=dict)
def register_installed_device(
    request: CreateInstalledDeviceRequest,
    user: UserVerifyDep,
    service: InstalledDeviceServiceDep,
):
    """Registra un nuevo installed_device con uuid y código de verificación."""
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id de usuario no encontrado",
        )

    try:
        device_id = service.create(user.id, request)
        device = service.repository.get_by_id(device_id)
        if device is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear el dispositivo",
            )
        return {
            "id": device.id,
            "name": device.name,
            "device_id": device.device_id,
            "house_id": device.house_id,
            "area_id": device.area_id,
        }
    except InstalledDeviceNotFoundByIdError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado con el uuid proporcionado",
        )
    except InstalledDeviceAlreadyRegisteredError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except InstalledDeviceVerificationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Código de verificación inválido",
        )


@router.patch("/{installed_device_id}", response_model=dict)
def update_installed_device(
    installed_device_id: int,
    request: UpdateInstalledDeviceRequest,
    user: UserVerifyDep,
    service: InstalledDeviceServiceDep,
):
    """Actualiza un installed_device (name, house_id, area_id)."""
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id de usuario no encontrado",
        )

    try:
        service.update(installed_device_id, user.id, request)
        device = service.repository.get_by_id(installed_device_id)
        if device is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar el dispositivo",
            )
        return {
            "id": device.id,
            "name": device.name,
            "device_id": device.device_id,
            "house_id": device.house_id,
            "area_id": device.area_id,
        }
    except InstalledDeviceNotFoundByIdError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Installed device no encontrado",
        )
    except InstalledDeviceUnauthorizedError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para actualizar este dispositivo",
        )


@router.delete("/{installed_device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_installed_device(
    installed_device_id: int,
    user: UserVerifyDep,
    service: InstalledDeviceServiceDep,
):
    """Elimina un installed_device."""
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id de usuario no encontrado",
        )

    try:
        service.delete(installed_device_id, user.id)
    except InstalledDeviceNotFoundByIdError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Installed device no encontrado",
        )
    except InstalledDeviceUnauthorizedError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este dispositivo",
        )


@router.post("/{installed_device_id}/command", status_code=status.HTTP_202_ACCEPTED)
def settings_installed_device(actions: CommandJson):
    pass
