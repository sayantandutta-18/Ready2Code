import uuid
from typing import Optional, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/interviews", tags=["interviews"])

class InterviewRound(BaseModel):
    name: str
    desc: str

class CreateInterviewRequest(BaseModel):
    author: str = "Anonymous"
    company: str
    role: str
    date: str
    verdict: str # Offer, Rejected
    ctc: str
    difficulty: str # Easy, Medium, Hard
    rounds: List[InterviewRound]
    advice: str

INTERVIEWS_DB = [
    {
        "id": "exp-1",
        "author": "Rohan V.",
        "company": "Google",
        "role": "Software Engineer (L3)",
        "date": "October 2026",
        "verdict": "Offer",
        "ctc": "₹45 LPA",
        "difficulty": "Hard",
        "rounds": [
            {"name": "OA (Online Assessment)", "desc": "2 graph questions involving Dijkstra and disjoint set union."},
            {"name": "Technical Round 1", "desc": "Sliding window maximum with monotonic deque + follow-up on 2D matrix."},
            {"name": "Technical Round 2", "desc": "Dynamic programming on trees with subtree memoization."},
            {"name": "Googlyness", "desc": "Hypothetical engineering conflict scenarios and cross-team communication."}
        ],
        "advice": "Do not jump straight into coding. Talk out loud for the first 5 minutes to validate edge cases and explain time/space trade-offs."
    },
    {
        "id": "exp-2",
        "author": "Sneha M.",
        "company": "Amazon",
        "role": "SDE-1",
        "date": "September 2026",
        "verdict": "Offer",
        "ctc": "₹34 LPA",
        "difficulty": "Medium",
        "rounds": [
            {"name": "OA", "desc": "Two Sum variant with stock profit optimization + debugging section."},
            {"name": "Round 1 (DSA)", "desc": "Lowest common ancestor in binary tree + Amazon LP Customer Obsession."},
            {"name": "Round 2 (DSA)", "desc": "Rotting Oranges multi-source BFS with edge cases."},
            {"name": "Round 3 (Bar Raiser)", "desc": "LRU Cache design and deep dive into 'Deliver Results' principle."}
        ],
        "advice": "Prepare 2 real stories in STAR format (Situation, Task, Action, Result) for every Amazon Leadership Principle."
    },
    {
        "id": "exp-3",
        "author": "Arjun K.",
        "company": "Microsoft",
        "role": "Software Engineer",
        "date": "August 2026",
        "verdict": "Offer",
        "ctc": "₹28 LPA",
        "difficulty": "Medium",
        "rounds": [
            {"name": "Round 1", "desc": "Reverse Linked List in K-groups + edge case discussion."},
            {"name": "Round 2", "desc": "Course Schedule topological sort (Kahn's algorithm)."},
            {"name": "Round 3 (Director)", "desc": "Project architecture deep dive and concurrency questions."}
        ],
        "advice": "Focus on clean code, naming conventions, and handling null/empty pointer checks before the interviewer asks."
    },
    {
        "id": "exp-4",
        "author": "Pooja D.",
        "company": "Uber",
        "role": "Software Engineer 1",
        "date": "November 2026",
        "verdict": "Rejected",
        "ctc": "₹42 LPA",
        "difficulty": "Hard",
        "rounds": [
            {"name": "Round 1 (DSA)", "desc": "Word Search II with Trie optimization. Got stuck on prefix pruning."},
            {"name": "Round 2 (DSA)", "desc": "Trapping Rain Water with two pointers. Passed all test cases."}
        ],
        "advice": "Uber's algorithmic bar is high. Practice hard Trie and Backtracking problems under a strict 35-minute timer."
    }
]

@router.get("")
def list_interviews(company: Optional[str] = None, verdict: Optional[str] = None):
    res = INTERVIEWS_DB
    if company and company.lower() != "all":
        res = [item for item in res if item["company"].lower() == company.lower()]
    if verdict and verdict.lower() != "all":
        res = [item for item in res if item["verdict"].lower() == verdict.lower()]
    return res

@router.post("")
def create_interview(req: CreateInterviewRequest):
    new_id = f"exp-{str(uuid.uuid4())[:8]}"
    item = {
        "id": new_id,
        "author": req.author,
        "company": req.company,
        "role": req.role,
        "date": req.date,
        "verdict": req.verdict,
        "ctc": req.ctc,
        "difficulty": req.difficulty,
        "rounds": [r.dict() for r in req.rounds],
        "advice": req.advice
    }
    INTERVIEWS_DB.insert(0, item)
    return {"status": "created", "interview": item}
