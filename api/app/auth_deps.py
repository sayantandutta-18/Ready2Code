from typing import Optional
from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
import jwt
from .database import get_db
from .models.entities import User
from .config import settings

def get_current_user_optional(
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Retrieves the current authenticated user from Bearer JWT token or X-User-Id header.
    Returns None for anonymous guests without raising an error.
    """
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "").strip()
    elif x_user_id:
        token = x_user_id.strip()

    if not token or token.lower() == "guest":
        return None

    user_id = token
    # Try decoding token as JWT
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        if "sub" in payload:
            user_id = payload["sub"]
    except Exception:
        # Fallback to direct user_id or username
        pass

    user = db.query(User).filter((User.id == user_id) | (User.username == user_id)).first()
    return user

def get_current_user(
    user: Optional[User] = Depends(get_current_user_optional)
) -> User:
    """
    Requires an authenticated user. Raises HTTP 401 if anonymous.
    """
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Authentication required to perform this action. Please sign in."
        )
    return user
