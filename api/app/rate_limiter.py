import time
from collections import defaultdict, deque
from typing import Dict, Deque
from fastapi import Request, HTTPException, Depends
from .config import settings

# Thread-safe in-memory sliding window tracker: key -> deque of timestamps
_rate_limits: Dict[str, Deque[float]] = defaultdict(deque)

def check_rate_limit(key: str, max_requests: int, window_seconds: int = 60) -> None:
    """
    Enforces a sliding window rate limit. Raises 429 if limit is exceeded.
    """
    if not settings.ENABLE_RATE_LIMITING:
        return

    now = time.time()
    queue = _rate_limits[key]
    
    # Prune timestamps older than window
    cutoff = now - window_seconds
    while queue and queue[0] < cutoff:
        queue.popleft()
        
    if len(queue) >= max_requests:
        retry_after = int(queue[0] + window_seconds - now) + 1
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Maximum {max_requests} requests allowed per {window_seconds}s. Retry in {retry_after}s.",
            headers={"Retry-After": str(retry_after)}
        )
        
    queue.append(now)

def _get_client_identifier(request: Request) -> str:
    # Prefer authenticated user header or authorization if present
    auth = request.headers.get("Authorization")
    if auth and auth.startswith("Bearer "):
        return f"auth:{auth[7:30]}"
    x_user = request.headers.get("X-User-Id")
    if x_user:
        return f"user:{x_user}"
    # Fallback to client IP
    if request.client:
        return f"ip:{request.client.host}"
    return "ip:anonymous"

def rate_limit_submissions(request: Request):
    client_id = _get_client_identifier(request)
    check_rate_limit(
        key=f"submit:{client_id}",
        max_requests=settings.SUBMISSION_RATE_LIMIT_PER_MINUTE,
        window_seconds=60
    )

def rate_limit_ai(request: Request):
    client_id = _get_client_identifier(request)
    check_rate_limit(
        key=f"ai:{client_id}",
        max_requests=settings.AI_RATE_LIMIT_PER_MINUTE,
        window_seconds=60
    )

def rate_limit_general(request: Request):
    client_id = _get_client_identifier(request)
    check_rate_limit(
        key=f"gen:{client_id}",
        max_requests=settings.RATE_LIMIT_PER_MINUTE,
        window_seconds=60
    )
