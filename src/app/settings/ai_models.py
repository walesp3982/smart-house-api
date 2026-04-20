from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

ProviderAvailable = Literal["groq", "gemini"]


class AIModelsSettings(BaseSettings):
    groq_api_key: str = ""
    gemini_api_key: str = ""
    llm_provider: ProviderAvailable = "gemini"
    groq_commands_model: str = "llama-3.1-8b-instant"
    groq_chat_model: str = "llama-3.3-70b-versatile"
    gemini_commands_model: str = "gemini-2.5-flash"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
