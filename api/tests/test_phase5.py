import os
import sys
import pytest
from pydantic import ValidationError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import SessionLocal
from app.config import settings
from app.routers.health import health_check
from app.routers.daily import get_daily_problem
from app.routers.companies import list_companies, get_company
from app.routers.interviews import list_interviews, create_interview, CreateInterviewRequest, InterviewRound
from app.routers.jobs import list_jobs, apply_for_job, JobApplicationRequest
from app.routers.ai import (
    get_socratic_hint, review_code, explain_verdict,
    HintRequest, ReviewRequest, ExplainVerdictRequest
)
from app.routers.submissions import RunRequest, SubmitRequest
from app.rate_limiter import check_rate_limit
from fastapi import HTTPException

def test_health_comprehensive():
    db = SessionLocal()
    try:
        res = health_check(db)
        assert "status" in res
        assert "postgres" in res
        assert "redis" in res
        assert "judge0" in res
        assert res["postgres"] == "up"
        assert res["environment"] is not None
    finally:
        db.close()

def test_daily_problem_endpoint():
    db = SessionLocal()
    try:
        res = get_daily_problem(user_id="algo_ninja", db=db)
        assert "date" in res
        assert "problem" in res
        assert "slug" in res["problem"]
        assert "streak" in res
        assert "freezes_left" in res
    finally:
        db.close()

def test_companies_endpoints():
    companies = list_companies()
    assert len(companies) >= 3
    first_slug = companies[0]["slug"]
    
    detail = get_company(first_slug)
    assert detail["slug"] == first_slug
    assert "schedule" in detail
    assert len(detail["schedule"]) > 0

def test_interviews_endpoints():
    interviews = list_interviews()
    assert isinstance(interviews, list)
    
    new_req = CreateInterviewRequest(
        author="candidate_test",
        company="Uber",
        role="Backend Engineer",
        date="November 2026",
        verdict="Offer",
        ctc="₹42 LPA",
        difficulty="Hard",
        rounds=[
            InterviewRound(name="Round 1", desc="Find shortest path in weighted graph")
        ],
        advice="Focus on space complexity and edge cases."
    )
    res = create_interview(new_req)
    assert res["status"] == "created"
    assert "interview" in res
    assert "id" in res["interview"]

def test_jobs_endpoints():
    jobs = list_jobs()
    assert len(jobs) >= 3
    job_id = jobs[0]["id"]
    
    app_req = JobApplicationRequest(
        user_id="test_user_id",
        username="top_coder",
        elo=1700,
        certificate_code="CERT-DSA-1234"
    )
    apply_res = apply_for_job(job_id, app_req)
    assert apply_res["status"] == "success"
    assert "application" in apply_res

def test_ai_endpoints():
    db = SessionLocal()
    try:
        # 1. Socratic Hint
        hint_req = HintRequest(
            problem_id="two-sum",
            user_code="def two_sum(nums, target): pass",
            level=1
        )
        hint_res = get_socratic_hint(hint_req, db=db)
        assert hint_res["level"] == 1
        assert "hint" in hint_res
        assert "socratic_question" in hint_res

        # 2. Code Review
        review_req = ReviewRequest(
            problem_id="two-sum",
            code="for i in range(len(nums)):\n  for j in range(i+1, len(nums)):\n    pass"
        )
        rev_res = review_code(review_req, db=db)
        assert rev_res["time_complexity"] == "O(n²)"
        assert "suggestion" in rev_res

        # 3. Explain Verdict
        exp_req = ExplainVerdictRequest(
            input_text="[2,7,11,15], 9",
            expected_output="[0,1]",
            actual_output="[]",
            verdict="WA"
        )
        exp_res = explain_verdict(exp_req)
        assert "explanation" in exp_res
    finally:
        db.close()

def test_input_length_limits():
    # Attempting to create SubmitRequest with > 65536 characters must raise ValidationError
    oversized_code = "x = 1\n" * 15000 # ~90,000 chars
    with pytest.raises(ValidationError):
        SubmitRequest(
            problem_id="two-sum",
            language="python",
            code=oversized_code
        )

def test_rate_limiter_logic():
    # Sliding window test: 3 requests per 10 seconds
    key = "unit_test_key"
    check_rate_limit(key, max_requests=3, window_seconds=10)
    check_rate_limit(key, max_requests=3, window_seconds=10)
    check_rate_limit(key, max_requests=3, window_seconds=10)
    
    # 4th request must exceed limit
    with pytest.raises(HTTPException) as exc_info:
        check_rate_limit(key, max_requests=3, window_seconds=10)
    assert exc_info.value.status_code == 429
