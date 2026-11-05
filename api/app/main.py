import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .logging_config import setup_logging, StructuredLoggingMiddleware
from .database import engine, Base
from .routers import (
    health, auth, problems, submissions, users, daily, notes, ai,
    lists, plans, contests, discussions, analytics,
    patterns, ladder, placement, certificates, battles,
    companies, interviews, jobs, topics
)

# Initialize structured logging
logger = setup_logging(is_production=(settings.ENVIRONMENT == "production"))

# Sentry Error Reporting Hook (Optional, disabled when DSN is empty)
if settings.SENTRY_DSN:
    try:
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            environment=settings.ENVIRONMENT,
            traces_sample_rate=0.2 if settings.ENVIRONMENT == "production" else 1.0,
            integrations=[FastApiIntegration()]
        )
        logger.info("Sentry monitoring initialized successfully")
    except ImportError:
        logger.warning("sentry-sdk not installed; error reporting hook disabled")
else:
    logger.info("Sentry DSN not provided; error reporting hook inactive")

# Ensure database tables exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ready2Code API",
    description="High-performance backend API for Ready2Code algorithmic learning platform",
    version="2.0.0",
    debug=settings.DEBUG
)

# Structured JSON logging middleware
app.add_middleware(StructuredLoggingMiddleware)

# Security: CORS Allowlist configuration
cors_origins = settings.CORS_ORIGINS if settings.CORS_ORIGINS else ["http://localhost:3000"]
# In development allow credentials with allow_origin_regex or defined origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins if settings.ENVIRONMENT == "production" else ["*"],
    allow_credentials=True if settings.ENVIRONMENT == "production" and "*" not in cors_origins else False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Security: Global exception handler preventing stack traces in production
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled server exception: %s", exc, exc_info=True)
    if settings.DEBUG:
        return JSONResponse(
            status_code=500,
            content={
                "detail": str(exc),
                "type": type(exc).__name__,
                "error": "InternalServerError"
            }
        )
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected internal server error occurred. Please try again later.",
            "error": "InternalServerError"
        }
    )

# Include API Routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(problems.router)
app.include_router(submissions.router)
app.include_router(users.router)
app.include_router(daily.router)
app.include_router(notes.router)
app.include_router(ai.router)
app.include_router(lists.router)
app.include_router(plans.router)
app.include_router(contests.router)
app.include_router(discussions.router)
app.include_router(analytics.router)
app.include_router(patterns.router)
app.include_router(ladder.router)
app.include_router(placement.router)
app.include_router(certificates.router)
app.include_router(battles.router)
app.include_router(companies.router)
app.include_router(interviews.router)
app.include_router(jobs.router)
app.include_router(topics.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Ready2Code API",
        "docs": "/docs",
        "health": "/health",
        "version": "2.0.0"
    }
