from pydantic import BaseModel

class LLMResult(BaseModel):
    output: str
    input_tokens: int | None = None
    output_tokens: int | None = None

class LLMProvider:
    name: str = "base"
    async def generate(self, prompt: str, model: str) -> LLMResult:
        raise NotImplementedError
