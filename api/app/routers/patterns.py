import json
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.entities import Pattern, PatternQuiz, Problem

router = APIRouter(prefix="/patterns", tags=["patterns"])

class SubmitQuizRequest(BaseModel):
    user_id: str = "guest"
    pattern_slug: str
    selected_option_index: int

PATTERNS_CATALOG = [
    {
        "slug": "two-pointers",
        "name": "Two Pointers",
        "order_index": 1,
        "signals": "Sorted arrays, searching for pairs, palindromes, in-place partitions.",
        "lesson_md": """### Pattern: Two Pointers
Two pointers iterate through the data structure from opposite ends or at different speeds.

#### Key Signals in Problem Statements:
- Array is sorted or order can be sorted in $O(n \\log n)$.
- Target involves pair sums, triplets, or subsegments.
- Requires $O(1)$ auxiliary space without extra allocations.
""",
        "template_code": """def two_pointers(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        # evaluate condition
        if condition(nums[left], nums[right]):
            left += 1
        else:
            right -= 1""",
        "quiz_question": "You need to find two numbers in an already sorted ascending array that sum to $K$ using $O(1)$ extra space. Which technique is optimal?",
        "options": ["Two Pointers (converging inward)", "Breadth-First Search", "Segment Tree", "Topological Sort"],
        "correct_option_index": 0
    },
    {
        "slug": "sliding-window",
        "name": "Sliding Window",
        "order_index": 2,
        "signals": "Contiguous subarrays, longest/shortest substrings, max sum of size K.",
        "lesson_md": """### Pattern: Sliding Window
Maintains a window `[left, right]` that expands to include valid elements and shrinks when constraints are violated.

#### Key Signals:
- Finding longest/shortest contiguous sequence matching criteria.
- Target constraint: at most $K$ distinct elements or max sum.
""",
        "template_code": """def sliding_window(s):
    left = 0
    state = {}
    best = 0
    for right, c in enumerate(s):
        state[c] = state.get(c, 0) + 1
        while not valid(state):
            state[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best""",
        "quiz_question": "Given a string $s$, find the length of the longest substring with at most two distinct characters. Which pattern directly applies?",
        "options": ["Sliding Window with character frequency hash map", "Floyd-Warshall algorithm", "Binary Indexed Tree", "Morris Traversal"],
        "correct_option_index": 0
    },
    {
        "slug": "fast-and-slow-pointers",
        "name": "Fast & Slow Pointers (Floyd's Cycle)",
        "order_index": 3,
        "signals": "Cycle detection in linked list, finding middle node, happy numbers.",
        "lesson_md": """### Pattern: Fast and Slow Pointers
Move `slow` one step and `fast` two steps. If a cycle exists, they will inevitably collide.
""",
        "template_code": """def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False""",
        "quiz_question": "How do you detect if a singly linked list contains a cycle using $O(1)$ space?",
        "options": ["Floyd's Tortoise and Hare (Slow/Fast pointers)", "Store nodes in an adjacency matrix", "Run Dijkstra's algorithm", "Recursively reverse each node"],
        "correct_option_index": 0
    },
    {
        "slug": "monotonic-stack",
        "name": "Monotonic Stack",
        "order_index": 4,
        "signals": "Next greater element, largest rectangle in histogram, daily temperatures.",
        "lesson_md": """### Pattern: Monotonic Stack
A stack maintaining strictly increasing or decreasing elements.
""",
        "template_code": """def next_greater(nums):
    res = [-1] * len(nums)
    stack = []
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            idx = stack.pop()
            res[idx] = x
        stack.append(i)
    return res""",
        "quiz_question": "Find the number of days until a warmer temperature for every day in an array. Optimal approach?",
        "options": ["Monotonic Decreasing Stack storing indices", "Nested loops scanning O(n²)", "Prim's Minimum Spanning Tree", "Bit manipulation"],
        "correct_option_index": 0
    },
    {
        "slug": "bfs-breadth-first-search",
        "name": "Breadth-First Search (BFS)",
        "order_index": 5,
        "signals": "Shortest path in unweighted graphs, level-order traversal, word ladder.",
        "lesson_md": """### Pattern: BFS
Explores graph or tree layer by layer using a FIFO queue.
""",
        "template_code": """def bfs(start):
    q = deque([start])
    visited = {start}
    while q:
        curr = q.popleft()
        for nbr in neighbors(curr):
            if nbr not in visited:
                visited.add(nbr)
                q.append(nbr)""",
        "quiz_question": "To find the minimum number of knight moves on a chessboard from start to destination, which search should you use?",
        "options": ["BFS using a Queue", "DFS with unlimited recursion depth", "QuickSort", "Kruskal's algorithm"],
        "correct_option_index": 0
    }
]

@router.get("")
def list_patterns():
    return [
        {
            "slug": p["slug"],
            "name": p["name"],
            "order_index": p["order_index"],
            "signals": p["signals"]
        }
        for p in PATTERNS_CATALOG
    ]

@router.get("/{slug}")
def get_pattern(slug: str):
    p = next((x for x in PATTERNS_CATALOG if x["slug"] == slug), None)
    if not p:
        raise HTTPException(status_code=404, detail="Pattern not found")
    return {
        "slug": p["slug"],
        "name": p["name"],
        "signals": p["signals"],
        "lesson_md": p["lesson_md"],
        "template_code": p["template_code"],
        "quiz": {
            "question": p["quiz_question"],
            "options": p["options"]
        }
    }

@router.post("/{slug}/quiz")
def submit_quiz(slug: str, req: SubmitQuizRequest):
    p = next((x for x in PATTERNS_CATALOG if x["slug"] == slug), None)
    if not p:
        raise HTTPException(status_code=404, detail="Pattern not found")

    is_correct = (req.selected_option_index == p["correct_option_index"])
    return {
        "correct": is_correct,
        "message": "Pattern unlocked! All problems matching this pattern are now accessible." if is_correct else "Incorrect. Review the pattern signals and try again.",
        "xp_earned": 15 if is_correct else 0
    }
