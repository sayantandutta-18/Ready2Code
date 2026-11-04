import json
import os

os.makedirs("content/traces", exist_ok=True)

two_sum_trace = {
    "algo": "two_sum",
    "version": 1,
    "scene": "array_with_map",
    "input": { "nums": [2, 7, 11, 15], "target": 9 },
    "frames": [
        {
            "step": 0,
            "array": [2, 7, 11, 15],
            "pointers": {"i": 0},
            "map": {},
            "highlight": [],
            "note": "Initialize empty hash map. Start scanning from index 0 (val = 2)."
        },
        {
            "step": 1,
            "array": [2, 7, 11, 15],
            "pointers": {"i": 0},
            "map": {"2": 0},
            "highlight": [0],
            "note": "Target is 9. Complement 9 - 2 = 7 not in map. Store {2: 0} in map."
        },
        {
            "step": 2,
            "array": [2, 7, 11, 15],
            "pointers": {"i": 1},
            "map": {"2": 0},
            "highlight": [1],
            "note": "Move to index 1 (val = 7). Target is 9. Required complement is 9 - 7 = 2."
        },
        {
            "step": 3,
            "array": [2, 7, 11, 15],
            "pointers": {"i": 1},
            "map": {"2": 0},
            "highlight": [0, 1],
            "found": [0, 1],
            "note": "Complement 2 is found in map at index 0! Solution pair: indices [0, 1]."
        }
    ]
}

with open("content/traces/two-sum.json", "w", encoding="utf-8") as f:
    json.dump(two_sum_trace, f, indent=2)

bubble_sort_trace = {
    "algo": "bubble_sort",
    "version": 1,
    "scene": "array",
    "input": {"nums": [5, 3, 8, 4, 2]},
    "frames": [
        {"step": 0, "array": [5, 3, 8, 4, 2], "pointers": {"j": 0}, "highlight": [0, 1], "note": "Comparing 5 and 3. Since 5 > 3, swap them."},
        {"step": 1, "array": [3, 5, 8, 4, 2], "pointers": {"j": 1}, "highlight": [1, 2], "note": "Comparing 5 and 8. 5 <= 8, no swap needed."},
        {"step": 2, "array": [3, 5, 8, 4, 2], "pointers": {"j": 2}, "highlight": [2, 3], "note": "Comparing 8 and 4. Since 8 > 4, swap them."},
        {"step": 3, "array": [3, 5, 4, 8, 2], "pointers": {"j": 3}, "highlight": [3, 4], "note": "Comparing 8 and 2. Since 8 > 2, swap them."},
        {"step": 4, "array": [3, 5, 4, 2, 8], "pointers": {"j": 0}, "highlight": [4], "note": "Element 8 is in its correct sorted position."}
    ]
}

with open("content/traces/bubble-sort.json", "w", encoding="utf-8") as f:
    json.dump(bubble_sort_trace, f, indent=2)

print("Traces written successfully!")
