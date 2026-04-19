from typing import Literal

from .gemini import GeminiProvider
from .groq import GroqProvider
from .interfaces.base import BaseLLMProvider
from .ollama import OllamaProvider

ProviderOptions = Literal["gemini", "groq", "ollama"]


class LLMFactoryProvider:
    @staticmethod
    def get_provider(option: ProviderOptions) -> BaseLLMProvider:
        match option:
            case "gemini":
                return GeminiProvider()
            case "groq":
                return GroqProvider()
            case "ollama":
                return OllamaProvider()
