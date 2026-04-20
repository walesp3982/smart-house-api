from typing import Generator, Type

from google import genai
from google.genai import types

from app.infraestructure.llm.interfaces.base import (
    BaseLLMProvider,
    CreativityLevel,
    SizeResponse,
    TModel,
    get_max_token,
)
from app.settings.ai_models import AIModelsSettings

ai_models_settings = AIModelsSettings


class GeminiProvider(BaseLLMProvider):
    def __init__(self):
        self.client = genai.Client(api_key=ai_models_settings.gemini_api_key)

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
        config_model = types.GenerateContentConfig(
            system_instruction=system_message,
            response_json_schema=schema.model_json_schema(),
            response_mime_type="application_json",
            temperature=self._get_temperature(creativity),
            max_output_tokens=get_max_token(size_response),
        )
        response = self.client.models.generate_content(
            model=ai_models_settings.gemini_commands_model,
            contents=user_message,
            config=config_model,
        )
        if response.text is None:
            raise
        return schema.model_validate_json(response.text)

    def stream_chat(
        self,
        system_message: str,
        user_message: str,
        creativity: CreativityLevel,
        size_response: SizeResponse,
    ) -> Generator[str, None, None]:
        config_model = types.GenerateContentConfig(
            system_instruction=system_message,
            temperature=self._get_temperature(creativity),
            max_output_tokens=get_max_token(size_response),
        )

        response = self.client.models.generate_content_stream(
            model=ai_models_settings.gemini_commands_model,
            contents=user_message,
            config=config_model,
        )

        for chunk in response:
            text = chunk.text
            if text is not None:
                yield text
