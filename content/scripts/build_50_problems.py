import json
import os
import copy
import random
import zlib
import inspect
import textwrap
import re
from collections import Counter, defaultdict, deque
import heapq
import bisect
import math

from problems_definitions_1_10 import add_problems_1_10
from problems_definitions_11_20 import add_problems_11_20
from problems_definitions_21_30 import add_problems_21_30
from problems_definitions_31_40 import add_problems_31_40
from problems_definitions_41_50 import add_problems_41_50

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "content", "problems"))
os.makedirs(OUT, exist_ok=True)

TOPIC_CONFIG = {
    "arrays": ("Arrays and Hashing", "array"),
    "two_pointers": ("Two Pointers and Sliding Window", "array"),
    "strings": ("Strings", "array"),
    "stack": ("Stack and Queue", "stack"),
    "linked_list": ("Linked List", "linked_list"),
    "trees": ("Trees", "tree"),
    "graphs": ("Graphs", "graph_grid"),
    "binary_search": ("Binary Search", "array"),
    "dp": ("Dynamic Programming", "dp_table"),
    "heap_greedy": ("Heap, Intervals and Greedy", "timeline"),
}

HINTS = {
    "arrays": [
        "Scan the array once and ask what information you need about the values you have already seen.",
        "A hash map or a running value can replace a nested loop.",
        "Data structure: a hash map (dict). Store what you have seen; check each new value against it in O(1)."
    ],
    "two_pointers": [
        "Think about what the two ends of the window or the two pointers tell you about the answer.",
        "Move the pointer that cannot improve the answer, instead of trying all pairs.",
        "Data structure: two integer indexes (left and right) moving in one pass, or a deque for a window."
    ],
    "strings": [
        "Count characters or compare positions. Ask what each character needs in order to match.",
        "A hash map of counts, or a single pass that tracks state, usually works.",
        "Data structure: a dict or Counter for counts, or a stack for nested structure."
    ],
    "stack": [
        "Think about which element has to wait until a later element is seen.",
        "Keep candidates in order. Pop when a new element resolves the ones on top.",
        "Data structure: a stack (Python list used with append and pop)."
    ],
    "linked_list": [
        "Work out how the pointers (or positions) of the nodes must change.",
        "Use two pointers, or first collect the values into a list and reason about indexes.",
        "Data structure: two pointers (slow and fast), or a list of values to rebuild the order."
    ],
    "trees": [
        "Think recursively: what does each subtree return to its parent?",
        "Visit nodes in a fixed order (depth-first) or level by level (breadth-first).",
        "Data structure: recursion (call stack) for depth-first, or a queue for level-order."
    ],
    "graphs": [
        "Model the grid or edges as nodes and neighbours. Ask which nodes you can reach from where.",
        "Use a visited set so each node is processed once.",
        "Data structure: a queue for breadth-first search, a stack for depth-first search."
    ],
    "binary_search": [
        "Ask whether the answer lies in the left or right half of the range.",
        "Keep a range [lo, hi] and shrink it each step by looking at the middle value.",
        "Data structure: two integer indexes lo and hi with mid = (lo + hi) // 2."
    ],
    "dp": [
        "Break the problem into smaller versions of itself. What does the answer for size n depend on?",
        "Write the recurrence first, then decide whether you need the whole table or just the last few values.",
        "Data structure: a 1D or 2D array of subproblem answers, filled in order."
    ],
    "heap_greedy": [
        "Ask which choice is safe to make right now and never needs to be undone.",
        "Sorting by the right key often reveals the greedy order.",
        "Data structure: a sorted list, or a heap (heapq) to repeatedly get the smallest or largest item."
    ],
}

PRELUDE = '''import math, bisect, heapq, os
from collections import Counter, defaultdict, deque
from itertools import groupby

class TN:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build(a):
    if not a or a[0] is None:
        return None
    root = TN(a[0]); q = deque([root]); i = 1
    while q and i < len(a):
        node = q.popleft()
        if i < len(a) and a[i] is not None:
            node.left = TN(a[i]); q.append(node.left)
        i += 1
        if i < len(a) and a[i] is not None:
            node.right = TN(a[i]); q.append(node.right)
        i += 1
    return root

def ser(root):
    out = []; q = deque([root])
    while q:
        n = q.popleft()
        if n is None:
            out.append(None); continue
        out.append(n.val); q.append(n.left); q.append(n.right)
    while out and out[-1] is None:
        out.pop()
    return out

def ins(root, v):
    if root is None:
        return TN(v)
    if v < root.val:
        root.left = ins(root.left, v)
    else:
        root.right = ins(root.right, v)
    return root

def adj_from_edges(n, edges):
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b); g[b].append(a)
    return g

ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
'''

NEW_PROBLEMS = []

def register_problem(slug, title, topic_key, diff, statement, fn, params, examples, sol, gen, custom_hints=None):
    NEW_PROBLEMS.append({
        "slug": slug,
        "title": title,
        "topic_key": topic_key,
        "difficulty": diff,
        "statement": statement,
        "fn": fn,
        "params": params,
        "examples": examples,
        "sol": sol,
        "gen": gen,
        "custom_hints": custom_hints
    })

# Register all 50 problems
add_problems_1_10(register_problem)
add_problems_11_20(register_problem)
add_problems_21_30(register_problem)
add_problems_31_40(register_problem)
add_problems_41_50(register_problem)

print(f"Total registered new problems: {len(NEW_PROBLEMS)}")

def ref_source(p):
    raw_src = textwrap.dedent(inspect.getsource(p["sol"]))
    # Replace the def sol_*(...) with def fn(...)
    clean_src = re.sub(r"^def \w+\(", f"def {p['fn']}(", raw_src, count=1, flags=re.M)
    return PRELUDE + "\n" + clean_src + "\n"

def stmt_md(p):
    sig = f"{p['fn']}({', '.join(p['params'])})"
    return (p["statement"] + "\n\n**Function:** `" + sig + "`\n\n"
            "**Input:** one JSON value per parameter, in the order above. **Output:** the returned value as JSON.")

created_slugs = []

for p in NEW_PROBLEMS:
    rng = random.Random(zlib.crc32(p["slug"].encode()))
    examples = []
    for test in p["examples"]:
        args, exp_out = test[0], test[1]
        calc_out = p["sol"](*copy.deepcopy(args))
        if calc_out != exp_out:
            raise ValueError(f"Example mismatch for {p['slug']}: got {calc_out}, expected {exp_out}")
        examples.append({"input": args, "output": exp_out})

    hidden = []
    seen = set()
    tries = 0
    while len(hidden) < 10 and tries < 500:
        tries += 1
        args = p["gen"](rng)
        key = json.dumps(args, sort_keys=True)
        if key in seen:
            continue
        seen.add(key)
        try:
            out = p["sol"](*copy.deepcopy(args))
            hidden.append({"input": args, "output": out})
        except Exception as e:
            print(f"Error generating test for {p['slug']}: {e}")
            continue

    if len(hidden) < 8:
        raise ValueError(f"Failed to generate >= 8 hidden tests for {p['slug']}: generated {len(hidden)}")

    topic_name, scene = TOPIC_CONFIG[p["topic_key"]]
    doc = {
        "slug": p["slug"],
        "title": p["title"],
        "topic": topic_name,
        "topic_key": p["topic_key"],
        "difficulty": p["difficulty"],
        "statement_md": stmt_md(p),
        "function_name": p["fn"],
        "params": p["params"],
        "examples": examples,
        "sample_tests": examples,
        "hidden_tests": hidden,
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "scene": scene,
        "hints": p["custom_hints"] or HINTS[p["topic_key"]],
        "starter_code": {
            "python": f"def {p['fn']}({', '.join(p['params'])}):\n    # Write your solution here\n    pass\n"
        },
        "reference_python": ref_source(p),
    }

    file_path = os.path.join(OUT, f"{p['slug']}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2)

    created_slugs.append(p["slug"])

print(f"Successfully generated {len(created_slugs)} problem files in content/problems/")
