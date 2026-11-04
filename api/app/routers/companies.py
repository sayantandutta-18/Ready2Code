from typing import Optional, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/companies", tags=["companies"])

COMPANIES_DB = [
    {
        "slug": "google",
        "name": "Google",
        "tier": "Tier 1 Product",
        "rounds": 5,
        "ctc": "₹35 - ₹55 LPA",
        "target_topics": ["Graphs", "Dynamic Programming", "Trie", "Binary Search"],
        "problem_count": 84,
        "description": "Heavy focus on optimal time/space complexity, edge case handling, and clean modular code.",
        "schedule": [
            {"day": 1, "title": "Array Two-Pointers & Sliding Window", "problems": ["two-sum", "container-with-most-water", "longest-substring-without-repeating-characters"]},
            {"day": 2, "title": "Stack & Monotonic Queue Patterns", "problems": ["valid-parentheses", "min-stack", "daily-temperatures"]},
            {"day": 3, "title": "Linked List Reversals & Cycles", "problems": ["reverse-linked-list", "merge-two-sorted-lists", "linked-list-cycle"]},
            {"day": 4, "title": "Binary Search Variations & Rotated Arrays", "problems": ["binary-search", "search-in-rotated-sorted-array", "find-minimum-in-rotated-sorted-array"]},
            {"day": 5, "title": "Tree Traversals & Binary Search Trees", "problems": ["maximum-depth-of-binary-tree", "validate-binary-search-tree", "invert-binary-tree"]},
            {"day": 6, "title": "Graph BFS / DFS & Grid Traversal", "problems": ["number-of-islands", "rotting-oranges", "course-schedule"]},
            {"day": 7, "title": "Dynamic Programming 1D & 2D Foundations", "problems": ["climbing-stairs", "coin-change", "longest-common-subsequence"]},
            {"day": 8, "title": "Intervals & Greedy Scheduling", "problems": ["merge-intervals", "insert-interval", "non-overlapping-intervals"]}
        ]
    },
    {
        "slug": "amazon",
        "name": "Amazon",
        "tier": "Tier 1 Product",
        "rounds": 4,
        "ctc": "₹28 - ₹45 LPA",
        "target_topics": ["Arrays", "Trees", "BFS/DFS", "Sliding Window"],
        "problem_count": 112,
        "description": "Balanced DSA rounds combined with 16 Amazon Leadership Principles across every interview.",
        "schedule": [
            {"day": 1, "title": "Array Hashing & Two Pointers", "problems": ["two-sum", "product-of-array-except-self", "container-with-most-water"]},
            {"day": 2, "title": "Tree Inorder, Preorder & BFS", "problems": ["binary-tree-inorder-traversal", "binary-tree-level-order-traversal"]},
            {"day": 3, "title": "Priority Queue & Top K Elements", "problems": ["kth-largest-element-in-an-array", "top-k-frequent-elements"]},
            {"day": 4, "title": "Dynamic Programming & Knapsack", "problems": ["coin-change", "house-robber", "word-break"]}
        ]
    },
    {
        "slug": "microsoft",
        "name": "Microsoft",
        "tier": "Tier 1 Product",
        "rounds": 4,
        "ctc": "₹26 - ₹42 LPA",
        "target_topics": ["Linked List", "Strings", "Trees", "Stack"],
        "problem_count": 96,
        "description": "Standard algorithmic problem solving with deep dive into code correctness and test writing.",
        "schedule": [
            {"day": 1, "title": "String Parsing & Anagrams", "problems": ["valid-anagram", "group-anagrams", "valid-parentheses"]},
            {"day": 2, "title": "Linked List Merge & Reverse", "problems": ["reverse-linked-list", "merge-two-sorted-lists"]},
            {"day": 3, "title": "Tree LCA & Validations", "problems": ["lowest-common-ancestor-of-a-bst", "validate-binary-search-tree"]}
        ]
    },
    {
        "slug": "uber",
        "name": "Uber",
        "tier": "Tier 1 Product",
        "rounds": 4,
        "ctc": "₹34 - ₹58 LPA",
        "target_topics": ["Graphs", "Shortest Path", "Heaps", "Intervals"],
        "problem_count": 65,
        "description": "High bar on graph algorithms, concurrency, and low-latency system design fundamentals.",
        "schedule": [
            {"day": 1, "title": "Topological Sort & Dependencies", "problems": ["course-schedule"]},
            {"day": 2, "title": "Rotting Oranges & Multi-source BFS", "problems": ["rotting-oranges", "number-of-islands"]}
        ]
    },
    {
        "slug": "flipkart",
        "name": "Flipkart",
        "tier": "Top E-Commerce",
        "rounds": 4,
        "ctc": "₹24 - ₹38 LPA",
        "target_topics": ["Dynamic Programming", "Trees", "Machine Coding (LLD)"],
        "problem_count": 78,
        "description": "Famous for the 90-minute Machine Coding round requiring fully working, extensible OOP code.",
        "schedule": [
            {"day": 1, "title": "Grid Traversal & Shortest Paths", "problems": ["unique-paths", "number-of-islands"]}
        ]
    },
    {
        "slug": "atlassian",
        "name": "Atlassian",
        "tier": "Tier 1 SaaS",
        "rounds": 5,
        "ctc": "₹38 - ₹65 LPA",
        "target_topics": ["Data Structures", "OOP", "Concurrency"],
        "problem_count": 52,
        "description": "Collaborative pair programming rounds evaluating design choices, unit testing, and communication.",
        "schedule": [
            {"day": 1, "title": "Interval Merging & Processing", "problems": ["merge-intervals", "insert-interval"]}
        ]
    }
]

@router.get("")
def list_companies():
    return COMPANIES_DB

@router.get("/{slug}")
def get_company(slug: str):
    slug_norm = slug.lower().strip()
    for c in COMPANIES_DB:
        if c["slug"] == slug_norm:
            return c
    raise HTTPException(status_code=404, detail="Company track not found")
