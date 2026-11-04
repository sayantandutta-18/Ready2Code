from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..database import get_db
from ..models.entities import Discussion, Comment, Vote, Problem, User
from ..auth_deps import get_current_user_optional

router = APIRouter(prefix="/discussions", tags=["discussions"])

class CreateDiscussionRequest(BaseModel):
    problem_slug: str = Field(..., max_length=128)
    title: str = Field(..., min_length=1, max_length=250)
    body_md: str = Field(..., min_length=1, max_length=15000)
    is_solution: bool = False
    author_id: str = Field(default="guest", max_length=128)

class VoteRequest(BaseModel):
    user_id: str = Field(default="guest", max_length=128)
    target_type: str = Field(..., max_length=32) # discussion, comment
    target_id: str = Field(..., max_length=128)
    value: int # 1 or -1

class CommentRequest(BaseModel):
    author_id: str = Field(default="guest", max_length=128)
    body_md: str = Field(..., min_length=1, max_length=10000)
    parent_id: Optional[str] = Field(default=None, max_length=128)

@router.get("/problem/{problem_slug}")
def get_problem_discussions(
    problem_slug: str,
    is_solution: bool = False,
    sort: str = "top", # top, new, old
    db: Session = Depends(get_db)
):
    prob = db.query(Problem).filter(Problem.slug == problem_slug).first()
    if not prob:
        raise HTTPException(status_code=404, detail="Problem not found")

    q = db.query(Discussion).filter(
        Discussion.problem_id == prob.id,
        Discussion.is_solution == is_solution,
        Discussion.is_hidden == False
    )

    if sort == "new":
        q = q.order_by(Discussion.created_at.desc())
    elif sort == "old":
        q = q.order_by(Discussion.created_at.asc())
    else: # top
        q = q.order_by(desc(Discussion.votes))

    threads = q.all()

    return [
        {
            "id": t.id,
            "title": t.title,
            "body_md": t.body_md,
            "votes": t.votes,
            "is_solution": t.is_solution,
            "author": t.author.username if t.author else "coder",
            "created_at": t.created_at.isoformat(),
            "comments_count": len(t.comments)
        }
        for t in threads
    ]

@router.post("")
def create_discussion(
    req: CreateDiscussionRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    user_obj = current_user if isinstance(current_user, User) else None
    eff_author_id = user_obj.id if user_obj else (req.author_id if req.author_id and req.author_id.lower() != "guest" else None)
    if not eff_author_id:
        raise HTTPException(
            status_code=401,
            detail="Authentication required: please sign in to post discussions or solutions."
        )

    prob = db.query(Problem).filter(Problem.slug == req.problem_slug).first()
    if not prob:
        raise HTTPException(status_code=404, detail="Problem not found")

    if req.is_solution:
        # Check requirement: at least 50 words in their own words
        words = req.body_md.strip().split()
        if len(words) < 50:
            raise HTTPException(
                status_code=400,
                detail=f"To share a solution, explain your approach in at least 50 words (currently {len(words)} words)."
            )

    author = db.query(User).filter(User.id == eff_author_id).first()
    if not author:
        author = User(id=eff_author_id, username=f"user_{eff_author_id[:6]}")
        db.add(author)
        db.commit()

    disc = Discussion(
        problem_id=prob.id,
        author_id=author.id,
        title=req.title,
        body_md=req.body_md,
        is_solution=req.is_solution,
        votes=1
    )
    db.add(disc)
    db.commit()
    db.refresh(disc)

    return {"status": "created", "id": disc.id}

@router.post("/vote")
def cast_vote(req: VoteRequest, db: Session = Depends(get_db)):
    v = db.query(Vote).filter(
        Vote.user_id == req.user_id,
        Vote.target_type == req.target_type,
        Vote.target_id == req.target_id
    ).first()

    val = 1 if req.value > 0 else -1

    if not v:
        v = Vote(
            user_id=req.user_id,
            target_type=req.target_type,
            target_id=req.target_id,
            value=val
        )
        db.add(v)
        delta = val
    else:
        if v.value == val:
            # cancel vote
            db.delete(v)
            delta = -val
        else:
            v.value = val
            delta = 2 * val

    if req.target_type == "discussion":
        target = db.query(Discussion).filter(Discussion.id == req.target_id).first()
        if target:
            target.votes += delta
    elif req.target_type == "comment":
        target = db.query(Comment).filter(Comment.id == req.target_id).first()
        if target:
            target.votes += delta

    db.commit()
    return {"status": "ok"}
