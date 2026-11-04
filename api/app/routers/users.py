import hashlib
from datetime import date
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.entities import User, Problem, UserProblemStatus, Streak, XPLedger, Bookmark, Note
from ..auth_deps import get_current_user_optional, get_current_user

router = APIRouter(prefix="/users", tags=["users"])

class UpdateProfileRequest(BaseModel):
    username: Optional[str] = None
    display_name: Optional[str] = None
    timezone: Optional[str] = None

class BookmarkRequest(BaseModel):
    problem_id: str

@router.get("/{username}")
def get_user_profile(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        # Check if username is an id
        user = db.query(User).filter(User.id == username).first()
    if not user:
        # Auto create if not found for seamless exploration
        user = User(
            id=username,
            username=username if len(username) <= 20 else f"coder_{username[:8]}",
            display_name=username.capitalize()
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    statuses = db.query(UserProblemStatus).filter(UserProblemStatus.user_id == user.id).all()
    solved_problem_ids = [s.problem_id for s in statuses if s.status == "solved"]

    solved_problems = db.query(Problem).filter(Problem.id.in_(solved_problem_ids)).all() if solved_problem_ids else []

    easy_count = sum(1 for p in solved_problems if p.difficulty == "easy")
    medium_count = sum(1 for p in solved_problems if p.difficulty == "medium")
    hard_count = sum(1 for p in solved_problems if p.difficulty == "hard")

    streak_rec = db.query(Streak).filter(Streak.user_id == user.id).first()
    streak_count = streak_rec.current_streak if streak_rec else 0
    longest_streak = streak_rec.longest_streak if streak_rec else 0

    xp_total = sum(x.amount for x in user.xp_entries) if user.xp_entries else 0

    # Skills breakdown by topic
    skills_map = {}
    for p in solved_problems:
        topic_name = p.topic.name if p.topic else "General"
        skills_map[topic_name] = skills_map.get(topic_name, 0) + 1

    return {
        "id": user.id,
        "username": user.username,
        "display_name": user.display_name or user.username,
        "avatar_url": user.avatar_url,
        "timezone": user.timezone,
        "solved": {
            "total": len(solved_problems),
            "easy": easy_count,
            "medium": medium_count,
            "hard": hard_count
        },
        "streak": {
            "current": streak_count,
            "longest": longest_streak,
            "freezes_left": streak_rec.freezes_left if streak_rec else 2
        },
        "xp": xp_total,
        "skills": skills_map
    }

@router.patch("/me")
def update_profile(req: UpdateProfileRequest, user_id: str = "guest", db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        user = User(id=user_id, username=f"coder_{user_id[:6]}")
        db.add(user)

    if req.username:
        clean = req.username.strip()
        if len(clean) < 3 or len(clean) > 20:
            raise HTTPException(status_code=400, detail="Username must be between 3 and 20 characters")
        if not clean.replace("_", "").isalnum():
            raise HTTPException(status_code=400, detail="Username can only contain alphanumeric and underscores")
        existing = db.query(User).filter(User.username == clean, User.id != user_id).first()
        if existing:
            raise HTTPException(status_code=409, detail="Username already taken")
        user.username = clean

    if req.display_name is not None:
        user.display_name = req.display_name
    if req.timezone is not None:
        user.timezone = req.timezone

    db.commit()
    return {"status": "ok", "username": user.username, "display_name": user.display_name}

@router.get("/me/bookmarks")
def get_user_bookmarks(
    problem_id: Optional[str] = None,
    user_id: Optional[str] = None,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    user_obj = current_user if isinstance(current_user, User) else None
    eff_user_id = (user_obj.id if user_obj else None) or (user_id if user_id and user_id.lower() != "guest" else None)
    if not eff_user_id:
        return {"bookmarked": False, "bookmarks": []}

    bookmarks = db.query(Bookmark).filter(Bookmark.user_id == eff_user_id).all()
    b_ids = [b.problem_id for b in bookmarks]

    is_bookmarked = False
    if problem_id:
        # Check by id or slug
        prob = db.query(Problem).filter((Problem.id == problem_id) | (Problem.slug == problem_id)).first()
        target_id = prob.id if prob else problem_id
        is_bookmarked = target_id in b_ids

    problems = db.query(Problem).filter(Problem.id.in_(b_ids)).all() if b_ids else []
    items = [{"id": p.id, "slug": p.slug, "title": p.title, "difficulty": p.difficulty} for p in problems]
    return {"bookmarked": is_bookmarked, "bookmarks": items}

@router.post("/me/bookmarks/toggle")
def toggle_bookmark(
    req: BookmarkRequest,
    user_id: Optional[str] = None,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    user_obj = current_user if isinstance(current_user, User) else None
    eff_user_id = (user_obj.id if user_obj else None) or (user_id if user_id and user_id.lower() != "guest" else None)
    if not eff_user_id:
        raise HTTPException(
            status_code=401,
            detail="Authentication required: please sign in to bookmark problems."
        )

    prob = db.query(Problem).filter((Problem.id == req.problem_id) | (Problem.slug == req.problem_id)).first()
    target_id = prob.id if prob else req.problem_id

    bm = db.query(Bookmark).filter(
        Bookmark.user_id == eff_user_id,
        Bookmark.problem_id == target_id
    ).first()

    if bm:
        db.delete(bm)
        db.commit()
        return {"bookmarked": False}
    else:
        new_bm = Bookmark(user_id=eff_user_id, problem_id=target_id)
        db.add(new_bm)
        db.commit()
        return {"bookmarked": True}
