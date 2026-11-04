from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/placement", tags=["placement"])

PLACEMENT_TRACKS = [
    {
        "id": "cs_core",
        "title": "CS Fundamentals Core",
        "description": "Operating Systems, DBMS & SQL, Computer Networks, and Object-Oriented Design interview questions.",
        "total_questions": 10,
        "companies": ["All Engineering Roles", "Google", "Microsoft"]
    },
    {
        "id": "aptitude",
        "title": "Campus & Company Aptitude",
        "description": "Number series, percentages, time & work, and logical reasoning for TCS, Infosys, Wipro, and Cognizant.",
        "total_questions": 6,
        "companies": ["TCS NQT", "Infosys", "Wipro", "Cognizant"]
    },
    {
        "id": "product_dsa",
        "title": "Product Company High-Yield DSA",
        "description": "Crucial 50 algorithmic problems asked repeatedly at Amazon, Google, Microsoft, and Uber.",
        "total_questions": 6,
        "companies": ["Amazon", "Google", "Microsoft", "Uber"]
    },
    {
        "id": "resume_prep",
        "title": "ATS Resume & Technical Interview Guide",
        "description": "ATS-friendly templates, project presentation techniques, and STAR behavioural answer formulas.",
        "total_questions": 5,
        "companies": ["Career Acceleration", "All Tech Roles"]
    }
]

CS_QUESTIONS_DATA = [
    # --- CS CORE: OS ---
    {
        "id": "os-1",
        "track": "cs_core",
        "title": "Process vs Thread & Context Switching",
        "question": "What is the fundamental difference between a Process and a Thread? How do context switching overheads differ?",
        "answer_md": """### Process vs Thread
- **Process:** An independent program in execution with its own separate address space, file handles, and memory map.
- **Thread:** A lightweight unit of execution within a process that shares the code, data, and open files with sibling threads, but maintains its own program counter, registers, and stack.
- **Context Switch:** Thread context switching is orders of magnitude faster because the memory cache (TLB) does not need to be flushed, unlike process switching.""",
        "hindi_summary": "Process ek poora program hota hai jiska apna alag memory space hota hai. Thread usi process ke andar chhota hissa hota hai jo shared memory use karta hai, isliye context switch bohot fast hota hai.",
        "bengali_summary": "Process holo ekta purno program jar nijosho alada memory thake. Thread holo sei process-er ontorgoto ekta lightweight unit ja shared memory bebohar kore, tai context switch onek druto hoy."
    },
    {
        "id": "os-2",
        "track": "cs_core",
        "title": "Deadlock: Conditions & Prevention",
        "question": "What are the 4 Coffman conditions required for Deadlock to occur, and how can they be prevented?",
        "answer_md": """### Coffman Conditions for Deadlock
1. **Mutual Exclusion:** Resources cannot be shared simultaneously.
2. **Hold and Wait:** A process holding at least one resource is waiting for another held by another process.
3. **No Preemption:** Resources cannot be forcibly revoked.
4. **Circular Wait:** A closed cycle exists where $P_0$ waits for $P_1$, and $P_n$ waits for $P_0$.

**Prevention:** Break any single condition (e.g. acquire all resources upfront, enforce global total ordering on resource IDs).""",
        "hindi_summary": "Deadlock hone ke 4 kaaran hote hain: Mutual Exclusion, Hold & Wait, No Preemption, aur Circular Wait. Inme se kisi ek ko bhi todne se deadlock avoid ho jaata hai.",
        "bengali_summary": "Deadlock hote 4ti shoroto dorkar hoy: Mutual Exclusion, Hold & Wait, No Preemption, ebong Circular Wait. Er moddhe je kono ekti bhanglei deadlock thakbe na."
    },
    {
        "id": "os-3",
        "track": "cs_core",
        "title": "Virtual Memory, Paging, and Page Faults",
        "question": "How does Virtual Memory work? What exact sequence of events occurs on a Page Fault?",
        "answer_md": """### Virtual Memory & Paging
- Virtual memory decouples logical process memory from physical RAM using the **Memory Management Unit (MMU)** and **Page Tables**.
- When a referenced virtual page has its valid bit unset in the page table, a **Page Fault interrupt** is raised.
- OS catches trap -> pauses process -> locates missing page on disk/swap -> reads page into available RAM frame -> updates page table valid bit -> resumes instruction.""",
        "hindi_summary": "Virtual memory process ko RAM se zyada memory use karne deti hai. Jab zaroori page RAM me nahi milta, to Page Fault hota hai aur OS disk se use load karta hai.",
        "bengali_summary": "Virtual memory-r maddhome RAM-er cheyeo beshi memory bebohar kora jay. Jokhon kono dorkari page RAM-e thake na, tokhon Page Fault hoy ebong OS disk theke ta load kore."
    },

    # --- CS CORE: DBMS ---
    {
        "id": "dbms-1",
        "track": "cs_core",
        "title": "ACID Properties in Relational Databases",
        "question": "Explain ACID properties in DBMS and why they are critical for transactional systems.",
        "answer_md": """### ACID Properties
- **Atomicity:** All operations in a transaction succeed completely or none take effect (via write-ahead log & rollback).
- **Consistency:** The database transitions from one valid state to another, preserving all integrity constraints.
- **Isolation:** Concurrent transactions execute without dirty reads or phantom data (managed via locks/MVCC).
- **Durability:** Committed transactions persist permanently even across power failures.""",
        "hindi_summary": "ACID ka matlab hai: Atomicity (sab hoga ya kuch nahi), Consistency (data sahi rules follow karega), Isolation (ek transaction dusre ko disturb nahi karega), aur Durability (save hone ke baad data surakshit rahega).",
        "bengali_summary": "ACID-er ortho holo: Atomicity (sobtuku hobe ba kichui hobe na), Consistency (nirdharito niyam mene cholbe), Isolation (ekta transaction onnotake disturb korbe na), Durability (commit houyar por data shorbo-da shurokkhito thakbe)."
    },
    {
        "id": "dbms-2",
        "track": "cs_core",
        "title": "Database Indexing: B-Tree vs Hash Index",
        "question": "How do B-Trees optimize database queries? When should you use a Hash Index instead?",
        "answer_md": """### Database Indexing
- **B+ Tree Index:** Balanced multi-way search tree. Leaves are linked sequentially. Enables $O(\\log n)$ point queries AND efficient **range scans** (`BETWEEN`, `<`, `>`). Default in MySQL InnoDB & PostgreSQL.
- **Hash Index:** Bucket lookup based on hash function. Delivers $O(1)$ point equality lookups (`WHERE id = 5`), but CANNOT perform range scans or prefix searches.""",
        "hindi_summary": "B+ Tree index range search (jaise 10 se 50 tak) aur point query dono ke liye behtareen hota hai. Hash index sirf exact match (WHERE id = 5) ke liye O(1) me kaam karta hai.",
        "bengali_summary": "B+ Tree index range scan ebong point query dutor jonnoi khub valo. Hash index shudhumatro exact equality match-er jonno O(1) shomoy ney, kintu range query korte pare na."
    },

    # --- CS CORE: NETWORKS ---
    {
        "id": "networks-1",
        "track": "cs_core",
        "title": "TCP 3-Way Handshake Reliability",
        "question": "How does TCP establish a reliable connection using the 3-Way Handshake?",
        "answer_md": """### TCP 3-Way Handshake
1. **SYN:** Client sends SYN with initial sequence number $X$.
2. **SYN-ACK:** Server responds with SYN with sequence number $Y$ and ACK $X+1$.
3. **ACK:** Client sends ACK with sequence number $Y+1$. Connection is now ESTABLISHED with synchronized duplex sequence windows.""",
        "hindi_summary": "Client SYN bhejta hai, server SYN-ACK se jawaab deta hai, aur client aakhri ACK bhej kar connection establish kar leta hai.",
        "bengali_summary": "Client prothome SYN pathay, server SYN-ACK diye uttor dey, ebong client sheshe ACK pathiye connection sthapon kore."
    },
    {
        "id": "networks-2",
        "track": "cs_core",
        "title": "TCP vs UDP: Trade-offs & Protocols",
        "question": "Compare TCP vs UDP in terms of connection state, overhead, reliability, and real-world use cases.",
        "answer_md": """### TCP vs UDP
- **TCP (Transmission Control Protocol):** Connection-oriented, guarantees packet delivery and ordering, flow control, congestion control. Used for HTTP/HTTPS, SSH, File Transfers.
- **UDP (User Datagram Protocol):** Connectionless, lightweight (8-byte header vs 20-byte TCP), no retransmission or ordering guarantees. Used for DNS, Video Streaming, Real-time Multiplayer Gaming, VoIP.""",
        "hindi_summary": "TCP reliable aur ordered hota hai jisme pakka data milta hai (web pages, files). UDP fast hota hai bina confirmation ke (gaming, live video streaming).",
        "bengali_summary": "TCP data delivery nishchit kore ebong shothik krome pathay. UDP onek druto kintu delivery guarantee kore na (live video ba gaming-e lage)."
    },

    # --- APTITUDE TRACK ---
    {
        "id": "apt-1",
        "track": "aptitude",
        "title": "Time and Work: Men and Days Formula",
        "question": "If 12 men can complete a project in 15 days working 8 hours a day, how many days will 18 men take working 10 hours a day?",
        "answer_md": """### Formula: $\\frac{M_1 D_1 H_1}{W_1} = \\frac{M_2 D_2 H_2}{W_2}$
- $M_1 = 12, D_1 = 15, H_1 = 8$
- $M_2 = 18, H_2 = 10, D_2 = ?$
- $12 \\times 15 \\times 8 = 18 \\times D_2 \\times 10$
- $1440 = 180 \\times D_2 \\implies D_2 = \\mathbf{8\\text{ days}}$. Answer: **8 Days**.""",
        "hindi_summary": "MDH formula use karein: 12 * 15 * 8 = 18 * D2 * 10. Solve karne par D2 = 8 din milta hai.",
        "bengali_summary": "MDH sutro bebohar korun: 12 * 15 * 8 = 18 * D2 * 10. Solution ashe D2 = 8 din."
    },
    {
        "id": "apt-2",
        "track": "aptitude",
        "title": "Percentages & Successive Discounts",
        "question": "A laptop is marked at ₹50,000. An online store gives two successive discounts of 20% and 10%. What is the final selling price?",
        "answer_md": """### Successive Discount Formula: $D_{\\text{eff}} = d_1 + d_2 - \\frac{d_1 d_2}{100}$
- $D_{\\text{eff}} = 20 + 10 - \\frac{20 \\times 10}{100} = 30 - 2 = 28\\%$.
- Discount amount = $28\\% \\text{ of } 50,000 = ₹14,000$.
- Selling Price = $50,000 - 14,000 = \\mathbf{₹36,000}$. Answer: **₹36,000**.""",
        "hindi_summary": "Successive discount nikaalne ke liye: 20 + 10 - (20*10)/100 = 28% total chhoot. 50,000 me se 28% ghata kar ₹36,000 banta hai.",
        "bengali_summary": "Duti kromo-gotyo chharer sutro: 20 + 10 - 2 = 28%. 50,000 takar 28% chhar dile bikroy mullo hoy ₹36,000."
    },

    # --- RESUME PREP TRACK ---
    {
        "id": "resume-1",
        "track": "resume_prep",
        "title": "The Google XYZ Resume Formula",
        "question": "How do you frame engineering project bullet points on your resume using Google's XYZ formula?",
        "answer_md": """### Google XYZ Formula
**\"Accomplished [X] as measured by [Y], by doing [Z]\"**

**Example Bad Bullet:**
- Built an algorithm visualizer with Next.js and Python.

**Example Production XYZ Bullet:**
- Engineered an interactive 3D algorithm visualizer supporting 30 problems, reducing user debugging time by **42%** through sub-millisecond trace playback built with **React Three Fiber and WebGL**.""",
        "hindi_summary": "Apne resume ke points me hamesha XYZ formula use karein: Maine [X] kaam kiya, jiska measurable result [Y]% tha, [Z] technology use karke.",
        "bengali_summary": "Resume-te shobshomoy XYZ formula bebohar korun: [X] kaaj korechi, jar folafol [Y] poriman unnoti hoyeche, [Z] projukti bebohar kore."
    }
]

@router.get("/tracks")
def get_tracks():
    return PLACEMENT_TRACKS

@router.get("/questions")
def get_questions(track: str = "cs_core", lang: str = "en"):
    questions = [q for q in CS_QUESTIONS_DATA if q["track"] == track]
    if not questions:
        # Return all if track not specifically populated
        questions = CS_QUESTIONS_DATA[:6]

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
