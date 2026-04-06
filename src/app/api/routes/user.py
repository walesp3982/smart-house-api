from fastapi import APIRouter, HTTPException, Response, status

from app.api.depends import UserCurrentDep, UserServiceDep
from app.api.schemas import (
    UserRegisterRequest,
    UserVerifiedStatusResponse,
    VisibleDataUserResponse,
)
from app.api.schemas.general import ErrorResponse
from app.exceptions import EmailAlreadyRegisterError
from app.exceptions.user_exceptions import UserNotFoundByToken, VerificationEmailInvalid

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/register",
    responses={
        400: {"model": ErrorResponse, "description": "Email duplicado"},
    },
)
async def register(
    data: UserRegisterRequest, user_service: UserServiceDep
) -> VisibleDataUserResponse:
    try:
        user = await user_service.register_user(data, "/users/email-verification/")
        return VisibleDataUserResponse(**user.model_dump())
    except EmailAlreadyRegisterError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email ya registrado"
        )


@router.post(
    "/me",
    responses={
        401: {"model": ErrorResponse, "description": "Usuario no encontrado"},
    },
)
def info_actual_user(actual_user: UserCurrentDep) -> VisibleDataUserResponse:
    return VisibleDataUserResponse(**actual_user.model_dump())


@router.post(
    "/verified",
    responses={
        401: {"model": ErrorResponse, "description": "Usuario no encontrado"},
    },
)
def get_verified_user(
    user_id: int, user_service: UserServiceDep
) -> UserVerifiedStatusResponse:
    is_verified = user_service.user_is_verified(user_id)
    return UserVerifiedStatusResponse(status=is_verified)


@router.get(
    "/email-verification/{token}",
    responses={
        401: {"model": ErrorResponse, "description": "Usuario no encontrado"},
        406: {"model": ErrorResponse, "description": "Validación de email inválida"},
        404: {"model": ErrorResponse, "description": "Token inválido"},
    },
)
def confirm_email(token: str, user_service: UserServiceDep):
    try:
        user_service.verified(token)
        Response(status_code=status.HTTP_204_NO_CONTENT)
    except VerificationEmailInvalid:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Validación de email inválida",
        )
    except UserNotFoundByToken:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Token inválido"
        )
