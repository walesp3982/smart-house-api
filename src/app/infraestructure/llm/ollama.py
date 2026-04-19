from typing import Generator, Type

from ollama import ChatResponse, chat

from app.exceptions.llm_exceptions import LLMResponseNotCreated
from app.infraestructure.llm.interfaces.base import (
    BaseLLMProvider,
    CreativityLevel,
    SizeResponse,
    TModel,
    get_max_token,
)


class OllamaProvider(BaseLLMProvider):
    def __init__(self, model: str = "llama2"):
        self.model = model

    def _get_temperature(self, creativity: CreativityLevel):
        match creativity:
            case "LOW":
                return 0
            case "MEDIUM":
                return 1
            case "HIGH":
                return 2

    def structured_chat(
        self,
        system_message: str,
        user_message: str,
        creativity: CreativityLevel,
        size_response: SizeResponse,
        schema: Type[TModel],
    ) -> TModel:
        response: ChatResponse = chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_message,
                },
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
            format=schema.model_json_schema(),
            options={
                "temperature": self._get_temperature(creativity),
                "num_predict": get_max_token(size_response),
            },
        )

        if response.message.content is None:
            raise LLMResponseNotCreated
        return schema.model_validate_json(response.message.content)

    def stream_chat(
        self,
        system_message: str,
        user_message: str,
        creativity: CreativityLevel,
        size_response: SizeResponse,
    ) -> Generator[str, None, None]:
        stream = chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_message,
                },
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
            stream=True,
            options={
                "temperature": self._get_temperature(creativity),
                "num_predict": get_max_token(size_response),
            },
        )

        for chunk in stream:
            if chunk.message.content is not None:
                yield chunk.message.content
