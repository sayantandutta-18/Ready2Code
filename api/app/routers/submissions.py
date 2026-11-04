import re
import json
from datetime import datetime, date, timezone
from typing import Optional, List
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models.entities import (
    Problem, ProblemTest, Submission, UserProblemStatus,
    Streak, XPLedger, User
)
from ..judge.client import run_code, LANGUAGE_MAP, map_status_id

router = APIRouter(prefix="/submissions", tags=["submissions"])

class RunRequest(BaseModel):
    problem_id: str
    language: str
    code: str

class SubmitRequest(BaseModel):
    user_id: Optional[str] = "guest"
    problem_id: str
    language: str
    code: str

def build_executable_source(code: str, language: str, input_str: str) -> str:
    """
    Wraps user code with harness to handle both direct stdin/stdout and standard function signatures.
    """
    lang = language.lower()
    if "python" in lang:
        harness = f"""
import sys, json

# User code starts
{code}
# User code ends

_raw_input = {repr(input_str)}.strip().split('\\n')
_parsed_args = []
for line in _raw_input:
    line = line.strip()
    if not line:
        continue
    try:
        _parsed_args.append(json.loads(line))
    except Exception:
        try:
            _parsed_args.append(eval(line))
        except Exception:
            _parsed_args.append(line)

# Auto call first defined user function if not calling explicitly
_func_candidates = [v for k, v in list(locals().items()) if callable(v) and not k.startswith('_')]
if _func_candidates:
    target_fn = _func_candidates[-1]
    try:
        res = target_fn(*_parsed_args)
        if res is True:
            print("true")
        elif res is False:
            print("false")
        elif isinstance(res, (dict, list)):
            print(json.dumps(res))
        else:
            print(res)
    except Exception as e:
        sys.stderr.write(str(e))
        sys.exit(1)
"""
        return harness

    elif "javascript" in lang or "node" in lang:
        harness = f"""
const fs = require('fs');

{code}

const rawInput = {json.dumps(input_str)}.trim().split('\\n');
const parsedArgs = rawInput.filter(Boolean).map(line => {{
    try {{ return JSON.parse(line); }} catch(e) {{ return line; }}
}});

const fnNames = Object.keys(global).filter(k => typeof global[k] === 'function');
"""
        return harness

    return code

def normalize_output(val: str) -> str:
    return val.strip().replace(" ", "").replace("\r\n", "\n").lower()

@router.post("/run")
def run_sample_tests(req: RunRequest, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(
        (Problem.id == req.problem_id) | (Problem.slug == req.problem_id)
    ).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    sample_tests = [t for t in problem.tests if not t.is_hidden]
    lang_id = LANGUAGE_MAP.get(req.language.lower(), 71)

    results = []
    overall_status = "Accepted"

    for idx, test in enumerate(sample_tests):
        source = build_executable_source(req.code, req.language, test.input_text)
        exec_res = run_code(
            language_id=lang_id,
            source=source,
            stdin=test.input_text,
            timeout_s=max(1.0, problem.time_limit_ms / 1000.0)
        )

        status_info = exec_res["status"]
        verdict = map_status_id(status_info.get("id", 3))

        actual_out = (exec_res.get("stdout") or "").strip()
        expected_out = test.expected_output.strip()

        passed = False
        if verdict == "AC":
            if normalize_output(actual_out) == normalize_output(expected_out):
                passed = True
            else:
                verdict = "WA"
                status_info = {"id": 4, "description": "Wrong Answer"}

        if not passed and overall_status == "Accepted":
            overall_status = status_info.get("description", "Wrong Answer")

        results.append({
            "test_index": idx + 1,
            "input": test.input_text,
            "expected_output": expected_out,
            "actual_output": actual_out,
            "stderr": exec_res.get("stderr", ""),
            "verdict": verdict,
            "status_description": status_info.get("description", "Accepted"),
            "runtime_ms": int(float(exec_res.get("time", "0.01")) * 1000),
            "passed": passed
        })

    return {
        "overall_status": overall_status,
        "results": results
    }

@router.post("")
def submit_solution(req: SubmitRequest, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(
        (Problem.id == req.problem_id) | (Problem.slug == req.problem_id)
    ).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    all_tests = problem.tests
    lang_id = LANGUAGE_MAP.get(req.language.lower(), 71)

    total_time_ms = 0
    max_memory_kb = 12000
    final_verdict = "AC"
    failed_test_index = None

    for idx, test in enumerate(all_tests):
        source = build_executable_source(req.code, req.language, test.input_text)
        exec_res = run_code(
            language_id=lang_id,
            source=source,
            stdin=test.input_text,
            timeout_s=max(1.0, problem.time_limit_ms / 1000.0)
        )

        v = map_status_id(exec_res["status"].get("id", 3))
        runtime = int(float(exec_res.get("time", "0.01")) * 1000)
        total_time_ms += runtime
        max_memory_kb = max(max_memory_kb, exec_res.get("memory", 12000))

        actual_out = (exec_res.get("stdout") or "").strip()
        expected_out = test.expected_output.strip()

        if v != "AC":
            final_verdict = v
            failed_test_index = idx + 1
            break
        elif normalize_output(actual_out) != normalize_output(expected_out):
            final_verdict = "WA"
            failed_test_index = idx + 1
            break

    # Runtime percentiles against past AC submissions
    faster_than_pct = 85.0
    memory_than_pct = 78.0

    past_ac = db.query(Submission).filter(
        Submission.problem_id == problem.id,
        Submission.verdict == "AC",
        Submission.language == req.language
    ).all()

    if past_ac:
        slower = sum(1 for s in past_ac if s.runtime_ms >= total_time_ms)
        faster_than_pct = max(5.0, round((slower / len(past_ac)) * 100, 1))

    # Ensure a user exists for tracking (guest or logged-in)
    user_id = req.user_id or "guest"
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        user = User(id=user_id, username=f"coder_{user_id[:6]}", display_name="Coder")
        db.add(user)
        db.commit()

    # Save submission
    sub = Submission(
        user_id=user.id,
        problem_id=problem.id,
        language=req.language,
        code=req.code,
        verdict=final_verdict,
        runtime_ms=total_time_ms,
        memory_kb=max_memory_kb,
        failed_test_index=failed_test_index
    )
    db.add(sub)

    # Update user status & awards if AC
    first_time_solve = False
    xp_awarded = 0
    if final_verdict == "AC":
        status_rec = db.query(UserProblemStatus).filter(
            UserProblemStatus.user_id == user.id,
            UserProblemStatus.problem_id == problem.id
        ).first()

        if not status_rec:
            first_time_solve = True
            status_rec = UserProblemStatus(
                user_id=user.id,
                problem_id=problem.id,
                status="solved",
                best_runtime_ms=total_time_ms,
                solved_at=datetime.now(timezone.utc)
            )
            db.add(status_rec)
        else:
            if status_rec.status != "solved":
                first_time_solve = True
            status_rec.status = "solved"
            if not status_rec.best_runtime_ms or total_time_ms < status_rec.best_runtime_ms:
                status_rec.best_runtime_ms = total_time_ms

        if first_time_solve:
            xp_map = {"easy": 10, "medium": 25, "hard": 50}
            xp_awarded = xp_map.get(problem.difficulty.lower(), 10)
            db.add(XPLedger(
                user_id=user.id,
                amount=xp_awarded,
                reason=f"Solved {problem.title}",
                ref_id=problem.id
            ))

        # Update streak
        today_str = date.today().isoformat()
        streak = db.query(Streak).filter(Streak.user_id == user.id).first()
        if not streak:
            streak = Streak(user_id=user.id, current_streak=1, longest_streak=1, last_active_date=today_str)
            db.add(streak)
        elif streak.last_active_date != today_str:
            streak.current_streak += 1
            if streak.current_streak > streak.longest_streak:
                streak.longest_streak = streak.current_streak
            streak.last_active_date = today_str

    db.commit()

    return {
        "id": sub.id,
        "verdict": final_verdict,
        "runtime_ms": total_time_ms,
        "memory_kb": max_memory_kb,
        "runtime_percentile": faster_than_pct,
        "memory_percentile": memory_than_pct,
        "failed_test_index": failed_test_index,
        "first_time_solve": first_time_solve,
        "xp_awarded": xp_awarded,
        "total_tests": len(all_tests)
    }

@router.get("")
def list_submissions(problem_id: Optional[str] = None, user_id: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Submission)
    if problem_id:
        q = q.filter(Submission.problem_id == problem_id)
    if user_id:
        q = q.filter(Submission.user_id == user_id)
    subs = q.order_by(Submission.created_at.desc()).limit(20).all()

    return [
        {
            "id": s.id,
            "problem_id": s.problem_id,
            "language": s.language,
            "verdict": s.verdict,
            "runtime_ms": s.runtime_ms,
            "memory_kb": s.memory_kb,
            "created_at": s.created_at.isoformat()
        }
        for s in subs
    ]
