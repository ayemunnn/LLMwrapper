from app.providers.mock import MockProvider

def get_provider(name: str):
    name = (name or "").lower().strip()

    if name == "mock":
        return MockProvider()

    # We'll add openai/gemini next
    raise ValueError(f"Unsupported provider: {name}")
