from fastapi import FastAPI
from app.api.routes_health import router as health_router
from app.api.routes_generate import router as generate_router

app = FastAPI(title="NimbusLLM", version="0.1.0")

app.include_router(health_router, tags=["health"])
app.include_router(generate_router, tags=["generate"])
