import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app.database import SessionLocal
from app.routers.health import health_check
from app.routers.problems import list_problems, get_problem
from app.routers.submissions import run_sample_tests, submit_solution, RunRequest, SubmitRequest
from app.routers.lists import get_lists, get_list_detail
from app.routers.plans import list_plans, get_plan
from app.routers.contests import list_contests, get_standings, contest_submit, ContestSubmission
from app.routers.discussions import create_discussion, get_problem_discussions, CreateDiscussionRequest
from app.routers.analytics import get_analytics, get_review_queue, grade_review, GradeReviewRequest
from app.routers.patterns import list_patterns, get_pattern, submit_quiz, SubmitQuizRequest
from app.routers.ladder import get_ladder, submit_stage, StageSubmitRequest
from app.routers.certificates import issue_certificate, verify_certificate, SubmitSkillTestRequest
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

def test_lists_and_study_plans():
    db = SessionLocal()
    try:
        lists = get_lists(db=db)
        assert len(lists) >= 2
        blind75 = next((l for l in lists if "Blind" in l["name"]), None)
        assert blind75 is not None

        detail = get_list_detail(blind75["id"], db=db)
        assert len(detail["problems"]) > 0

        plans = list_plans(db=db)
        assert len(plans) >= 1
        bootcamp = get_plan(plans[0]["id"], current_day=1, db=db)
        assert len(bootcamp["days"]) == 30
        assert bootcamp["days"][0]["unlocked"] is True
    finally:
        db.close()

def test_contests_and_standings():
    import uuid
    db = SessionLocal()
    try:
        contests = list_contests(db=db)
        assert len(contests) >= 1
        c_id = contests[0]["id"]
        standings = get_standings(c_id, db=db)
        assert len(standings) >= 1
        # Submit contest wrong attempt
        test_uid = f"contest_user_{uuid.uuid4().hex[:6]}"
        res = contest_submit(c_id, ContestSubmission(user_id=test_uid, problem_id="two-sum", verdict="WA"), db=db)
        assert res["penalty_s"] == 300
    finally:
        db.close()

def test_discussions_and_solutions_gate():
    db = SessionLocal()
    try:
        req = CreateDiscussionRequest(
            problem_slug="two-sum",
            title="Clean Hash Map Solution",
            body_md="Here is an optimal O(n) solution in Python using a dictionary to track seen complements. " * 5,
            is_solution=True,
            author_id="author_123"
        )
        res = create_discussion(req, db=db)
        assert res["status"] == "created"

        discs = get_problem_discussions("two-sum", is_solution=True, db=db)
        assert len(discs) >= 1
    finally:
        db.close()

def test_analytics_and_review_queue():
    db = SessionLocal()
    try:
        analytics = get_analytics(db=db)
        assert len(analytics["weekly_solves"]) > 0
        assert len(analytics["topic_acceptance"]) > 0

        rq = get_review_queue("guest", db=db)
        assert "due_today" in rq

        p1_id = rq["due_today"][0]["problem_id"] if rq["due_today"] else "two-sum"
        grade_res = grade_review(GradeReviewRequest(user_id="guest", problem_id=p1_id, passed=True), db=db)
        assert grade_res["next_interval_days"] in (3, 7, 21)
    finally:
        db.close()

def test_patterns_and_ladder():
    patterns = list_patterns()
    assert len(patterns) >= 5
    first_p = get_pattern(patterns[0]["slug"])
    assert "template_code" in first_p

    quiz_res = submit_quiz(patterns[0]["slug"], SubmitQuizRequest(pattern_slug=patterns[0]["slug"], selected_option_index=0))
    assert quiz_res["correct"] is True

    db = SessionLocal()
    try:
        ladder = get_ladder("two-sum", db=db)
        assert len(ladder["stages"]) == 3
        stage_res = submit_stage(StageSubmitRequest(problem_slug="two-sum", stage="brute", runtime_ms=120), db=db)
        assert stage_res["passed"] is True
    finally:
        db.close()

def test_certificates_issue_and_verify():
    db = SessionLocal()
    try:
        issued = issue_certificate(SubmitSkillTestRequest(user_id="cert_tester", skill="Data Structures", score_pct=85), db=db)
        assert issued["verify_code"].startswith("R2C-")
        verified = verify_certificate(issued["verify_code"], db=db)
        assert verified["verified"] is True
        assert verified["skill"] == "Data Structures"
    finally:
        db.close()
