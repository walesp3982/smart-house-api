from fastapi import APIRouter, Depends, HTTPException, status

from app.api.depends.auth import UserVerifyDep
from app.api.depends.service import AreaServiceDep, HouseServiceDep
from app.api.schemas.area import AreaResponse, CreateAreaRequest, UpdateAreaRequest
from app.api.schemas.general import ErrorResponse
from app.exceptions.areas_exceptions import (
    AreaNotFoundByIdError,
    DuplicateNameAreaError,
)
from app.exceptions.house_exception import (
    HouseNotFoundByIdError,
    HouseUnathorizadedError,
)


def verify_house_ownership(house_id: int, user: UserVerifyDep, house_service: HouseServiceDep):
    """Verifica que la casa pertenezca al usuario autenticado."""
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id de usuario no encontrado",
        )
    try:
        house_service.get_house_by_id(house_id, user.id)
    except HouseUnathorizadedError:
        raise HTTPException(status_code=403, detail="No tienes acceso a esta casa")
    except HouseNotFoundByIdError:
        raise HTTPException(status_code=404, detail="Casa no encontrada")


router = APIRouter(tags=["Areas"])


@router.get(
    "/houses/{house_id}/areas",
    response_model=list[AreaResponse],
    responses={
        200: {"model": list[AreaResponse], "description": "Lista de áreas de la casa"},
        400: {"model": ErrorResponse, "description": "ID de usuario no encontrado"},
        403: {"model": ErrorResponse, "description": "No tienes acceso a esta casa"},
        404: {"model": ErrorResponse, "description": "Casa no encontrada"},
    },
)
def get_areas_by_house(
    house_id: int, area_service: AreaServiceDep, _=Depends(verify_house_ownership)
):
    """Obtiene todas las áreas de una casa."""
    areas = area_service.get_areas_by_house_id(house_id)
    return [AreaResponse.from_entity(area) for area in areas]


@router.get(
    "/houses/{house_id}/areas/{area_id}",
    response_model=AreaResponse,
    responses={
        200: {"model": AreaResponse, "description": "Área encontrada"},
        400: {"model": ErrorResponse, "description": "ID de usuario no encontrado"},
        403: {"model": ErrorResponse, "description": "No tienes acceso a esta casa"},
        404: {"model": ErrorResponse, "description": "Casa o área no encontrada"},
    },
)
def get_area_by_id(
    house_id: int,
    area_id: int,
    area_service: AreaServiceDep,
    _=Depends(verify_house_ownership),
):
    """Obtiene una área específica por su ID."""
    try:
        area = area_service.get_area_by_id(area_id)
        return AreaResponse.from_entity(area)
    except AreaNotFoundByIdError:
        raise HTTPException(status_code=404, detail="Área no encontrada")


@router.post(
    "/houses/{house_id}/areas",
    response_model=AreaResponse,
    responses={
        200: {"model": AreaResponse, "description": "Área creada exitosamente"},
        400: {
            "model": ErrorResponse,
            "description": "ID de usuario no encontrado o datos inválidos",
        },
        403: {"model": ErrorResponse, "description": "No tienes acceso a esta casa"},
        404: {"model": ErrorResponse, "description": "Casa no encontrada"},
        409: {
            "model": ErrorResponse,
            "description": "Nombre de área duplicado en la casa",
        },
    },
)
def create_area(
    house_id: int,
    request: CreateAreaRequest,
    area_service: AreaServiceDep,
    _=Depends(verify_house_ownership),
):
    """Crea una nueva área en una casa."""
    try:
        area_id = area_service.create_area(house_id, request)
        area = area_service.get_area_by_id(area_id)
        return AreaResponse.from_entity(area)
    except DuplicateNameAreaError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.patch(
    "/houses/{house_id}/areas/{area_id}",
    response_model=AreaResponse,
    responses={
        200: {"model": AreaResponse, "description": "Área actualizada exitosamente"},
        400: {
            "model": ErrorResponse,
            "description": "ID de usuario no encontrado",
        },
        403: {"model": ErrorResponse, "description": "No tienes acceso a esta casa"},
        404: {"model": ErrorResponse, "description": "Casa o área no encontrada"},
    },
)
def patch_area(
    house_id: int,
    area_id: int,
    request: UpdateAreaRequest,
    area_service: AreaServiceDep,
    _=Depends(verify_house_ownership),
):
    """Actualiza parcialmente una área."""
    try:
        success = area_service.patch_area(area_id, request)
        if not success:
            raise HTTPException(
                status_code=400, detail="No se proporcionaron campos para actualizar"
            )
        area = area_service.get_area_by_id(area_id)
        return AreaResponse.from_entity(area)
    except AreaNotFoundByIdError:
        raise HTTPException(status_code=404, detail="Área no encontrada")
    except DuplicateNameAreaError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete(
    "/houses/{house_id}/areas/{area_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Área eliminada exitosamente"},
        400: {"model": ErrorResponse, "description": "ID de usuario no encontrado"},
        403: {"model": ErrorResponse, "description": "No tienes acceso a esta casa"},
        404: {"model": ErrorResponse, "description": "Casa o área no encontrada"},
    },
)
def delete_area(
    house_id: int,
    area_id: int,
    area_service: AreaServiceDep,
    _=Depends(verify_house_ownership),
):
    """Elimina una área."""
    try:
        area_service.delete_area(area_id)
        return {"message": "Área eliminada"}
    except AreaNotFoundByIdError:
        raise HTTPException(status_code=404, detail="Área no encontrada")
