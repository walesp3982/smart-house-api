from typing import cast

from fastapi import APIRouter, HTTPException, status

from app.api.depends import HouseServiceDep, UserVerifyDep
from app.api.schemas.general import ErrorResponse
from app.api.schemas.house import (
    CreateHouseRequest,
    HouseResponse,
    HouseWithAreasResponse,
    UpdateHouseRequest,
    UpdateHouseResponse,
)
from app.exceptions.house_exception import (
    HouseNotFoundByIdError,
    HouseUnathorizadedError,
)

router = APIRouter(prefix="/houses", tags=["Casa"])


@router.get(
    "",
    responses={
        200: {"description": "Lista de casas del usuario"},
        401: {"model": ErrorResponse, "description": "Usuario no autenticado"},
    },
)
def get_all_houses(
    user: UserVerifyDep,
    house_service: HouseServiceDep,
) -> list[HouseResponse]:
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Id del usuario no encontrado",
        )
    return cast(
        list[HouseResponse],
        house_service.get_all_houses_own_user(user.id, include_areas=False),
    )


@router.get(
    "/with-areas",
    responses={
        200: {"description": "Lista de casas del usuario con áreas"},
        401: {"model": ErrorResponse, "description": "Usuario no autenticado"},
    },
)
def get_all_houses_with_areas(
    user: UserVerifyDep,
    house_service: HouseServiceDep,
) -> list[HouseWithAreasResponse]:
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Id del usuario no encontrado",
        )
    return cast(
        list[HouseWithAreasResponse],
        house_service.get_all_houses_own_user(user.id, include_areas=True),
    )


@router.get(
    "/{id}",
    response_model=HouseResponse,
    responses={
        200: {"model": HouseResponse, "description": "Casa encontrada"},
        401: {
            "model": ErrorResponse,
            "description": "Usuario no autenticado o no autorizado",
        },
        404: {"model": ErrorResponse, "description": "Casa no encontrada"},
    },
)
def get_house(id: int, user: UserVerifyDep, house_service: HouseServiceDep) -> HouseResponse:
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Id del usuario no encontrado",
        )
    try:
        house = house_service.get_house_by_id(id, user.id)
        return HouseResponse.from_entity(house)
    except HouseNotFoundByIdError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Casa no encontrada")
    except HouseUnathorizadedError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Casa no autorizada")


@router.put(
    "/{id}",
    response_model=UpdateHouseResponse,
    responses={
        200: {"model": UpdateHouseResponse, "description": "Casa actualizada"},
        401: {
            "model": ErrorResponse,
            "description": "Usuario no autenticado o no autorizado",
        },
        404: {"model": ErrorResponse, "description": "Casa no encontrada"},
    },
)
def update_house(
    id: int,
    user: UserVerifyDep,
    house_service: HouseServiceDep,
    body: UpdateHouseRequest,
):
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Id del usuario no encontrado",
        )

    try:
        updated = house_service.update_house_data(id, body, user.id)

        return UpdateHouseResponse(
            message="Casa actualizada" if updated else "Casa sin cambios",
            updated=updated,
        )
    except HouseNotFoundByIdError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Casa no encontrada",
        )
    except HouseUnathorizadedError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Casa no autorizada",
        )


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Casa eliminada exitosamente"},
        401: {
            "model": ErrorResponse,
            "description": "Usuario no autenticado o no autorizado",
        },
        404: {"model": ErrorResponse, "description": "Casa no encontrada"},
    },
)
def delete_house(id: int, user: UserVerifyDep, house_service: HouseServiceDep):
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Id del usuario no encontrado",
        )

    try:
        house_service.delete_house(id, user.id)
    except HouseNotFoundByIdError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Casa no encontrada",
        )
    except HouseUnathorizadedError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Casa no autorizada",
        )


@router.post(
    "/",
    response_model=HouseResponse,
    responses={
        200: {"model": HouseResponse, "description": "Casa creada exitosamente"},
        401: {"model": ErrorResponse, "description": "Usuario no autenticado"},
    },
)
def create_house(
    body: CreateHouseRequest, user: UserVerifyDep, house_service: HouseServiceDep
) -> HouseResponse:
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Id del usuario no encontrado",
        )

    house = house_service.create_new_house(user.id, body)
    return HouseResponse.from_entity(house)
