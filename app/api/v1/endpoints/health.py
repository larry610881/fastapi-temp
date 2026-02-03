from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db
from app.core.redis import get_redis
import redis.asyncio as redis

router = APIRouter()

@router.get("/health")
async def health_check(
    db: AsyncSession = Depends(get_db),
    r: redis.Redis = Depends(get_redis)
):
    # Check DB
    db_status = "disconnected"
    try:
        await db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        pass

    # Check Redis
    redis_status = "disconnected"
    try:
        if await r.ping():
            redis_status = "connected"
    except Exception:
        pass

    return {
        "status": "ok",
        "database": db_status,
        "redis": redis_status,
        "api": "running"
    }
