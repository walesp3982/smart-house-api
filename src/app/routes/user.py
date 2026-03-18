from fastapi import APIRouter, HTTPException, status

from app.depends import UserCurrentDep, UserServiceDep
from app.dto import UserDTO
from app.exceptions import EmailAlreadyRegisterError
from app.schemas import VisibleDataUser

router = APIRouter(prefix="users", tags=["users"])


@router.post("/register")
def register(data: UserDTO, user_service: UserServiceDep):
    try:
        user = user_service.create_user(data)
        return VisibleDataUser(**user.model_dump())
    except EmailAlreadyRegisterError:
        HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email ya registrado"
        )


@router.post("/me")
def info_actual_user(actual_user: UserCurrentDep) -> VisibleDataUser:
    return VisibleDataUser(**actual_user.model_dump())
