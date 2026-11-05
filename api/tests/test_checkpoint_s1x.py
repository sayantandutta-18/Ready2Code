import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import SessionLocal
from app.models.entities import Problem, Topic, ProblemTest
from app.routers.problems import list_problems, get_problem
from app.routers.topics import get_topics
from scripts.seed import seed_database

def test_seed_idempotency_and_counts():
    """
    Runs the seed twice and checks:
    - Exactly 100 problems loaded
    - Exactly 10 topics created in database
    - No duplicate slugs or rows
    - Second run loads 0 new rows and does not fail
    """
    # First execution
    new_first, total_first = seed_database()
    assert total_first == 100

    db = SessionLocal()
    try:
        # Check problem count
        problems = db.query(Problem).filter(Problem.is_published == True).all()
        assert len(problems) == 100

        slugs = [p.slug for p in problems]
        assert len(slugs) == len(set(slugs)), "Duplicate problem slugs found!"

        # Check topic count
        topics = db.query(Topic).all()
        assert len(topics) == 10, f"Expected 10 topics, got {len(topics)}"
        topic_names = [t.name for t in topics]
        assert len(topic_names) == len(set(topic_names)), "Duplicate topic names found!"
    finally:
        db.close()

    # Second execution (idempotency check)
    new_second, total_second = seed_database()
    assert new_second == 0, f"Expected 0 new problems on second run, got {new_second}"
    assert total_second == 100

    db = SessionLocal()
    try:
        problems_after = db.query(Problem).filter(Problem.is_published == True).all()
        assert len(problems_after) == 100
        topics_after = db.query(Topic).all()
        assert len(topics_after) == 10
    finally:
        db.close()

def test_no_hidden_tests_in_problems_api():
    """
    Verifies that neither GET /problems nor GET /problems/{slug} ever leaks
    hidden test inputs or outputs to the client.
    """
    db = SessionLocal()
    try:
        # 1. Check list_problems response
        paged_res = list_problems(page=1, limit=50, db=db)
        items = paged_res["items"] if isinstance(paged_res, dict) else paged_res
        assert len(items) > 0

        # Query all hidden test inputs from database to verify against
        hidden_tests = db.query(ProblemTest).filter(ProblemTest.is_hidden == True).all()
        hidden_inputs = {t.input_text.strip() for t in hidden_tests if t.input_text}
        hidden_outputs = {t.expected_output.strip() for t in hidden_tests if t.expected_output}

        for item in items:
            # list_problems must not contain tests at all
            assert "sample_tests" not in item
            assert "hidden_tests" not in item
            assert "tests" not in item

        # 2. Check get_problem detail response for several problems
        test_slugs = [items[0]["slug"], items[1]["slug"], "contains-duplicate", "binary-search"]
        for slug in test_slugs:
            detail = get_problem(slug, db=db)
            assert detail["slug"] == slug
            assert "sample_tests" in detail
            assert "hidden_tests" not in detail

            # None of the sample tests should be marked as hidden
            for st in detail["sample_tests"]:
                assert st.get("is_hidden", False) is False

            # Verify no hidden test for this problem leaked into sample_tests
            prob = db.query(Problem).filter(Problem.slug == slug).first()
            if prob:
                prob_hidden = [t for t in prob.tests if t.is_hidden]
                prob_hidden_inputs = {t.input_text.strip() for t in prob_hidden}
                prob_sample_inputs = {st["input_text"].strip() for st in detail["sample_tests"]}

                # If hidden inputs differ from sample inputs, ensure no leak
                for hi in prob_hidden_inputs:
                    assert hi not in prob_sample_inputs or len(prob_hidden) == 0

        # 3. Check topics endpoint returns 10 topics
        topics_res = get_topics(db=db)
        assert len(topics_res) == 10
        assert all("name" in t and "slug" in t for t in topics_res)

    finally:
        db.close()
