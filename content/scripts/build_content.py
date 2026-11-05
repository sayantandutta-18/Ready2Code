import json, random, copy, zlib, inspect, os, re
from problems_bank import PROBLEMS, build, ser, ins, adj_from_edges, TN

OUT = "/mnt/user-data/outputs/content/problems"
os.makedirs(OUT, exist_ok=True)

SCENE_BY_TOPIC = {"stack": "stack", "linked_list": "linked_list", "trees": "tree", "graphs": "graph_grid",
                  "dp": "dp_table", "heap_greedy": "timeline"}
TOPIC_NAME = {"arrays": "Arrays and Hashing", "two_pointers": "Two Pointers and Sliding Window",
              "strings": "Strings", "stack": "Stack and Queue", "linked_list": "Linked List",
              "trees": "Trees", "graphs": "Graphs", "binary_search": "Binary Search",
              "dp": "Dynamic Programming", "heap_greedy": "Heap, Intervals and Greedy"}
HINTS = {
 "arrays": ["Scan the array once and ask what information you need about the values you have already seen.",
            "A hash map or a running value can replace a nested loop.",
            "Data structure: a hash map (dict). Store what you have seen; check each new value against it in O(1)."],
 "two_pointers": ["Think about what the two ends of the window or the two pointers tell you about the answer.",
                  "Move the pointer that cannot improve the answer, instead of trying all pairs.",
                  "Data structure: two integer indexes (left and right) moving in one pass, or a deque for a window."],
 "strings": ["Count characters or compare positions. Ask what each character needs in order to match.",
             "A hash map of counts, or a single pass that tracks state, usually works.",
             "Data structure: a dict or Counter for counts, or a stack for nested structure."],
 "stack": ["Think about which element has to wait until a later element is seen.",
           "Keep candidates in order. Pop when a new element resolves the ones on top.",
           "Data structure: a stack (Python list used with append and pop)."],
 "linked_list": ["Work out how the pointers (or positions) of the nodes must change.",
                 "Use two pointers, or first collect the values into a list and reason about indexes.",
                 "Data structure: two pointers (slow and fast), or a list of values to rebuild the order."],
 "trees": ["Think recursively: what does each subtree return to its parent?",
           "Visit nodes in a fixed order (depth-first) or level by level (breadth-first).",
           "Data structure: recursion (call stack) for depth-first, or a queue for level-order."],
 "graphs": ["Model the grid or edges as nodes and neighbours. Ask which nodes you can reach from where.",
            "Use a visited set so each node is processed once.",
            "Data structure: a queue for breadth-first search, a stack for depth-first search."],
 "binary_search": ["Ask whether the answer lies in the left or right half of the range.",
                   "Keep a range [lo, hi] and shrink it each step by looking at the middle value.",
                   "Data structure: two integer indexes lo and hi with mid = (lo + hi) // 2."],
 "dp": ["Break the problem into smaller versions of itself. What does the answer for size n depend on?",
        "Write the recurrence first, then decide whether you need the whole table or just the last few values.",
        "Data structure: a 1D or 2D array of subproblem answers, filled in order."],
 "heap_greedy": ["Ask which choice is safe to make right now and never needs to be undone.",
                 "Sorting by the right key often reveals the greedy order.",
                 "Data structure: a sorted list, or a heap (heapq) to repeatedly get the smallest or largest item."],
}
REF_TEXT = {
 "reverse-words": "return \" \".join(reversed(s.split()))",
 "longest-common-prefix": "return os.path.commonprefix(strs)",
 "run-length-encoding": "return \"\".join(k + str(len(list(g))) for k, g in groupby(s))",
 "reverse-linked-list": "return values[::-1]",
 "middle-of-linked-list": "return values[len(values) // 2:]",
 "merge-two-sorted-lists": "return sorted(list1 + list2)",
 "palindrome-linked-list": "return values == values[::-1]",
 "remove-linked-list-elements": "return [x for x in values if x != val]",
 "search-insert-position": "return bisect.bisect_left(nums, target)",
 "unique-paths": "return math.comb(m + n - 2, m - 1)",
 "integer-square-root": "return math.isqrt(x)",
}
ALIAS = {"longest-palindromic-substring-length": "longestPalindrome"}


def scene_for(p):
    if p["slug"] == "two-sum":
        return "array_with_map"
    return SCENE_BY_TOPIC.get(p["topic"], "array")


PRELUDE = (
    "import math, bisect, heapq, os\n"
    "from collections import Counter, defaultdict, deque\n"
    "from itertools import groupby\n\n"
    + inspect.getsource(TN) + "\n"
    + inspect.getsource(build) + "\n"
    + inspect.getsource(ser) + "\n"
    + inspect.getsource(ins) + "\n"
    + inspect.getsource(adj_from_edges) + "\n"
    + 'ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}\n'
)


def ref_source(p):
    if p["slug"] in REF_TEXT:
        return PRELUDE + f"\ndef {p['fn']}({', '.join(p['params'])}):\n    {REF_TEXT[p['slug']]}\n"
    src = inspect.getsource(p["sol"])
    return PRELUDE + "\n" + re.sub(r"^def \w+\(", f"def {p['fn']}(", src, count=1, flags=re.M)


def stmt_md(p):
    sig = f"{p['fn']}({', '.join(p['params'])})"
    return (p["statement"] + "\n\n**Function:** `" + sig + "`\n\n"
            "**Input:** one JSON value per parameter, in the order above. **Output:** the returned value as JSON.")


summary = []
for p in PROBLEMS:
    rng = random.Random(zlib.crc32(p["slug"].encode()))
    examples = []
    for args in p["examples"]:
        out = p["sol"](*copy.deepcopy(args))
        examples.append({"input": args, "output": out})
    hidden = []
    seen = set()
    tries = 0
    while len(hidden) < 10 and tries < 200:
        tries += 1
        args = p["gen"](rng)
        key = json.dumps(args)
        if key in seen:
            continue
        seen.add(key)
        hidden.append({"input": args, "output": p["sol"](*copy.deepcopy(args))})
    doc = {
        "slug": p["slug"],
        "title": p["title"],
        "topic": TOPIC_NAME[p["topic"]],
        "topic_key": p["topic"],
        "difficulty": p["difficulty"],
        "statement_md": stmt_md(p),
        "function_name": p["fn"],
        "params": p["params"],
        "examples": examples,
        "sample_tests": examples,
        "hidden_tests": hidden,
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "scene": scene_for(p),
        "hints": HINTS[p["topic"]],
        "starter_code": {"python": f"def {p['fn']}({', '.join(p['params'])}):\n    # Write your solution here\n    pass\n"},
        "reference_python": ref_source(p),
    }
    with open(os.path.join(OUT, p["slug"] + ".json"), "w") as f:
        json.dump(doc, f, indent=2)
    summary.append((p["slug"], p["title"], TOPIC_NAME[p["topic"]], p["difficulty"], len(hidden)))

with open("/mnt/user-data/outputs/content/index.json", "w") as f:
    json.dump([{"slug": s, "title": t, "topic": tp, "difficulty": d, "hidden_tests": h}
               for s, t, tp, d, h in summary], f, indent=2)
print("written", len(summary))
