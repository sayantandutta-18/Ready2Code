import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app.database import SessionLocal
from app.routers.health import health_check
from app.routers.problems import list_problems, get_problem
from app.routers.submissions import run_sample_tests, submit_solution, RunRequest, SubmitRequest
from app.judge.client import run_code
from scripts.seed import validate_problem_dict

def test_health_endpoint():
    db = SessionLocal()
    try:
        res = health_check(db)
        assert res["status"] in ("ok", "degraded")
        assert res["db"] is True
    finally:
        db.close()

def test_judge0_client_print_hello():
    res = run_code(71, 'print("hello")')
    assert res["status"]["id"] == 3
    assert "hello" in res["stdout"].strip()

def test_problems_list_and_detail():
    db = SessionLocal()
    try:
        problems = list_problems(db=db)
        assert len(problems) == 12
        first = problems[0]
        assert "slug" in first
        assert "tags" in first
        assert len(first["tags"]) > 0

        p = get_problem(first["slug"], db=db)
        assert len(p["sample_tests"]) > 0
        assert len(p["hints"]) > 0
        assert p["editorial"] is not None
    finally:
        db.close()

def test_problem_validator_rejects_missing_hidden_tests():
    invalid_dict = {
        "slug": "bad-problem",
        "title": "Bad",
        "difficulty": "easy",
        "statement_md": "broken",
        "sample_tests": [{"input_text": "1", "expected_output": "1"}],
        "hidden_tests": []
    }
    with pytest.raises(ValueError, match="must have at least one hidden test"):
        validate_problem_dict(invalid_dict, "bad.json")

def test_run_sample_tests_two_sum():
    correct_solution = """
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []
"""
    db = SessionLocal()
    try:
        req = RunRequest(problem_id="two-sum", language="python", code=correct_solution)
        data = run_sample_tests(req, db=db)
        assert data["overall_status"] == "Accepted"
        assert len(data["results"]) > 0
        assert all(r["passed"] for r in data["results"])
    finally:
        db.close()

def test_submit_two_sum_verdicts():
    correct_solution = """
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []
"""
    db = SessionLocal()
    try:
        req = SubmitRequest(user_id="test_user_1", problem_id="two-sum", language="python", code=correct_solution)
        data = submit_solution(req, db=db)
        assert data["verdict"] == "AC"
        assert data["runtime_percentile"] > 0
    finally:
        db.close()
