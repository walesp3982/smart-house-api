from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.depends import TokenJWTServiceDep, UserServiceDep
from app.entities import User
from app.exceptions import UserNotFoundByIdException
from app.schemas import Payload

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


def get_user_current(
    payload: Annotated[Payload, Depends(get_payload)],
    user_service: UserServiceDep,
) -> User:
    try:
        user = user_service.get_user_by_id(int(payload.sub))
        return user
    except UserNotFoundByIdException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
        )
