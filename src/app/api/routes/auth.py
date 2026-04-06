from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.depends import TokenJWTServiceDep, UserServiceDep
from app.api.schemas import CredencialsUserRequest
from app.api.schemas.auth import Token
from app.api.schemas.general import ErrorResponse
from app.exceptions import (
    CredencialsUserIncorrectError,
    UserNotFoundByEmailError,
)

router = APIRouter()


@router.post(
    "/token",
    responses={
        401: {"model": ErrorResponse, "description": "Credenciales inválidas"},
    },
)
def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserServiceDep,
    jwt_service: TokenJWTServiceDep,
) -> Token:
    # Creamos las credenciales
    credencials = CredencialsUserRequest(
        email=form_data.username,
        password=form_data.password,
    )

    # Inicializamos sesion con el usuario
    try:
        user = user_service.get_user_by_credencials(credencials)

        if user.id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        token = jwt_service.encode(user.id, user.name)
        return Token(access_token=token, token_type="Bearer")
    except UserNotFoundByEmailError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except CredencialsUserIncorrectError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
