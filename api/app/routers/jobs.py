import uuid
from typing import Optional, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/jobs", tags=["jobs"])

class JobApplicationRequest(BaseModel):
    user_id: str
    username: str
    elo: int
    certificate_code: Optional[str] = None

JOBS_DB = [
    {
        "id": "job-1",
        "company": "Razorpay",
        "role": "Software Development Engineer (Backend)",
        "location": "Bengaluru, India (Hybrid)",
        "ctc": "₹24 - ₹32 LPA",
        "min_elo": 1550,
        "tags": ["Go", "Distributed Systems", "DSA", "Kafka"],
        "description": "Scale India's premier financial payments infrastructure handling 10,000+ transactions per second."
    },
    {
        "id": "job-2",
        "company": "Zepto",
        "role": "SDE-1 (Supply Chain & Routing)",
        "location": "Mumbai / Bengaluru",
        "ctc": "₹28 - ₹36 LPA",
        "min_elo": 1600,
        "tags": ["Python", "Algorithms", "Graph Theory", "Redis"],
        "description": "Design hyper-optimized routing and dispatch algorithms for 10-minute grocery fulfillment."
    },
    {
        "id": "job-3",
        "company": "Cred",
        "role": "Backend Engineer (Payments & Trust)",
        "location": "Bengaluru, India",
        "ctc": "₹30 - ₹45 LPA",
        "min_elo": 1650,
        "tags": ["Java", "High Concurrency", "System Design"],
        "description": "Architect mission-critical payment workflows with four 9s reliability and microsecond latency."
    },
    {
        "id": "job-4",
        "company": "Swiggy",
        "role": "Software Engineer (Delivery Logistics)",
        "location": "Bengaluru / Remote",
        "ctc": "₹22 - ₹30 LPA",
        "min_elo": 1500,
        "tags": ["Java", "Data Structures", "Dynamic Programming"],
        "description": "Optimize real-time batching and delivery assignment algorithms across 500+ Indian cities."
    },
    {
        "id": "job-5",
        "company": "Meesho",
        "role": "SDE-1 (Platform & Search)",
        "location": "Bengaluru, India",
        "ctc": "₹20 - ₹28 LPA",
        "min_elo": 1500,
        "tags": ["Elasticsearch", "DSA", "Node.js"],
        "description": "Power high-throughput search and discovery for 100M+ monthly active Indian consumers."
    }
]

APPLICATIONS_DB: List[dict] = []

@router.get("")
def list_jobs():
    return JOBS_DB

@router.post("/{job_id}/apply")
def apply_for_job(job_id: str, req: JobApplicationRequest):
    job = next((j for j in JOBS_DB if j["id"] == job_id), None)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if req.elo < job["min_elo"]:
        raise HTTPException(
            status_code=400,
            detail=f"Minimum required rating is {job['min_elo']} ELO. Your current rating is {req.elo} ELO."
        )

    app_record = {
        "id": str(uuid.uuid4())[:8],
        "job_id": job_id,
        "company": job["company"],
        "role": job["role"],
        "user_id": req.user_id,
        "username": req.username,
        "elo": req.elo,
        "certificate_code": req.certificate_code,
        "status": "referred_fast_track"
    }
    APPLICATIONS_DB.append(app_record)
    return {"status": "success", "application": app_record}
