import json
import logging
import sys
import time
from datetime import datetime, timezone
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class JSONFormatter(logging.Formatter):
    """
    Structured JSON log formatter for production logging and observability.
    """
    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        if hasattr(record, "request_id"):
            log_obj["request_id"] = record.request_id
        if hasattr(record, "http"):
            log_obj["http"] = record.http
            
        return json.dumps(log_obj)

def setup_logging(is_production: bool = False):
    """
    Initializes structured JSON logging for standard stdout and uvicorn.
    """
    root = logging.getLogger()
    # Avoid duplicate handlers on hot reload
    root.handlers.clear()
    
    handler = logging.StreamHandler(sys.stdout)
    if is_production:
        handler.setFormatter(JSONFormatter())
    else:
        # Clear format for clean development console output
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        
    root.addHandler(handler)
    root.setLevel(logging.INFO)
    return root

class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that records structured timing and status for every request.
    """
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()
        logger = logging.getLogger("api.access")
        
        try:
            response = await call_next(request)
            duration_ms = round((time.time() - start_time) * 1000, 2)
            
            # Skip verbose logs for health checks to keep logs clean
            if not request.url.path.startswith("/health"):
                logger.info(
                    f"{request.method} {request.url.path} {response.status_code} in {duration_ms}ms",
                    extra={
                        "http": {
                            "method": request.method,
                            "path": request.url.path,
                            "status_code": response.status_code,
                            "duration_ms": duration_ms,
                            "client_ip": request.client.host if request.client else "unknown"
                        }
                    }
                )
            return response
        except Exception as exc:
            duration_ms = round((time.time() - start_time) * 1000, 2)
            logger.error(
                f"Unhandled exception during {request.method} {request.url.path}: {exc}",
                exc_info=True,
                extra={
                    "http": {
                        "method": request.method,
                        "path": request.url.path,
                        "duration_ms": duration_ms,
                        "client_ip": request.client.host if request.client else "unknown"
                    }
                }
            )
            raise exc
