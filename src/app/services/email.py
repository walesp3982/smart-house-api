from abc import ABC, abstractmethod
from enum import StrEnum
from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, MessageType
from jinja2 import Environment, FileSystemLoader
from pydantic import NameEmail

from app.settings import connection_config_email, general_settings

BASE_DIR = Path(__file__).resolve().parent
DIR_TEMPLATES = "templates"


class EmailContentBuilder(ABC):
    def __init__(self):
        self.enviroment = Environment(loader=FileSystemLoader(BASE_DIR / DIR_TEMPLATES))

    @abstractmethod
    def generate(self) -> str: ...


class VerificationEmailBuilder(EmailContentBuilder):
    def __init__(self, url: str, name: str) -> None:
        super().__init__()
        self.url = url
        self.name = name

    def generate(self) -> str:
        template = self.enviroment.get_template("email/verify_email.html")

        # /users/email-verification/{token}
        content = template.render(
            {
                "url": self.url,
                "name": self.name,
            }
        )
        return content


class EmailContentEnum(StrEnum):
    verification = "verification"


class FactoryEmailContent:
    @staticmethod
    def create(type: EmailContentEnum, **kwargs) -> EmailContentBuilder:
        match type:
            case EmailContentEnum.verification:
                return VerificationEmailBuilder(**kwargs)
        return ValueError()


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
