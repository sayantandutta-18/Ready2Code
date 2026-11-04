from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.entities import ProblemList, ListItem, Problem, UserProblemStatus

router = APIRouter(prefix="/lists", tags=["lists"])

class CreateListRequest(BaseModel):
    name: str
    description: Optional[str] = ""
    problem_slugs: Optional[List[str]] = []
    owner_id: Optional[str] = "guest"

class ReorderRequest(BaseModel):
    items: List[dict] # [{"problem_id": "...", "position": 0}]

@router.get("")
def get_lists(db: Session = Depends(get_db)):
    lists = db.query(ProblemList).all()
    res = []
    for l in lists:
        res.append({
            "id": l.id,
            "name": l.name,
            "description": l.description,
            "is_system": l.is_system,
            "visibility": l.visibility,
            "total_problems": len(l.items)
        })
    return res

@router.get("/{list_id}")
def get_list_detail(list_id: str, user_id: str = "guest", db: Session = Depends(get_db)):
    l = db.query(ProblemList).filter(
        (ProblemList.id == list_id) | (ProblemList.name.ilike(list_id))
    ).first()
    if not l:
        raise HTTPException(status_code=404, detail="List not found")

    user_solved_ids = set()
    statuses = db.query(UserProblemStatus).filter(
        UserProblemStatus.user_id == user_id,
        UserProblemStatus.status == "solved"
    ).all()
    user_solved_ids = {s.problem_id for s in statuses}

    problems = []
    for item in sorted(l.items, key=lambda x: x.position):
        p = item.problem
        if p:
            problems.append({
                "id": p.id,
                "slug": p.slug,
                "title": p.title,
                "difficulty": p.difficulty,
                "topic": p.topic.name if p.topic else "General",
                "position": item.position,
                "solved": p.id in user_solved_ids
            })

    solved_count = sum(1 for p in problems if p["solved"])

    return {
        "id": l.id,
        "name": l.name,
        "description": l.description,
        "is_system": l.is_system,
        "problems": problems,
        "total_problems": len(problems),
        "solved_count": solved_count,
        "progress_pct": round((solved_count / len(problems) * 100), 1) if problems else 0
    }

@router.post("")
def create_list(req: CreateListRequest, db: Session = Depends(get_db)):
    new_list = ProblemList(
        owner_id=req.owner_id,
        name=req.name,
        description=req.description,
        is_system=False,
        visibility="public"
    )
    db.add(new_list)
    db.commit()
    db.refresh(new_list)

    if req.problem_slugs:
        for idx, slug in enumerate(req.problem_slugs):
            prob = db.query(Problem).filter(Problem.slug == slug).first()
            if prob:
                db.add(ListItem(list_id=new_list.id, problem_id=prob.id, position=idx))
        db.commit()

    return {"status": "created", "id": new_list.id, "name": new_list.name}

@router.put("/{list_id}/reorder")
def reorder_list(list_id: str, req: ReorderRequest, db: Session = Depends(get_db)):
    for it in req.items:
        li = db.query(ListItem).filter(
            ListItem.list_id == list_id,
            ListItem.problem_id == it["problem_id"]
        ).first()
        if li:
            li.position = it["position"]
    db.commit()
    return {"status": "reordered"}
