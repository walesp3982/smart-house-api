from typing import Literal

from fastapi_mail import FastMail, MessageSchema, MessageType
from pydantic import NameEmail

from app.settings import connection_config_email, general_settings

from .builder import EmailContentBuilder, VerificationEmailBuilder

EmailOptionsliteral = Literal["verification", "forgot_password"]


class FactoryEmailContent:
    @staticmethod
    def create(type: EmailOptionsliteral, **kwargs) -> EmailContentBuilder:
        match type:
            case "verification":
                return VerificationEmailBuilder(**kwargs)
        raise ValueError()


class EmailSender:
    def __init__(self):
        self.email_provider = FastMail(connection_config_email)

    async def execute(self, html: str, email_address: list[NameEmail]):
        message = MessageSchema(
            subject=general_settings.app_name,
            recipients=email_address,
            subtype=MessageType.html,
            body=html,
        )

        await self.email_provider.send_message(message)
