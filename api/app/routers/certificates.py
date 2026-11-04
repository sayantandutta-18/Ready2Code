import secrets
from datetime import datetime, timezone
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.entities import Certificate, User

router = APIRouter(prefix="/certificates", tags=["certificates"])

class SubmitSkillTestRequest(BaseModel):
    user_id: str = "guest"
    skill: str # Problem Solving, Python 3, Data Structures
    score_pct: int # Must be >= 70%

@router.post("/issue")
def issue_certificate(req: SubmitSkillTestRequest, db: Session = Depends(get_db)):
    if req.score_pct < 70:
        raise HTTPException(
            status_code=400,
            detail=f"Passing threshold is 70%. Your score of {req.score_pct}% did not qualify."
        )

    user = db.query(User).filter(User.id == req.user_id).first()
    if not user:
        user = User(id=req.user_id, username=f"user_{req.user_id[:6]}")
        db.add(user)
        db.commit()

    code = f"R2C-{secrets.token_hex(4).upper()}"
    cert = Certificate(
        user_id=user.id,
        skill=req.skill,
        score=req.score_pct,
        verify_code=code,
        issued_at=datetime.now(timezone.utc)
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)

    return {
        "status": "issued",
        "verify_code": cert.verify_code,
        "skill": cert.skill,
        "score": cert.score,
        "holder_name": user.display_name or user.username,
        "verify_url": f"/certificates/{cert.verify_code}"
    }

@router.get("/verify/{verify_code}")
def verify_certificate(verify_code: str, db: Session = Depends(get_db)):
    cert = db.query(Certificate).filter(Certificate.verify_code == verify_code.upper()).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Invalid certificate verification code")

    user = cert.user
    return {
        "verified": True,
        "verify_code": cert.verify_code,
        "skill": cert.skill,
        "score": cert.score,
        "holder_name": user.display_name or user.username if user else "Verified Coder",
        "issued_at": cert.issued_at.strftime("%B %d, %Y"),
        "platform": "Ready2Code 3D DSA Arena"
    }
