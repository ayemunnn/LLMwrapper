import time
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Dict, Any

from app.providers.factory import get_provider

router = APIRouter()

Role = Literal["system", "user", "assistant"]

class Message(BaseModel):
    role: Role
    content: str = Field(min_length=1)

class GenerateRequest(BaseModel):
    provider: str = Field(min_length=1)
    model: str = Field(min_length=1)
    messages: List[Message] = Field(min_length=1)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None, ge=1, le=8192)

class GenerateResponse(BaseModel):
    id: str
    provider: str
    model: str
    text: str
    usage: Dict[str, int]
    latency_ms: int
    raw: Optional[Any] = None

@router.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest):
    start = time.time()
    request_id = f"req_{uuid.uuid4().hex[:12]}"

    try:
        provider = get_provider(req.provider)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    result = await provider.generate(
        messages=[m.model_dump() for m in req.messages],
        model=req.model,
        temperature=req.temperature,
        max_tokens=req.max_tokens,
    )

    latency_ms = int((time.time() - start) * 1000)

    return GenerateResponse(
        id=request_id,
        provider=req.provider.lower(),
        model=req.model,
        text=result["text"],
        usage=result.get("usage", {"input_tokens": 0, "output_tokens": 0}),
        latency_ms=latency_ms,
        raw=result.get("raw"),
    )
