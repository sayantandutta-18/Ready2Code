import random
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..database import get_db
from ..models.entities import Problem, ProblemTag, ProblemTest, ProblemHint, Editorial, UserProblemStatus, User, Topic
from ..auth_deps import get_current_user_optional

router = APIRouter(prefix="/problems", tags=["problems"])

@router.get("")
def list_problems(
    topic: Optional[str] = None,
    difficulty: Optional[str] = None,
    company: Optional[str] = None,
    tag: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = "id",
    sort_order: Optional[str] = "asc",
    page: Optional[int] = None,
    limit: Optional[int] = 25,
    user_id: Optional[str] = None,
    random_unsolved: bool = False,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    query = db.query(Problem).filter(Problem.is_published == True)

    if topic and topic.lower() != "all":
        t_clean = topic.strip().lower()
        t_first = t_clean.split()[0] if t_clean else ""
        query = query.filter(
            Problem.topic.has(Topic.slug == t_clean) |
            Problem.topic.has(Topic.slug == t_first) |
            Problem.topic.has(Topic.name.ilike(f"%{t_clean}%")) |
            Problem.topic.has(Topic.name.ilike(f"%{t_first}%")) |
            (Problem.topic_id == topic)
        )

    if difficulty and difficulty.lower() != "all":
        query = query.filter(Problem.difficulty == difficulty.lower())

    if search:
        search_filter = f"%{search.strip().lower()}%"
        query = query.filter(
            or_(
                Problem.title.ilike(search_filter),
                Problem.slug.ilike(search_filter),
                Problem.tags.any(ProblemTag.tag.ilike(search_filter))
            )
        )

    if company and company.lower() != "all":
        query = query.filter(Problem.tags.any(ProblemTag.tag.ilike(f"%{company}%")))

    if tag and tag.lower() != "all":
        query = query.filter(Problem.tags.any(ProblemTag.tag.ilike(f"%{tag}%")))

    problems = query.all()

    # User problem status and best runtime mapping
    user_obj = current_user if isinstance(current_user, User) else None
    eff_user_id = user_obj.id if user_obj else (user_id if user_id and user_id.lower() != "guest" else None)
    user_status_map: Dict[str, Dict[str, Any]] = {}
    if eff_user_id:
        statuses = db.query(UserProblemStatus).filter(UserProblemStatus.user_id == eff_user_id).all()
        user_status_map = {
            s.problem_id: {
                "status": s.status,
                "best_runtime_ms": s.best_runtime_ms
            }
            for s in statuses
        }

    results = []
    unsolved_candidates = []

    for p in problems:
        p_info = user_status_map.get(p.id, {"status": "todo", "best_runtime_ms": None})
        p_status = p_info["status"]
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
            "best_runtime_ms": p_info.get("best_runtime_ms"),
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

    # Sorting
    diff_rank = {"easy": 1, "medium": 2, "hard": 3}
    status_rank = {"solved": 1, "attempted": 2, "todo": 3}
    reverse = (sort_order or "asc").lower() == "desc"

    sort_field = (sort_by or "id").lower()
    if sort_field == "title":
        results.sort(key=lambda x: x["title"].lower(), reverse=reverse)
    elif sort_field == "difficulty":
        results.sort(key=lambda x: diff_rank.get(x["difficulty"], 99), reverse=reverse)
    elif sort_field == "topic":
        results.sort(key=lambda x: x["topic"].lower(), reverse=reverse)
    elif sort_field == "status":
        results.sort(key=lambda x: status_rank.get(x["status"], 99), reverse=reverse)
    elif sort_field == "acceptance":
        results.sort(key=lambda x: x["acceptance_rate"], reverse=reverse)
    elif sort_field == "runtime":
        results.sort(key=lambda x: (x["best_runtime_ms"] is None, x["best_runtime_ms"] or 999999), reverse=reverse)

    # Server-side pagination
    if page is not None and page > 0:
        lim = limit or 25
        total_count = len(results)
        start_idx = (page - 1) * lim
        end_idx = start_idx + lim
        page_items = results[start_idx:end_idx]
        total_pages = max(1, (total_count + lim - 1) // lim)
        return {
            "items": page_items,
            "total": total_count,
            "page": page,
            "limit": lim,
            "total_pages": total_pages
        }

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
