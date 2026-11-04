from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import (
    health, auth, problems, submissions, users, daily, notes, ai,
    lists, plans, contests, discussions, analytics,
    patterns, ladder, placement, certificates, battles,
    companies, interviews, jobs
)

# Ensure database tables exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ready2Code API",
    description="High-performance backend API for Ready2Code algorithmic learning platform",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/")
def root():
    return {
        "message": "Welcome to Ready2Code API",
        "docs": "/docs",
        "health": "/health"
    }
