import time
import uuid
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.db.models import LLMRequestLog
from app.providers.factory import get_provider
from app.schemas.generate import GenerateRequest, GenerateResponse
router = APIRouter()

@router.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest, db: Session = Depends(get_db)):
    start = time.time()
    request_id = f"req_{uuid.uuid4().hex[:12]}"
    provider_name = req.provider.lower().strip()

    try:
        provider = get_provider(provider_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    prompt_text = req.messages[-1].content  # simple v1: last user message only

    try:
        result = await provider.generate(
            messages=[m.model_dump() for m in req.messages],
            model=req.model,
            temperature=req.temperature,
            max_tokens=req.max_tokens,
        )
        latency_ms = int((time.time() - start) * 1000)

        usage = result.get("usage", {"input_tokens": 0, "output_tokens": 0})
        text = result["text"]

        db.add(
            LLMRequestLog(
                request_id=request_id,
                provider=provider_name,
                model=req.model,
                prompt=prompt_text,
                response_text=text,
                input_tokens=int(usage.get("input_tokens", 0)),
                output_tokens=int(usage.get("output_tokens", 0)),
                latency_ms=latency_ms,
                status="success",
                error=None,
            )
        )
        db.commit()

        return GenerateResponse(
            id=request_id,
            provider=provider_name,
            model=req.model,
            text=text,
            usage={
                "input_tokens": int(usage.get("input_tokens", 0)),
                "output_tokens": int(usage.get("output_tokens", 0)),
            },
            latency_ms=latency_ms,
            raw=result.get("raw"),
        )

    except Exception as e:
        latency_ms = int((time.time() - start) * 1000)

        db.add(
            LLMRequestLog(
                request_id=request_id,
                provider=provider_name,
                model=req.model,
                prompt=prompt_text,
                response_text="",
                input_tokens=0,
                output_tokens=0,
                latency_ms=latency_ms,
                status="fail",
                error=str(e),
            )
        )
        db.commit()

        raise HTTPException(status_code=500, detail="Provider call failed")
