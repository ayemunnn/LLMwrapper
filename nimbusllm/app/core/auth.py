import os
from fastapi import Header, HTTPException

def require_api_key(x_api_key: str = Header(default="")) -> str:
    allowed = [k.strip() for k in os.getenv("API_KEYS", "").split(",") if k.strip()]
    if not allowed:
        raise HTTPException(status_code=500, detail="API_KEYS not configured")
    if x_api_key not in allowed:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key
