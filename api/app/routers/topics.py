from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.entities import Topic, Problem

router = APIRouter(prefix="/topics", tags=["topics"])

@router.get("")
def get_topics(db: Session = Depends(get_db)):
    topics = db.query(Topic).order_by(Topic.order_index.asc()).all()
    res = []
    for t in topics:
        res.append({
            "id": t.id,
            "slug": t.slug,
            "name": t.name,
            "order_index": t.order_index,
            "problem_count": len([p for p in t.problems if p.is_published])
        })
    return res
