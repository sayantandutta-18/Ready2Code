import os
from datetime import datetime, timedelta, timezone
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..database import get_db
from ..models.entities import Contest, ContestProblem, ContestEntry, Rating, User, Problem

router = APIRouter(prefix="/contests", tags=["contests"])

class ContestSubmission(BaseModel):
    user_id: str
    problem_id: str
    verdict: str # AC, WA, TLE, RE

@router.get("")
def list_contests(db: Session = Depends(get_db)):
    contests = db.query(Contest).order_by(Contest.starts_at.desc()).all()
    now = datetime.now(timezone.utc)
    res = []
    for c in contests:
        starts_at = c.starts_at if c.starts_at.tzinfo else c.starts_at.replace(tzinfo=timezone.utc)
        end_time = starts_at + timedelta(minutes=c.duration_min)
        status = "upcoming"
        if starts_at <= now <= end_time:
            status = "live"
        elif now > end_time:
            status = "past"
        res.append({
            "id": c.id,
            "title": c.title,
            "starts_at": starts_at.isoformat(),
            "duration_min": c.duration_min,
            "type": c.type,
            "status": status,
            "total_problems": len(c.problems)
        })
    return res

@router.get("/{contest_id}")
def get_contest(contest_id: str, db: Session = Depends(get_db)):
    c = db.query(Contest).filter(Contest.id == contest_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Contest not found")

    problems = []
    for cp in sorted(c.problems, key=lambda x: x.position):
        p = cp.problem
        if p:
            problems.append({
                "id": p.id,
                "slug": p.slug,
                "title": p.title,
                "difficulty": p.difficulty,
                "points": cp.points,
                "position": cp.position
            })

    return {
        "id": c.id,
        "title": c.title,
        "starts_at": c.starts_at.isoformat(),
        "duration_min": c.duration_min,
        "type": c.type,
        "status": c.status,
        "problems": problems
    }

@router.get("/{contest_id}/standings")
def get_standings(contest_id: str, db: Session = Depends(get_db)):
    entries = db.query(ContestEntry).filter(
        ContestEntry.contest_id == contest_id
    ).order_by(desc(ContestEntry.score), ContestEntry.penalty_s.asc()).all()

    standings = []
    for idx, e in enumerate(entries):
        user = e.user
        standings.append({
            "rank": idx + 1,
            "user_id": e.user_id,
            "username": user.username if user else f"user_{e.user_id[:6]}",
            "score": e.score,
            "penalty_min": round(e.penalty_s / 60, 1),
            "finished_at": e.finished_at.isoformat() if e.finished_at else None
        })
    return standings

@router.post("/{contest_id}/submit")
def contest_submit(contest_id: str, req: ContestSubmission, db: Session = Depends(get_db)):
    entry = db.query(ContestEntry).filter(
        ContestEntry.contest_id == contest_id,
        ContestEntry.user_id == req.user_id
    ).first()

    if not entry:
        user_record = db.query(User).filter(User.id == req.user_id).first()
        if not user_record:
            db.add(User(id=req.user_id, username=req.user_id, display_name=req.user_id))
            db.commit()
        entry = ContestEntry(contest_id=contest_id, user_id=req.user_id, score=0, penalty_s=0)
        db.add(entry)

    cp = db.query(ContestProblem).filter(
        ContestProblem.contest_id == contest_id,
        ContestProblem.problem_id == req.problem_id
    ).first()
    pts = cp.points if cp else 100

    if req.verdict == "AC":
        entry.score += pts
        entry.finished_at = datetime.now(timezone.utc)
    else:
        # 5 minutes penalty per wrong submission before acceptance
        entry.penalty_s += 300

    db.commit()
    return {"status": "recorded", "score": entry.score, "penalty_s": entry.penalty_s}

@router.get("/ratings/{username}")
def get_user_ratings(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter((User.username == username) | (User.id == username)).first()
    if not user:
        return []
    ratings = db.query(Rating).filter(Rating.user_id == user.id).order_by(Rating.created_at.asc()).all()
    return [
        {
            "contest_id": r.contest_id,
            "rating_before": r.rating_before,
            "rating_after": r.rating_after,
            "rank": r.rank,
            "date": r.created_at.strftime("%b %d")
        }
        for r in ratings
    ]
