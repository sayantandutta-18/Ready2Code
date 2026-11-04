from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.entities import Note, Problem

router = APIRouter(prefix="/notes", tags=["notes"])

class NotePayload(BaseModel):
    problem_id: str
    body_md: str
    user_id: Optional[str] = "guest"

@router.get("/{problem_id}")
def get_note(problem_id: str, user_id: str = "guest", db: Session = Depends(get_db)):
    note = db.query(Note).filter(
        Note.user_id == user_id,
        (Note.problem_id == problem_id) | (Note.problem.has(slug=problem_id))
    ).first()
    return {"body_md": note.body_md if note else "", "updated_at": note.updated_at.isoformat() if note else None}

@router.post("")
def save_note(payload: NotePayload, db: Session = Depends(get_db)):
    prob = db.query(Problem).filter(
        (Problem.id == payload.problem_id) | (Problem.slug == payload.problem_id)
    ).first()
    p_id = prob.id if prob else payload.problem_id

    note = db.query(Note).filter(
        Note.user_id == payload.user_id,
        Note.problem_id == p_id
    ).first()

    if not note:
        note = Note(user_id=payload.user_id, problem_id=p_id, body_md=payload.body_md)
        db.add(note)
    else:
        note.body_md = payload.body_md
        note.updated_at = datetime.utcnow()

    db.commit()
    return {"status": "saved", "updated_at": note.updated_at.isoformat()}
