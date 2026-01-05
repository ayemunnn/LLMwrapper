from fastapi import FastAPI
from dotenv import load_dotenv
from app.db.init_db import init_db
from app.api.routes_health import router as health_router
from app.api.routes_generate import router as generate_router

load_dotenv()
init_db()

app = FastAPI(title="NimbusLLM", version="0.1.0")
app.include_router(health_router)
app.include_router(generate_router)
