from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Any

class Message(BaseModel):
    role: Literal["system", "user", "assistant", "tool"] = "user"
    content: str = Field(..., min_length=1)

class GenerateRequest(BaseModel):
    provider: str = Field(..., min_length=1)
    model: str = Field(..., min_length=1)
    messages: List[Message] = Field(..., min_length=1)  # ✅ prevents empty list
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(512, ge=1, le=32768)

class Usage(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0

class GenerateResponse(BaseModel):
    id: str
    provider: str
    model: str
    text: str
    usage: Usage
    latency_ms: int
    raw: Optional[Any] = None
