import os
from .base import LLMProvider
from .mock import MockProvider

def get_provider() -> LLMProvider:
    provider = os.getenv("LLM_PROVIDER", "mock").lower()
    if provider == "mock":
        return MockProvider()
    # later: gemini/openai adapters here
    return MockProvider()
