import random
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..database import get_db
from ..models.entities import Problem, ProblemTag, ProblemTest, ProblemHint, Editorial, UserProblemStatus

router = APIRouter(prefix="/problems", tags=["problems"])

@router.get("")
def list_problems(
    topic: Optional[str] = None,
    difficulty: Optional[str] = None,
    company: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    user_id: Optional[str] = None,
    random_unsolved: bool = False,
    db: Session = Depends(get_db)
):
    query = db.query(Problem).filter(Problem.is_published == True)

    if topic and topic.lower() != "all":
        query = query.filter(Problem.topic.has(slug=topic.lower()) | (Problem.topic_id == topic))

    if difficulty and difficulty.lower() != "all":
        query = query.filter(Problem.difficulty == difficulty.lower())

    if search:
        search_filter = f"%{search.strip().lower()}%"
        query = query.filter(
            or_(
                Problem.title.ilike(search_filter),
                Problem.slug.ilike(search_filter)
            )
        )

    if company:
        query = query.filter(Problem.tags.any(tag=company))

    problems = query.all()

    # User problem status mapping
    user_status_map = {}
    if user_id:
        statuses = db.query(UserProblemStatus).filter(UserProblemStatus.user_id == user_id).all()
        user_status_map = {s.problem_id: s.status for s in statuses}

    results = []
    unsolved_candidates = []

    for p in problems:
        p_status = user_status_map.get(p.id, "todo")
        if status and status.lower() != "all":
            if p_status != status.lower():
                continue

        item = {
            "id": p.id,
            "slug": p.slug,
            "title": p.title,
            "difficulty": p.difficulty,
            "topic": p.topic.name if p.topic else "General",
            "tags": [t.tag for t in p.tags],
            "status": p_status,
            "acceptance_rate": 68.5, # Default benchmark
            "time_limit_ms": p.time_limit_ms,
            "memory_limit_mb": p.memory_limit_mb
        }
        results.append(item)
        if p_status != "solved":
            unsolved_candidates.append(item)

    if random_unsolved:
        target_list = unsolved_candidates if unsolved_candidates else results
        if target_list:
            return {"random_problem": random.choice(target_list)}
        raise HTTPException(status_code=404, detail="No problems found")

    return results

@router.get("/{slug}")
def get_problem(slug: str, user_id: Optional[str] = None, db: Session = Depends(get_db)):
    p = db.query(Problem).filter(Problem.slug == slug).first()
    if not p:
        raise HTTPException(status_code=404, detail="Problem not found")

    user_status = "todo"
    if user_id:
        status_rec = db.query(UserProblemStatus).filter(
            UserProblemStatus.user_id == user_id,
            UserProblemStatus.problem_id == p.id
        ).first()
        if status_rec:
            user_status = status_rec.status

    sample_tests = [
        {
            "id": t.id,
            "input_text": t.input_text,
            "expected_output": t.expected_output,
            "order_index": t.order_index
        }
        for t in p.tests if not t.is_hidden
    ]

    hints = [
        {
            "id": h.id,
            "level": h.level,
            "text": h.text,
            "xp_cost": h.xp_cost
        }
        for h in sorted(p.hints, key=lambda x: x.level)
    ]

    editorial = None
    if p.editorial:
        editorial = {
            "body_md": p.editorial.body_md,
            "approach": p.editorial.approach,
            "complexity_time": p.editorial.complexity_time,
            "complexity_space": p.editorial.complexity_space
        }

    return {
        "id": p.id,
        "slug": p.slug,
        "title": p.title,
        "difficulty": p.difficulty,
        "topic": p.topic.name if p.topic else "General",
        "tags": [t.tag for t in p.tags],
        "statement_md": p.statement_md,
        "time_limit_ms": p.time_limit_ms,
        "memory_limit_mb": p.memory_limit_mb,
        "sample_tests": sample_tests,
        "hints": hints,
        "editorial": editorial,
        "user_status": user_status
    }
