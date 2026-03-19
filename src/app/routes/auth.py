from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.depends import TokenJWTServiceDep, UserServiceDep
from app.exceptions import (
    CredencialsUserIncorrectError,
    UserNotFoundByEmailError,
)
from app.schemas import CredencialsUser
from app.schemas.auth import Token

router = APIRouter()


@router.post("/token")
def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserServiceDep,
    jwt_service: TokenJWTServiceDep,
):
    # Creamos las credenciales
    credencials = CredencialsUser(
        email=form_data.username,
        password=form_data.password,
    )

    # Inicializamos sesion con el usuario
    try:
        user = user_service.get_user_by_credencials(credencials)

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
