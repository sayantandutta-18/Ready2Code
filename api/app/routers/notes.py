from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.entities import Note, Problem, User
from ..auth_deps import get_current_user_optional

router = APIRouter(prefix="/notes", tags=["notes"])

class NotePayload(BaseModel):
    problem_id: str
    body_md: str
    user_id: Optional[str] = None

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

    prob = db.query(Problem).filter((Problem.id == problem_id) | (Problem.slug == problem_id)).first()
    p_id = prob.id if prob else problem_id

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

    prob = db.query(Problem).filter(
        (Problem.id == payload.problem_id) | (Problem.slug == payload.problem_id)
    ).first()
    p_id = prob.id if prob else payload.problem_id

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
