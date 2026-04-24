from typing import Generator, Type

from groq import Groq

from app.exceptions.llm_exceptions import LLMResponseNotCreated
from app.settings.ai_models import AIModelsSettings

from .interfaces.base import (
    BaseLLMProvider,
    CreativityLevel,
    SizeResponse,
    TModel,
    get_max_token,
)

ai_models_settings = AIModelsSettings()


class GroqProvider(BaseLLMProvider):
    def __init__(self):
        self.client = Groq(api_key=ai_models_settings.groq_api_key)

    def _get_temperature(self, creativity: CreativityLevel) -> float:
        match creativity:
            case "HIGH":
                return 1
            case "MEDIUM":
                return 0.5
            case "LOW":
                return 0

    def structured_chat(
        self,
        system_message: str,
        user_message: str,
        creativity: CreativityLevel,
        size_response: SizeResponse,
        schema: Type[TModel],
    ) -> TModel:
        temperature = self._get_temperature(creativity)
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            model=ai_models_settings.groq_commands_model,
            temperature=temperature,
            max_completion_tokens=get_max_token(size_response),
            response_format={"type": "json_object"},
        )

        response = chat_completion.choices[0].message.content
        if response is None:
            raise LLMResponseNotCreated()
        return schema.model_validate_json(response)

    def stream_chat(
        self,
        system_message: str,
        user_message: str,
        creativity: CreativityLevel,
        size_response: SizeResponse,
    ) -> Generator[str, None, None]:
        temperature = self._get_temperature(creativity)
        stream = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            model=ai_models_settings.groq_commands_model,
            stream=True,
            temperature=temperature,
            max_tokens=get_max_token(size_response),
        )
        for chuck in stream:
            if not chuck.choices:
                continue
            part = chuck.choices[0].delta.content
            if part is not None:
                yield part
