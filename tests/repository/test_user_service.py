import asyncio
from datetime import datetime, timedelta, timezone

import pytest

from app.entities import UserEntity
from app.exceptions.user_exceptions import (
    ResetPasswordTokenExpired,
    ResetPasswordTokenInvalid,
)
from app.services.user import UserService
from app.settings.enviroment import helper_url_reset_password


def test_forgot_password_generates_token_and_sends_email(user_repo, monkeypatch):
    user = UserEntity(
        name="juan",
        email="juan@gmail.com",
        password="password",
        is_verified=True,
    )
    user_id = user_repo.create(user)

    sent = {}

    async def fake_send_message(html: str, email_address: list):
        sent["html"] = html
        sent["email_address"] = email_address

    service = UserService(user_repo)
    monkeypatch.setattr(service.email_sender, "execute", fake_send_message)

    asyncio.run(service.forgot_password(user.email, helper_url_reset_password()))

    updated_user = user_repo.get_by_id(user_id)
    assert updated_user.password_reset_token is not None
    assert updated_user.password_reset_token_expired_at is not None
    assert "Restablecer contraseña" in sent["html"]
    assert updated_user.email == sent["email_address"][0].email


def test_reset_password_invalid_token(user_repo):
    service = UserService(user_repo)

    with pytest.raises(ResetPasswordTokenInvalid):
        service.reset_password("invalid-token", "newpassword")


def test_reset_password_expired_token(user_repo):
    user = UserEntity(
        name="maria",
        email="maria@gmail.com",
        password="password",
        is_verified=True,
        password_reset_token="reset123",
        password_reset_token_expired_at=datetime.now(timezone.utc)
        - timedelta(minutes=1),
    )
    user_id = user_repo.create(user)

    service = UserService(user_repo)

    with pytest.raises(ResetPasswordTokenExpired):
        service.reset_password("reset123", "newpassword")


def test_reset_password_updates_password(user_repo):
    user = UserEntity(
        name="pedro",
        email="pedro@gmail.com",
        password="password",
        is_verified=True,
        password_reset_token="reset123",
        password_reset_token_expired_at=datetime.now(timezone.utc)
        + timedelta(minutes=10),
    )
    user_id = user_repo.create(user)

    service = UserService(user_repo)
    service.reset_password("reset123", "newpassword")

    updated_user = user_repo.get_by_id(user_id)
    assert updated_user.password_reset_token is None
    assert updated_user.password_reset_token_expired_at is None
    assert updated_user.password != "password"
