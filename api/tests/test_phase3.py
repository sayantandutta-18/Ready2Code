import uuid
import pytest
from app.database import SessionLocal
from app.routers.auth import register, login, get_current_user_profile, AuthRequest
from app.routers.problems import list_problems
from app.routers.submissions import submit_solution, SubmitRequest
from app.routers.notes import save_note, get_note, NotePayload
from app.routers.users import toggle_bookmark, get_user_bookmarks, BookmarkRequest
from fastapi import HTTPException

def test_auth_registration_and_login():
    db = SessionLocal()
    try:
        uname = f"tester_{uuid.uuid4().hex[:8]}"
        # Register new user with explicit terms consent
        reg_req = AuthRequest(
            username=uname,
            display_name="Phase 3 Tester",
            timezone="America/New_York",
            terms_accepted=True,
            terms_version="2026-11-11"
        )
        reg_res = register(reg_req, db=db)
        assert "token" in reg_res
        assert reg_res["user"]["username"] == uname
        assert reg_res["user"]["timezone"] == "America/New_York"
        assert reg_res["user"]["streak"] == 0

        # Login existing user
        login_req = AuthRequest(username=uname)
        login_res = login(login_req, db=db)
        assert login_res["token"] == reg_res["token"]
        assert login_res["user"]["username"] == uname
    finally:
        db.close()

def test_registration_requires_terms_consent():
    db = SessionLocal()
    try:
        uname = f"noterms_{uuid.uuid4().hex[:8]}"
        reg_req = AuthRequest(username=uname, terms_accepted=False)
        with pytest.raises(HTTPException) as exc_info:
            register(reg_req, db=db)
        assert exc_info.value.status_code == 400
        assert "Affirmative consent" in exc_info.value.detail
    finally:
        db.close()

def test_user_account_deletion():
    db = SessionLocal()
    try:
        from app.routers.users import delete_user_account
        from app.models.entities import User

        uname = f"del_{uuid.uuid4().hex[:8]}"
        reg_req = AuthRequest(username=uname, terms_accepted=True)
        reg_res = register(reg_req, db=db)
        user_id = reg_res["user"]["id"]

        # Delete account
        del_res = delete_user_account(user_id=user_id, current_user=None, db=db)
        assert del_res["status"] == "ok"

        # Confirm user is deleted from DB
        deleted_user = db.query(User).filter(User.id == user_id).first()
        assert deleted_user is None
    finally:
        db.close()

def test_anonymous_write_rejection():
    db = SessionLocal()
    try:
        # Anonymous submit (no user_id or guest) must raise 401
        req = SubmitRequest(user_id="guest", problem_id="two-sum-sorted-offsets", language="python", code="def solve(): pass")
        with pytest.raises(HTTPException) as exc_info:
            submit_solution(req, current_user=None, db=db)
        assert exc_info.value.status_code == 401

        # Anonymous note save must raise 401
        note_req = NotePayload(problem_id="two-sum-sorted-offsets", body_md="my note", user_id="guest")
        with pytest.raises(HTTPException) as exc_info:
            save_note(note_req, current_user=None, db=db)
        assert exc_info.value.status_code == 401

        # Anonymous bookmark toggle must raise 401
        bm_req = BookmarkRequest(problem_id="two-sum-sorted-offsets")
        with pytest.raises(HTTPException) as exc_info:
            toggle_bookmark(bm_req, user_id="guest", current_user=None, db=db)
        assert exc_info.value.status_code == 401
    finally:
        db.close()

def test_problems_server_pagination_filtering_and_sorting():
    db = SessionLocal()
    try:
        # Test pagination (25 per page)
        page1 = list_problems(page=1, limit=25, db=db)
        assert isinstance(page1, dict)
        assert len(page1["items"]) == 25
        assert page1["total"] >= 60
        assert page1["page"] == 1
        assert page1["total_pages"] >= 3

        page2 = list_problems(page=2, limit=25, db=db)
        assert len(page2["items"]) == 25
        assert page2["page"] == 2

        # Test difficulty filtering
        easy_res = list_problems(difficulty="easy", page=1, limit=100, db=db)
        assert all(p["difficulty"] == "easy" for p in easy_res["items"])
        assert easy_res["total"] >= 25

        # Test topic filtering
        arr_res = list_problems(topic="Arrays and Hashing", page=1, limit=100, db=db)
        assert all("Array" in p["topic"] for p in arr_res["items"])
        assert arr_res["total"] >= 10

        # Test sorting by title ascending
        sorted_res = list_problems(sort_by="title", sort_order="asc", page=1, limit=25, db=db)
        titles = [p["title"] for p in sorted_res["items"]]
        assert titles == sorted(titles, key=lambda s: s.lower())
    finally:
        db.close()

def test_streak_and_progress_tracking_with_timezone():
    db = SessionLocal()
    try:
        uname = f"streak_{uuid.uuid4().hex[:8]}"
        reg_req = AuthRequest(username=uname, timezone="Asia/Kolkata")
        reg_res = register(reg_req, db=db)
        user_id = reg_res["user"]["id"]

        # Submit an accepted solution
        correct_code = """
def two_sum_sorted(numbers, target):
    l, r = 0, len(numbers) - 1
    while l < r:
        s = numbers[l] + numbers[r]
        if s == target: return [l + 1, r + 1]
        elif s < target: l += 1
        else: r -= 1
    return []
"""
        sub_req = SubmitRequest(user_id=user_id, problem_id="two-sum-sorted", language="python", code=correct_code)
        sub_res = submit_solution(sub_req, current_user=None, db=db)
        assert sub_res["verdict"] == "AC"

        # Verify streak updated to at least 1
        from app.models.entities import Streak, UserProblemStatus
        streak = db.query(Streak).filter(Streak.user_id == user_id).first()
        assert streak.current_streak >= 1

        # Verify progress status is "solved" with best_runtime_ms
        from app.models.entities import Problem
        prob = db.query(Problem).filter(Problem.slug == "two-sum-sorted").first()
        status = db.query(UserProblemStatus).filter(
            UserProblemStatus.user_id == user_id,
            UserProblemStatus.problem_id == prob.id
        ).first()
        assert status is not None
        assert status.status == "solved"
        assert status.best_runtime_ms is not None
    finally:
        db.close()

def test_notes_and_bookmarks_persistence():
    db = SessionLocal()
    try:
        user_id = f"test_user_{uuid.uuid4().hex[:8]}"
        # Save note
        save_res = save_note(
            NotePayload(problem_id="two-sum-sorted-offsets", body_md="Remember two pointers approach", user_id=user_id),
            db=db
        )
        assert save_res["status"] == "saved"

        # Get note
        note = get_note("two-sum-sorted-offsets", user_id=user_id, db=db)
        assert "two pointers" in note["body_md"]

        # Toggle bookmark
        bm_res = toggle_bookmark(
            BookmarkRequest(problem_id="two-sum-sorted-offsets"),
            user_id=user_id,
            db=db
        )
        assert bm_res["bookmarked"] is True

        # Check user bookmarks
        bms = get_user_bookmarks(problem_id="two-sum-sorted-offsets", user_id=user_id, db=db)
        assert bms["bookmarked"] is True
        assert len(bms["bookmarks"]) >= 1
    finally:
        db.close()
