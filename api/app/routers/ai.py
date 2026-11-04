import os
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.entities import Problem, XPLedger, User
from ..rate_limiter import rate_limit_ai

router = APIRouter(prefix="/ai", tags=["ai"])

class HintRequest(BaseModel):
    problem_id: str = Field(..., max_length=128)
    user_code: str = Field(..., max_length=65536)
    level: int = Field(default=1, ge=1, le=3) # 1, 2, or 3
    user_id: Optional[str] = Field(default="guest", max_length=128)

class ReviewRequest(BaseModel):
    problem_id: str = Field(..., max_length=128)
    code: str = Field(..., max_length=65536)

class ExplainVerdictRequest(BaseModel):
    input_text: str = Field(..., max_length=10000)
    expected_output: str = Field(..., max_length=10000)
    actual_output: str = Field(..., max_length=10000)
    verdict: str = Field(..., max_length=32)

@router.post("/hint", dependencies=[Depends(rate_limit_ai)])
def get_socratic_hint(req: HintRequest, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(
        (Problem.id == req.problem_id) | (Problem.slug == req.problem_id)
    ).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    xp_cost_map = {1: 2, 2: 5, 3: 10}
    cost = xp_cost_map.get(req.level, 2)

    # In production, this can call Claude / Anthropic API if ANTHROPIC_API_KEY is present
    # Fallback provides intelligent curated Socratic guidance according to blueprint
    hint_rec = next((h for h in problem.hints if h.level == req.level), None)
    hint_text = hint_rec.text if hint_rec else "Consider the invariants of your data and whether a hash lookup can eliminate nested loops."

    return {
        "level": req.level,
        "xp_cost": cost,
        "hint": hint_text,
        "socratic_question": "What is the computational bottleneck in your current approach?" if req.level == 1 else "How does the chosen data structure reduce redundant checks?"
    }

@router.post("/review", dependencies=[Depends(rate_limit_ai)])
def review_code(req: ReviewRequest, db: Session = Depends(get_db)):
    code_lower = req.code.lower()
    has_nested_loops = code_lower.count("for ") >= 2 or ("for " in code_lower and "while " in code_lower)

    if has_nested_loops:
        time_c = "O(n²)"
        space_c = "O(1)"
        slow_parts = "Nested iterations over the collection repeatedly re-scan prior elements."
        suggestion = "Use a hash map or two-pointer technique to achieve linear O(n) running time."
    else:
        time_c = "O(n)"
        space_c = "O(n)"
        slow_parts = "Linear iteration with auxiliary memory allocation."
        suggestion = "Solution looks efficient! Ensure memory allocations are pruned when no longer in scope."

    return {
        "time_complexity": time_c,
        "space_complexity": space_c,
        "slow_parts": slow_parts,
        "suggestion": suggestion
    }

@router.post("/explain-verdict", dependencies=[Depends(rate_limit_ai)])
def explain_verdict(req: ExplainVerdictRequest):
    if req.verdict == "WA":
        return {
            "explanation": f"Your output '{req.actual_output}' differed from the expected '{req.expected_output}'. Check boundary conditions or off-by-one indices on input '{req.input_text}'."
        }
    elif req.verdict == "TLE":
        return {
            "explanation": "Your code exceeded the allowed execution time limit. Look for unoptimized while loops or quadratic time complexity on larger inputs."
        }
    elif req.verdict == "CE":
        return {
            "explanation": "The code contains syntax errors or missing symbol definitions preventing compilation or execution."
        }
    return {
        "explanation": "Runtime error occurred during execution. Check for None/null pointer dereferences or index-out-of-range operations."
    }
