import hashlib
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.entities import DailyProblem, Problem, Streak

router = APIRouter(prefix="/daily", tags=["daily"])

@router.get("")
def get_daily_problem(user_id: str = "guest", db: Session = Depends(get_db)):
    today_str = date.today().isoformat()

    daily = db.query(DailyProblem).filter(DailyProblem.date == today_str).first()
    if not daily:
        # Deterministically select today's problem
        problems = db.query(Problem).filter(Problem.is_published == True).all()
        if not problems:
            raise HTTPException(status_code=404, detail="No problems published yet")

        # Hash date to integer index
        hash_val = int(hashlib.sha256(today_str.encode()).hexdigest(), 16)
        chosen = problems[hash_val % len(problems)]

        daily = DailyProblem(date=today_str, problem_id=chosen.id)
        db.add(daily)
        db.commit()
        db.refresh(daily)

    p = db.query(Problem).filter(Problem.id == daily.problem_id).first()

    # User streak information
    streak = db.query(Streak).filter(Streak.user_id == user_id).first()
    streak_count = streak.current_streak if streak else 0
    solved_today = (streak.last_active_date == today_str) if streak else False

    return {
        "date": today_str,
        "problem": {
            "id": p.id,
            "slug": p.slug,
            "title": p.title,
            "difficulty": p.difficulty,
            "topic": p.topic.name if p.topic else "General"
        },
        "streak": streak_count,
        "solved_today": solved_today,
        "freezes_left": streak.freezes_left if streak else 2
    }
