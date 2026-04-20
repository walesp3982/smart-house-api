from abc import ABC, abstractmethod
from typing import Generator, Literal, Type, TypeVar

from pydantic import BaseModel

CreativityLevel = Literal["LOW", "MEDIUM", "HIGH"]
SizeResponse = Literal["SMALL", "MEDIUM", "BIG"]
TModel = TypeVar("TModel", bound=BaseModel)


def get_max_token(size: SizeResponse):
    match size:
        case "BIG":
            return 1024
        case "MEDIUM":
            return 512
        case "SMALL":
            return 100


class BaseLLMProvider(ABC):
    @abstractmethod
    def structured_chat(
        self,
        system_message: str,
        user_message: str,
        creativity: CreativityLevel,
        size_response: SizeResponse,
        schema: Type[TModel],
    ) -> TModel: ...
    @abstractmethod
    def stream_chat(
        self,
        system_message: str,
        user_message: str,
        creativity: CreativityLevel,
        size_response: SizeResponse,
    ) -> Generator[str, None, None]: ...
