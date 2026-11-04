from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/placement", tags=["placement"])

PLACEMENT_TRACKS = [
    {
        "id": "aptitude",
        "title": "Campus & Company Aptitude",
        "description": "Number series, percentages, time & work, and logical reasoning for TCS, Infosys, Wipro, and Cognizant.",
        "total_questions": 15,
        "companies": ["TCS NQT", "Infosys", "Wipro", "Cognizant"]
    },
    {
        "id": "product_dsa",
        "title": "Product Company High-Yield DSA",
        "description": "Crucial 50 algorithmic problems asked repeatedly at Amazon, Google, Microsoft, and Uber.",
        "total_questions": 12,
        "companies": ["Amazon", "Google", "Microsoft", "Uber"]
    },
    {
        "id": "cs_core",
        "title": "CS Fundamentals Core",
        "description": "Operating Systems, DBMS & SQL, Computer Networks, and Object-Oriented Design interview questions.",
        "total_questions": 20,
        "companies": ["All Engineering Roles"]
    },
    {
        "id": "resume_prep",
        "title": "ATS Resume & Technical Interview Guide",
        "description": "ATS-friendly templates, project presentation techniques, and STAR behavioural answer formulas.",
        "total_questions": 8,
        "companies": ["Career Acceleration"]
    }
]

CS_QUESTIONS_DATA = [
    {
        "id": "os-1",
        "track": "cs_core",
        "title": "Process vs Thread",
        "question": "What is the fundamental difference between a Process and a Thread? How do context switching overheads differ?",
        "answer_md": """### Process vs Thread
- **Process:** An independent program in execution with its own separate address space, file handles, and memory map.
- **Thread:** A lightweight unit of execution within a process that shares the code, data, and open files with sibling threads, but maintains its own program counter and stack.
- **Context Switch:** Thread context switching is significantly faster than process context switching because memory cache (TLB) doesn't need to be flushed.""",
        "hindi_summary": "Process ek poora program hota hai jiska apna alag memory space hota hai. Thread usi process ke andar chhota hissa hota hai jo shared memory use karta hai, isliye context switch bohot fast hota hai.",
        "bengali_summary": "Process holo ekta purno program jar nijosho alada memory thake. Thread holo sei process-er ontorgoto ekta lightweight unit ja shared memory bebohar kore, tai context switch onek druto hoy."
    },
    {
        "id": "dbms-1",
        "track": "cs_core",
        "title": "ACID Properties in Relational Databases",
        "question": "Explain ACID properties in DBMS and why they are critical for transactional systems.",
        "answer_md": """### ACID Properties
- **Atomicity:** All operations in a transaction succeed completely or none take effect.
- **Consistency:** The database transitions from one valid state to another, preserving all integrity constraints.
- **Isolation:** Concurrent transactions execute without interfering with one another.
- **Durability:** Committed transactions persist permanently even across hardware failures.""",
        "hindi_summary": "ACID ka matlab hai: Atomicity (sab hoga ya kuch nahi), Consistency (data sahi rules follow karega), Isolation (ek transaction dusre ko disturb nahi karega), aur Durability (save hone ke baad data surakshit rahega).",
        "bengali_summary": "ACID-er ortho holo: Atomicity (sobtuku hobe ba kichui hobe na), Consistency (nirdharito niyam mene cholbe), Isolation (ekta transaction onnotake disturb korbe na), Durability (commit houyar por data shorbo-da shurokkhito thakbe)."
    },
    {
        "id": "networks-1",
        "track": "cs_core",
        "title": "TCP 3-Way Handshake",
        "question": "How does TCP establish a reliable connection using the 3-Way Handshake?",
        "answer_md": """### TCP 3-Way Handshake
1. **SYN:** Client sends SYN with sequence number $X$.
2. **SYN-ACK:** Server responds with SYN with sequence number $Y$ and ACK $X+1$.
3. **ACK:** Client sends ACK with sequence number $Y+1$. Connection is now ESTABLISHED.""",
        "hindi_summary": "Client SYN bhejta hai, server SYN-ACK se jawaab deta hai, aur client aakhri ACK bhej kar connection establish kar leta hai.",
        "bengali_summary": "Client prothome SYN pathay, server SYN-ACK diye uttor dey, ebong client sheshe ACK pathiye connection sthapon kore."
    }
]

@router.get("/tracks")
def get_tracks():
    return PLACEMENT_TRACKS

@router.get("/questions")
def get_questions(track: str = "cs_core", lang: str = "en"):
    questions = [q for q in CS_QUESTIONS_DATA if q["track"] == track]
    res = []
    for q in questions:
        summary = q["answer_md"]
        if lang == "hi" and q.get("hindi_summary"):
            summary = q["hindi_summary"]
        elif lang == "bn" and q.get("bengali_summary"):
            summary = q["bengali_summary"]

        res.append({
            "id": q["id"],
            "title": q["title"],
            "question": q["question"],
            "answer": summary,
            "full_answer_md": q["answer_md"]
        })
    return res
