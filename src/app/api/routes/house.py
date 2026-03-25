from fastapi import APIRouter, HTTPException, status

from app.api.depends import HouseServiceDep, UserVerifyDep
from app.api.schemas.house import (
    CreateHouseRequest,
    UpdateHouseRequest,
    UpdateHouseResponse,
)
from app.exceptions.house_exception import (
    HouseNotFoundByIdError,
    HouseUnathorizadedError,
)

router = APIRouter(prefix="/houses", tags=["Casa"])


@router.get("/")
def get_all_house(user: UserVerifyDep, house_service: HouseServiceDep):
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Id del usuario no encontrado",
        )
    houses = house_service.get_all_houses_own_user(user.id)
    return houses


@router.get("/{id}")
def get_house(id: int, user: UserVerifyDep, house_service: HouseServiceDep):
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Id del usuario no encontrado",
        )
    try:
        house = house_service.get_house_by_id(id, user.id)
        return house
    except HouseNotFoundByIdError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Casa no encontrada"
        )
    except HouseUnathorizadedError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Casa no autorizada"
        )


@router.put("/{id}")
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


@router.post("/")
def create_house(
    body: CreateHouseRequest, user: UserVerifyDep, house_service: HouseServiceDep
):
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Id del usuario no encontrado",
        )

    house = house_service.create_new_house(user.id, body)
    return house
