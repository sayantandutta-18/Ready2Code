import socket
import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
import httpx
from ..database import get_db
from ..config import settings

router = APIRouter(tags=["health"])
logger = logging.getLogger("api.health")

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Comprehensive multi-service health check verifying:
    1. Postgres / SQLite database connectivity
    2. Redis cache connectivity
    3. Judge0 code execution engine availability
    """
    # 1. Database Check
    db_ok = False
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception as exc:
        logger.warning("Database health check failed: %s", exc)
        db_ok = False

    # 2. Redis Check
    redis_ok = False
    try:
        import redis
        r = redis.from_url(settings.REDIS_URL, socket_connect_timeout=1.0)
        redis_ok = bool(r.ping())
    except Exception as exc:
        logger.debug("Redis ping failed: %s", exc)
        try:
            from urllib.parse import urlparse
            p = urlparse(settings.REDIS_URL)
            host = p.hostname or settings.REDIS_HOST
            port = p.port or settings.REDIS_PORT
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.0)
            res = sock.connect_ex((host, port))
            sock.close()
            redis_ok = (res == 0)
        except Exception:
            redis_ok = False

    # 3. Judge0 Check
    judge0_ok = False
    try:
        with httpx.Client(timeout=0.4) as client:
            resp = client.get(f"{settings.JUDGE0_URL}/about")
            judge0_ok = (resp.status_code == 200)
    except Exception:
        # Fallback socket check on host/port if /about route isn't standard
        try:
            from urllib.parse import urlparse
            parsed = urlparse(settings.JUDGE0_URL)
            host = parsed.hostname or "localhost"
            port = parsed.port or 2358
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.2)
            res = sock.connect_ex((host, port))
            sock.close()
            judge0_ok = (res == 0)
        except Exception:
            judge0_ok = False

    status = "ok" if db_ok else "degraded"

    return {
        "status": status,
        "db": db_ok, # Preserved for backward compatibility with existing tests
        "redis": redis_ok,
        "judge0": judge0_ok,
        "postgres": "up" if db_ok else "down",
        "redis_status": "up" if redis_ok else "down",
        "judge0_status": "up" if judge0_ok else "down",
        "environment": settings.ENVIRONMENT,
        "app": "Ready2Code API"
    }
