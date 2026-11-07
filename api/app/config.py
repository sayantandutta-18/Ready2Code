import os
from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Priority 1: api/.env, Priority 2: root .env
for _p in [
    os.path.join(os.path.dirname(__file__), "..", ".env"),
    os.path.join(os.getcwd(), "api", ".env"),
    os.path.join(os.getcwd(), ".env"),
]:
    if os.path.exists(_p):
        load_dotenv(_p, override=True)
        break

class Settings(BaseModel):
    ENVIRONMENT: str = Field(default_factory=lambda: os.getenv("ENVIRONMENT", "development"))
    DEBUG: bool = Field(default_factory=lambda: os.getenv("DEBUG", "false").lower() in ("true", "1", "yes"))
    
    # Database
    DATABASE_URL: str = Field(default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///./ready2code.db"))
    
    # Redis
    REDIS_URL: str = Field(default_factory=lambda: os.getenv("REDIS_URL", "redis://localhost:6379/0"))
    REDIS_HOST: str = Field(default_factory=lambda: os.getenv("REDIS_HOST", "localhost"))
    REDIS_PORT: int = Field(default_factory=lambda: int(os.getenv("REDIS_PORT", "6379")))
    REDIS_PASSWORD: str = Field(default_factory=lambda: os.getenv("REDIS_PASSWORD", ""))
    
    # Judge0
    JUDGE0_URL: str = Field(default_factory=lambda: os.getenv("JUDGE0_URL", "http://localhost:2358"))
    
    # JWT & Security
    JWT_SECRET: str = Field(default_factory=lambda: os.getenv("JWT_SECRET", "ready2code-super-secret-jwt-key-change-in-prod-2026"))
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_DAYS: int = 7
    DEV_DEMO_LOGIN: bool = Field(default_factory=lambda: os.getenv("DEV_DEMO_LOGIN", "true").lower() in ("true", "1", "yes"))
    
    # CORS
    CORS_ORIGINS: List[str] = Field(default_factory=lambda: [
        origin.strip() for origin in os.getenv(
            "CORS_ORIGINS", 
            "http://localhost:3000,http://127.0.0.1:3000,https://ready2code.vercel.app"
        ).split(",") if origin.strip()
    ])
    
    # Rate Limiting
    ENABLE_RATE_LIMITING: bool = Field(default_factory=lambda: os.getenv("ENABLE_RATE_LIMITING", "true").lower() in ("true", "1", "yes"))
    RATE_LIMIT_PER_MINUTE: int = Field(default_factory=lambda: int(os.getenv("RATE_LIMIT_PER_MINUTE", "120")))
    SUBMISSION_RATE_LIMIT_PER_MINUTE: int = Field(default_factory=lambda: int(os.getenv("SUBMISSION_RATE_LIMIT_PER_MINUTE", "15")))
    AI_RATE_LIMIT_PER_MINUTE: int = Field(default_factory=lambda: int(os.getenv("AI_RATE_LIMIT_PER_MINUTE", "10")))
    
    # Input Constraints
    MAX_CODE_LENGTH: int = 65536
    MAX_TITLE_LENGTH: int = 250
    MAX_CONTENT_LENGTH: int = 15000
    
    # Monitoring
    SENTRY_DSN: str = Field(default_factory=lambda: os.getenv("SENTRY_DSN", ""))
    
    # Third party integrations
    GEMINI_API_KEY: str = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))

settings = Settings()
