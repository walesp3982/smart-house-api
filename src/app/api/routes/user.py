from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse

from app.api.depends import TokenJWTServiceDep, UserCurrentDep, UserServiceDep
from app.api.schemas import (
    ForgotPasswordRequest,
    ResetPasswordRequest,
    UserRegisterRequest,
    UserVerifiedStatusResponse,
    VisibleDataUserResponse,
)
from app.api.schemas.general import ErrorResponse
from app.exceptions import EmailAlreadyRegisterError
from app.exceptions.user_exceptions import (
    ResetPasswordTokenExpired,
    ResetPasswordTokenInvalid,
    UserNotFoundByToken,
    VerificationEmailExpired,
    VerificationEmailInvalid,
)
from app.settings.enviroment import (
    helper_url_reset_password,
    helper_url_verify_check_email,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/register",
    responses={
        200: {
            "model": VisibleDataUserResponse,
            "description": "Usuario registrado exitosamente",
        },
        400: {"model": ErrorResponse, "description": "Email ya registrado"},
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
    "/forgot-password",
    responses={
        200: {
            "description": "Se ha enviado un correo para restablecer la contraseña",
        },
    },
)
async def forgot_password(data: ForgotPasswordRequest, user_service: UserServiceDep):
    await user_service.forgot_password(data.email, helper_url_reset_password())
    return {"message": "Se ha enviado un correo para restablecer la contraseña."}


@router.post(
    "/reset-password/{token}",
    responses={
        200: {
            "description": "Contraseña restablecida correctamente",
        },
        404: {"model": ErrorResponse, "description": "Token inválido"},
        406: {"model": ErrorResponse, "description": "Token expirado"},
    },
)
def reset_password(
    token: str,
    data: ResetPasswordRequest,
    user_service: UserServiceDep,
):
    try:
        user_service.reset_password(token, data.password)
        return {"message": "Contraseña restablecida correctamente."}
    except ResetPasswordTokenInvalid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token de restablecimiento inválido",
        )
    except ResetPasswordTokenExpired:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Token de restablecimiento expirado",
        )


@router.get(
    "/me",
    responses={
        200: {
            "model": VisibleDataUserResponse,
            "description": "Información del usuario actual",
        },
        401: {"model": ErrorResponse, "description": "Usuario no autenticado"},
    },
)
def info_actual_user(actual_user: UserCurrentDep) -> VisibleDataUserResponse:
    return VisibleDataUserResponse(**actual_user.model_dump())


@router.get(
    "/verified/{user_id}",
    responses={
        200: {
            "model": UserVerifiedStatusResponse,
            "description": "Estado de verificación del usuario",
        },
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
) -> RedirectResponse:
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
        return RedirectResponse(url=helper_url_verify_check_email("invalid"))
    except UserNotFoundByToken:
        return RedirectResponse(url=helper_url_verify_check_email("invalid"))
    except VerificationEmailExpired:
        return RedirectResponse(url=helper_url_verify_check_email("expired"))
