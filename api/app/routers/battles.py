import uuid
import random
import time
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/battles", tags=["battles"])

# In-memory battle state cache (production connects to Redis)
_BATTLES: Dict[str, Dict[str, Any]] = {}

class QueueRequest(BaseModel):
    user_id: str
    username: str
    elo: int = 1500
    preferred_language: str = "python"

class BattleSubmitRequest(BaseModel):
    user_id: str
    passed_tests: int
    total_tests: int
    runtime_ms: int

BOT_NAMES = ["AlgorithmAce", "CodeNinja99", "ByteMaster", "GraphWalker", "DpDynasty", "BinaryBeast"]

@router.post("/queue")
def queue_battle(req: QueueRequest):
    """
    Matchmakes a 1v1 coding battle with another user or instant Elo-balanced rival.
    """
    battle_id = str(uuid.uuid4())[:8]
    bot_name = random.choice(BOT_NAMES)
    bot_elo = max(800, req.elo + random.randint(-40, 40))
    
    # Pick a popular battle problem
    problems_pool = [
        {"slug": "two-sum", "title": "Two Sum", "difficulty": "Easy", "time_limit": 600},
        {"slug": "valid-parentheses", "title": "Valid Parentheses", "difficulty": "Easy", "time_limit": 600},
        {"slug": "container-with-most-water", "title": "Container With Most Water", "difficulty": "Medium", "time_limit": 900},
        {"slug": "maximum-subarray", "title": "Maximum Subarray", "difficulty": "Medium", "time_limit": 900},
        {"slug": "best-time-to-buy-and-sell-stock", "title": "Best Time to Buy and Sell Stock", "difficulty": "Easy", "time_limit": 600}
    ]
    selected_prob = random.choice(problems_pool)
    
    battle_data = {
        "id": battle_id,
        "status": "ongoing",
        "created_at": time.time(),
        "duration_seconds": selected_prob["time_limit"],
        "problem": selected_prob,
        "player1": {
            "id": req.user_id,
            "username": req.username,
            "elo": req.elo,
            "progress": 0,
            "passed": 0,
            "total": 5,
            "status": "coding"
        },
        "player2": {
            "id": f"bot_{bot_name.lower()}",
            "username": bot_name,
            "elo": bot_elo,
            "progress": 0,
            "passed": 0,
            "total": 5,
            "status": "coding",
            "is_bot": True
        },
        "winner": None
    }
    _BATTLES[battle_id] = battle_data
    return battle_data

@router.get("/{battle_id}")
def get_battle(battle_id: str):
    if battle_id not in _BATTLES:
        raise HTTPException(status_code=404, detail="Battle not found")
    
    battle = _BATTLES[battle_id]
    
    # Simulate rival bot progress realistically over elapsed time
    if battle["status"] == "ongoing" and battle["player2"].get("is_bot"):
        elapsed = time.time() - battle["created_at"]
        # Bot progresses roughly every 30-45 seconds
        bot_tests = min(5, int(elapsed / 35))
        battle["player2"]["passed"] = bot_tests
        battle["player2"]["progress"] = int((bot_tests / 5) * 100)
        
        if bot_tests == 5 and not battle["winner"]:
            battle["status"] = "finished"
            battle["winner"] = battle["player2"]["username"]
            battle["player2"]["status"] = "accepted"
            
    return battle

@router.post("/{battle_id}/submit")
def submit_battle_code(battle_id: str, req: BattleSubmitRequest):
    if battle_id not in _BATTLES:
        raise HTTPException(status_code=404, detail="Battle not found")
        
    battle = _BATTLES[battle_id]
    if battle["status"] != "ongoing":
        return battle
        
    p1 = battle["player1"]
    if p1["id"] == req.user_id:
        p1["passed"] = req.passed_tests
        p1["total"] = req.total_tests
        p1["progress"] = int((req.passed_tests / max(1, req.total_tests)) * 100)
        
        if req.passed_tests == req.total_tests:
            battle["status"] = "finished"
            battle["winner"] = p1["username"]
            p1["status"] = "accepted"
            
    return battle
