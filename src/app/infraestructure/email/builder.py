from abc import ABC, abstractmethod
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

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
