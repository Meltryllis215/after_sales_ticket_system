from fastapi import FastAPI

from app.config import DB_PATH, LLM_API_KEY
from app.database import ensure_database
from app.routers import tickets


ensure_database()

app = FastAPI(title="智能售后工单处理系统", version="0.1.0")

app.include_router(tickets.router)


@app.get("/health")
def health_check() -> dict:
    return {
        "message": "after sales ticket system is running",
        "database": str(DB_PATH),
        "llm_enabled": bool(LLM_API_KEY),
    }
