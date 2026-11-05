from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.entities import Note, Problem, User
from ..auth_deps import get_current_user_optional

router = APIRouter(prefix="/notes", tags=["notes"])

class NotePayload(BaseModel):
    problem_id: str = Field(..., max_length=128)
    body_md: str = Field(..., max_length=50000)
    user_id: Optional[str] = Field(default=None, max_length=128)

@router.get("/{problem_id}")
def get_note(
    problem_id: str,
    user_id: Optional[str] = None,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    user_obj = current_user if isinstance(current_user, User) else None
    eff_user_id = (user_obj.id if user_obj else None) or user_id or "guest"
    if eff_user_id == "guest":
        return {"body_md": "", "updated_at": None}

    target_pid = "two-sum-sorted" if problem_id == "two-sum-sorted-offsets" else problem_id
    prob = db.query(Problem).filter((Problem.id == target_pid) | (Problem.slug == target_pid)).first()
    p_id = prob.id if prob else target_pid

    note = db.query(Note).filter(
        Note.user_id == eff_user_id,
        Note.problem_id == p_id
    ).first()
    return {"body_md": note.body_md if note else "", "updated_at": note.updated_at.isoformat() if note else None}

@router.post("")
def save_note(
    payload: NotePayload,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    user_obj = current_user if isinstance(current_user, User) else None
    eff_user_id = (user_obj.id if user_obj else None) or (payload.user_id if payload.user_id and payload.user_id.lower() != "guest" else None)
    if not eff_user_id:
        raise HTTPException(
            status_code=401,
            detail="Authentication required: please sign in to save personal notes."
        )

    target_pid = "two-sum-sorted" if payload.problem_id == "two-sum-sorted-offsets" else payload.problem_id
    prob = db.query(Problem).filter(
        (Problem.id == target_pid) | (Problem.slug == target_pid)
    ).first()
    p_id = prob.id if prob else target_pid

    note = db.query(Note).filter(
        Note.user_id == eff_user_id,
        Note.problem_id == p_id
    ).first()

    if not note:
        note = Note(user_id=eff_user_id, problem_id=p_id, body_md=payload.body_md)
        db.add(note)
    else:
        note.body_md = payload.body_md
        note.updated_at = datetime.now(timezone.utc)

    db.commit()
    return {"status": "saved", "updated_at": note.updated_at.isoformat()}
