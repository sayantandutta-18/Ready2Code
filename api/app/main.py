from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import health, problems, submissions, users, daily, notes, ai

# Ensure database tables exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ready2Code API",
    description="High-performance backend API for Ready2Code algorithmic learning platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(problems.router)
app.include_router(submissions.router)
app.include_router(users.router)
app.include_router(daily.router)
app.include_router(notes.router)
app.include_router(ai.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Ready2Code API",
        "docs": "/docs",
        "health": "/health"
    }
