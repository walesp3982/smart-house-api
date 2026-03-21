from fastapi import APIRouter, HTTPException, Response, status

from app.depends import UserCurrentDep, UserServiceDep
from app.exceptions import EmailAlreadyRegisterError
from app.schemas import (
    UserRegisterRequest,
    UserVerifiedStatusResponse,
    VisibleDataUserResponse,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
async def register(
    data: UserRegisterRequest, user_service: UserServiceDep, response: Response
):
    try:
        user = await user_service.register_user(data, "/users/email-verification/")
        return VisibleDataUserResponse(**user.model_dump())
    except EmailAlreadyRegisterError:
        HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email ya registrado"
        )


@router.post("/me")
def info_actual_user(actual_user: UserCurrentDep) -> VisibleDataUserResponse:
    return VisibleDataUserResponse(**actual_user.model_dump())


@router.get("/verified")
def get_verified_user(user_id: int, user_service: UserServiceDep):
    is_verified = user_service.user_is_verified(user_id)
    return UserVerifiedStatusResponse(status=is_verified)


@router.post("/email-verification/{token}")
def confirm_email(token: str, user_service: UserServiceDep):
    user_service.verified(token)
    Response(status_code=status.HTTP_204_NO_CONTENT)
