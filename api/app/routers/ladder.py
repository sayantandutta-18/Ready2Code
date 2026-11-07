from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.entities import Problem, UserLadder, LadderStage, User

router = APIRouter(prefix="/ladder", tags=["ladder"])

class StageSubmitRequest(BaseModel):
    user_id: str = "guest"
    problem_slug: str
    stage: str # brute, better, optimal
    runtime_ms: int

LADDER_STAGES_INFO = {
    "two-sum": {
        "brute": {
            "title": "Stage 1: Brute Force",
            "time_complexity": "O(n²)",
            "space_complexity": "O(1)",
            "hint": "Check every possible pair (i, j) with nested loops.",
            "max_runtime_ms": 250
        },
        "better": {
            "title": "Stage 2: Sort and Two Pointers",
            "time_complexity": "O(n log n)",
            "space_complexity": "O(n)",
            "hint": "Sort array while preserving original indices, then converge two pointers inwards.",
            "max_runtime_ms": 70
        },
        "optimal": {
            "title": "Stage 3: Hash Map Lookup",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "hint": "Single pass over array checking if complement (target - x) exists in dictionary.",
            "max_runtime_ms": 25
        }
    }
}

@router.get("/{problem_slug}")
def get_ladder(problem_slug: str, user_id: str = "guest", db: Session = Depends(get_db)):
    prob = db.query(Problem).filter(Problem.slug == problem_slug).first()
    if not prob:
        raise HTTPException(status_code=404, detail="Problem not found")

    stages_data = LADDER_STAGES_INFO.get(problem_slug, LADDER_STAGES_INFO["two-sum"])

    user_prog = db.query(UserLadder).filter(
        UserLadder.user_id == user_id,
        UserLadder.problem_id == prob.id
    ).first()

    current_stage = user_prog.stage_reached if user_prog else "brute"
    stage_order = ["brute", "better", "optimal", "mastered"]
    curr_idx = stage_order.index(current_stage)

    stages = []
    for s_key in ["brute", "better", "optimal"]:
        info = stages_data[s_key]
        s_idx = stage_order.index(s_key)
        unlocked = s_idx <= curr_idx
        completed = s_idx < curr_idx

        stages.append({
            "stage": s_key,
            "title": info["title"],
            "time_complexity": info["time_complexity"],
            "space_complexity": info["space_complexity"],
            "hint": info["hint"],
            "unlocked": unlocked,
            "completed": completed
        })

    return {
        "problem_slug": problem_slug,
        "problem_title": prob.title,
        "current_stage": current_stage,
        "stages": stages
    }

@router.post("/stage")
def submit_stage(req: StageSubmitRequest, db: Session = Depends(get_db)):
    prob = db.query(Problem).filter(Problem.slug == req.problem_slug).first()
    if not prob:
        raise HTTPException(status_code=404, detail="Problem not found")

    stages_data = LADDER_STAGES_INFO.get(req.problem_slug, LADDER_STAGES_INFO["two-sum"])
    stage_info = stages_data.get(req.stage)
    if not stage_info:
        raise HTTPException(status_code=400, detail="Invalid stage")

    # Enforce runtime threshold
    if req.runtime_ms > stage_info["max_runtime_ms"]:
        return {
            "passed": False,
            "message": f"Runtime {req.runtime_ms} ms exceeded {req.stage} threshold of {stage_info['max_runtime_ms']} ms. Optimize your algorithm further."
        }

    user_prog = db.query(UserLadder).filter(
        UserLadder.user_id == req.user_id,
        UserLadder.problem_id == prob.id
    ).first()

    next_map = {"brute": "better", "better": "optimal", "optimal": "mastered"}
    next_stage = next_map.get(req.stage, "mastered")

    if not user_prog:
        user_record = db.query(User).filter(User.id == req.user_id).first()
        if not user_record:
            db.add(User(id=req.user_id, username=req.user_id, display_name=req.user_id))
            db.commit()
        user_prog = UserLadder(user_id=req.user_id, problem_id=prob.id, stage_reached=next_stage)
        db.add(user_prog)
    else:
        user_prog.stage_reached = next_stage

    db.commit()

    return {
        "passed": True,
        "message": f"Congratulations! {stage_info['title']} accepted. Next stage unlocked!",
        "stage_reached": next_stage
    }
