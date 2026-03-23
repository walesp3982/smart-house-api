from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.api.depends.service import TokenJWTServiceDep, UserServiceDep
from app.api.schemas import Payload
from app.entities import UserEntity
from app.exceptions import UserNotFoundByIdError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_payload(
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_service: TokenJWTServiceDep,
) -> Payload:
    try:
        payload = jwt_service.decode(token)
        return payload
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.__str__,
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.__str__,
        )


PayloadDep = Annotated[Payload, Depends(get_payload)]


def get_user_current(
    payload: Annotated[Payload, Depends(get_payload)],
    user_service: UserServiceDep,
) -> UserEntity:
    try:
        user = user_service.get_user_by_id(int(payload.sub))
        return user
    except UserNotFoundByIdError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
        )


UserCurrentDep = Annotated[UserEntity, Depends(get_user_current)]


def get_user_verified(current_user: UserCurrentDep) -> UserEntity:
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not verified"
        )
    return current_user
