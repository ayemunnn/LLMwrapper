from .base import LLMProvider, LLMResult

class MockProvider(LLMProvider):
    name = "mock"

    async def generate(self, prompt: str, model: str) -> LLMResult:
        # Very simple placeholder so the whole system works end-to-end
        out = f"[MOCK:{model}] {prompt[:400]}"
        return LLMResult(output=out, input_tokens=len(prompt)//4, output_tokens=len(out)//4)
