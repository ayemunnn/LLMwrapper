import time, uuid
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.auth import require_api_key
from app.providers.factory import get_provider
from app.db.session import SessionLocal
from app.db.models import RequestLog

router = APIRouter()

class GenerateRequest(BaseModel):
    task: str
    input: str
    model: str = "default"

class GenerateResponse(BaseModel):
    request_id: str
    output: str
    latency_ms: int
    usage: dict

@router.post("/v1/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest, api_key: str = Depends(require_api_key)):
    request_id = uuid.uuid4().hex
    t0 = time.perf_counter()

    provider = get_provider()
    status = "ok"
    err = None

    try:
        # v1 prompt: simple template (later swap to YAML prompt registry)
        prompt = f"Task: {req.task}\n\nInput:\n{req.input}"
        result = await provider.generate(prompt=prompt, model=req.model)
    except Exception as e:
        status = "error"
        err = str(e)
        raise
    finally:
        latency_ms = int((time.perf_counter() - t0) * 1000)
        # write telemetry
        db = SessionLocal()
        try:
            db.add(RequestLog(
                request_id=request_id,
                api_key=api_key,
                provider=provider.name,
                model=req.model,
                input_chars=len(req.input),
                latency_ms=latency_ms,
                status=status,
                error=err
            ))
            db.commit()
        finally:
            db.close()

    return GenerateResponse(
        request_id=request_id,
        output=result.output,
        latency_ms=latency_ms,
        usage={"input_tokens": result.input_tokens, "output_tokens": result.output_tokens}
    )
