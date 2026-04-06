from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse

from app.api.depends import TokenJWTServiceDep, UserCurrentDep, UserServiceDep
from app.api.schemas import (
    UserRegisterRequest,
    UserVerifiedStatusResponse,
    VisibleDataUserResponse,
)
from app.api.schemas.general import ErrorResponse
from app.exceptions import EmailAlreadyRegisterError
from app.exceptions.user_exceptions import (
    UserNotFoundByToken,
    VerificationEmailExpired,
    VerificationEmailInvalid,
)
from app.settings.enviroment import helper_url_verify_check_email

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


@router.get(
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
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    responses={
        401: {"model": ErrorResponse, "description": "Usuario no encontrado"},
        406: {"model": ErrorResponse, "description": "Validación de email inválida"},
        404: {"model": ErrorResponse, "description": "Token inválido"},
    },
)
def confirm_email(
    token: str,
    user_service: UserServiceDep,
    token_jwt_service: TokenJWTServiceDep,
):
    try:
        user = user_service.verified(token)
        if user.id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )
        access_token = token_jwt_service.encode(user.id, user.name)

        response = RedirectResponse(url=helper_url_verify_check_email("success"))

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )

        return response
    except VerificationEmailInvalid:
        RedirectResponse(url=helper_url_verify_check_email("invalid"))
    except UserNotFoundByToken:
        RedirectResponse(url=helper_url_verify_check_email("invalid"))
    except VerificationEmailExpired:
        RedirectResponse(url=helper_url_verify_check_email("expired"))
