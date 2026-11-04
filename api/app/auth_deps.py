from typing import Optional
from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models.entities import User

def get_current_user_optional(
    authorization: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Retrieves the current authenticated user if token or X-User-Id is provided.
    Returns None for anonymous guests without raising an error.
    """
    user_id = None
    if authorization and authorization.startswith("Bearer "):
        user_id = authorization.replace("Bearer ", "").strip()
    elif x_user_id:
        user_id = x_user_id.strip()

    if not user_id or user_id.lower() == "guest":
        return None

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
