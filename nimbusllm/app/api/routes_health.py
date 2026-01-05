from fastapi import APIRouter
from app.db.session import engine

router = APIRouter()

@router.get("/v1/health")
def health():
    # minimal DB ping
    ok = True
    try:
        with engine.connect() as conn:
            conn.exec_driver_sql("SELECT 1")
    except Exception:
        ok = False
    return {"status": "ok" if ok else "degraded"}
