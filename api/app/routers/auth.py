import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional
import bcrypt
import jwt
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.entities import User, Streak, UserProblemStatus
from ..auth_deps import get_current_user
from ..config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

class AuthRequest(BaseModel):
    username: str
    password: Optional[str] = None
    display_name: Optional[str] = None
    timezone: Optional[str] = "UTC"

class UserResponse(BaseModel):
    id: str
    username: str
    display_name: str
    avatar_url: Optional[str] = None
    timezone: str
    streak: int
    xp: int
    solved_count: int

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False

def create_access_token(user_id: str, username: str) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=settings.JWT_EXPIRES_DAYS)
    payload = {
        "sub": user_id,
        "username": username,
        "exp": int(expire.timestamp()),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def build_user_payload(user: User, db: Session) -> dict:
    streak_rec = db.query(Streak).filter(Streak.user_id == user.id).first()
    current_streak = streak_rec.current_streak if streak_rec else 0
    xp_total = sum(x.amount for x in user.xp_entries) if user.xp_entries else 0
    solved_count = db.query(UserProblemStatus).filter(
        UserProblemStatus.user_id == user.id,
        UserProblemStatus.status == "solved"
    ).count()

    return {
        "id": user.id,
        "username": user.username,
        "display_name": user.display_name or user.username,
        "avatar_url": user.avatar_url,
        "timezone": user.timezone or "UTC",
        "streak": current_streak,
        "xp": xp_total,
        "solved_count": solved_count
    }

@router.post("/register")
def register(req: AuthRequest, db: Session = Depends(get_db)):
    clean_username = req.username.strip().lower()
    if len(clean_username) < 3 or len(clean_username) > 24:
        raise HTTPException(status_code=400, detail="Username must be between 3 and 24 characters")
    if not clean_username.replace("_", "").replace("-", "").isalnum():
        raise HTTPException(status_code=400, detail="Username may only contain letters, numbers, hyphens, and underscores")

    existing = db.query(User).filter(User.username == clean_username).first()
    if existing:
        raise HTTPException(status_code=409, detail="Username is already taken. Please choose another or sign in.")

    password_hash = hash_password(req.password) if req.password else None

    user = User(
        id=f"user_{uuid.uuid4().hex[:12]}",
        username=clean_username,
        password_hash=password_hash,
        display_name=req.display_name or req.username.strip(),
        timezone=req.timezone or "UTC"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Initialize streak record
    db.add(Streak(user_id=user.id, current_streak=0, longest_streak=0, last_active_date=None, freezes_left=2))
    db.commit()

    token = create_access_token(user.id, user.username)
    user_payload = build_user_payload(user, db)
    return {
        "token": token,
        "user": user_payload
    }

@router.post("/login")
def login(req: AuthRequest, db: Session = Depends(get_db)):
    clean_username = req.username.strip().lower()
    user = db.query(User).filter((User.username == clean_username) | (User.id == clean_username)).first()

    if not user:
        if settings.DEV_DEMO_LOGIN:
            # Auto-create demo user for smooth testing
            user = User(
                id=f"user_{uuid.uuid4().hex[:12]}",
                username=clean_username,
                password_hash=hash_password(req.password) if req.password else None,
                display_name=req.display_name or req.username.strip(),
                timezone=req.timezone or "UTC"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            db.add(Streak(user_id=user.id, current_streak=0, longest_streak=0, last_active_date=None, freezes_left=2))
            db.commit()
        else:
            raise HTTPException(status_code=401, detail="Invalid username or password")

    if user.password_hash and req.password:
        if not verify_password(req.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid username or password")
    elif user.password_hash and not req.password:
        if not settings.DEV_DEMO_LOGIN:
            raise HTTPException(status_code=401, detail="Password is required")

    token = create_access_token(user.id, user.username)
    user_payload = build_user_payload(user, db)
    return {
        "token": token,
        "user": user_payload
    }

@router.get("/me")
def get_current_user_profile(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return build_user_payload(user, db)
