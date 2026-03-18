from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.depends import UserServiceDep
from app.exceptions import (
    CredencialsUserIncorrectError,
    UserNotFoundByEmailError,
)
from app.schemas import CredencialsUser

router = APIRouter()


@router.post("/token")
def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserServiceDep,
):
    # Creamos las credenciales
    credencials = CredencialsUser(
        email=form_data.username,
        password=form_data.password,
    )

    # Inicializamos sesion con el usuario
    try:
        user = user_service.get_user_by_credencials(credencials)
        return {"access_token": user.email, "token_type": "bearer"}
    except UserNotFoundByEmailError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )

    except CredencialsUserIncorrectError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
