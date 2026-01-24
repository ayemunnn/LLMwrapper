from typing import Any, Dict, List, Optional
from app.providers.base import BaseLLMProvider

class MockProvider(BaseLLMProvider):
    async def generate(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        last = messages[-1]["content"]
        return {
            "text": f"[MOCK] model={model} temp={temperature} :: {last}",
            "usage": {
                "input_tokens": len(last.split()),
                "output_tokens": 12
            },
            "raw": None
        }
