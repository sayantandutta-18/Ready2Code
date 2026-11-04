from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.entities import StudyPlan, PlanDay, Problem, UserProblemStatus

router = APIRouter(prefix="/plans", tags=["plans"])

@router.get("")
def list_plans(db: Session = Depends(get_db)):
    plans = db.query(StudyPlan).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "duration_days": p.duration_days,
            "total_problems": len(p.days)
        }
        for p in plans
    ]

@router.get("/{plan_id}")
def get_plan(plan_id: str, current_day: int = 1, user_id: str = "guest", db: Session = Depends(get_db)):
    p = db.query(StudyPlan).filter(
        (StudyPlan.id == plan_id) | (StudyPlan.name.ilike(f"%{plan_id}%"))
    ).first()
    if not p:
        raise HTTPException(status_code=404, detail="Study plan not found")

    user_solved_ids = set()
    statuses = db.query(UserProblemStatus).filter(
        UserProblemStatus.user_id == user_id,
        UserProblemStatus.status == "solved"
    ).all()
    user_solved_ids = {s.problem_id for s in statuses}

    # Group problems by day number
    days_map = {}
    for d in p.days:
        if d.day_number not in days_map:
            days_map[d.day_number] = []
        if d.problem:
            days_map[d.day_number].append({
                "id": d.problem.id,
                "slug": d.problem.slug,
                "title": d.problem.title,
                "difficulty": d.problem.difficulty,
                "topic": d.problem.topic.name if d.problem.topic else "General",
                "solved": d.problem.id in user_solved_ids
            })

    days_list = []
    for day_num in range(1, p.duration_days + 1):
        day_probs = days_map.get(day_num, [])
        is_unlocked = day_num <= current_day
        is_completed = len(day_probs) > 0 and all(x["solved"] for x in day_probs)
        days_list.append({
            "day_number": day_num,
            "problems": day_probs,
            "unlocked": is_unlocked,
            "completed": is_completed
        })

    return {
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "duration_days": p.duration_days,
        "current_day": current_day,
        "days": days_list
    }
