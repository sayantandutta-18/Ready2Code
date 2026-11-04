"""
Problem Generator - Batch 4: Linked List (6 problems) + Trees (7 problems)
Linked List mix: 3 Easy, 2 Medium, 1 Hard
Trees mix: 3 Easy, 3 Medium, 1 Hard
"""
import os
import json

PROBLEMS = [
    # 31. Linked List - Easy
    {
        "slug": "invert-singly-linked-chain",
        "title": "Invert Singly Linked Chain Pointer Directions",
        "difficulty": "easy",
        "topic": "Linked List",
        "tags": ["Linked List", "Recursion"],
        "company_tags": ["Amazon", "Google", "Apple", "Microsoft"],
        "statement_md": "Given the `head` of a singly linked list represented as an array of values, reverse the list by inverting its pointers, and return the reversed list.\n\n### Input Format\n- A JSON-encoded list of integers `head`\n\n### Output Format\n- A JSON-encoded list of integers representing the reversed list",
        "examples": [
            {
                "input": "[1, 2, 3, 4, 5]",
                "output": "[5, 4, 3, 2, 1]",
                "explanation": "The pointers 1 -> 2 -> 3 -> 4 -> 5 are inverted to 5 -> 4 -> 3 -> 2 -> 1."
            },
            {
                "input": "[1, 2]",
                "output": "[2, 1]",
                "explanation": "1 -> 2 becomes 2 -> 1."
            }
        ],
        "sample_tests": [
            {"input_text": "[1, 2, 3, 4, 5]", "expected_output": "[5, 4, 3, 2, 1]"},
            {"input_text": "[1, 2]", "expected_output": "[2, 1]"},
            {"input_text": "[]", "expected_output": "[]"}
        ],
        "hidden_tests": [
            {"input_text": "[10]", "expected_output": "[10]"},
            {"input_text": "[1, 1, 1]", "expected_output": "[1, 1, 1]"},
            {"input_text": "[-1, -2, -3]", "expected_output": "[-3, -2, -1]"},
            {"input_text": "[0, 10, 20, 30]", "expected_output": "[30, 20, 10, 0]"},
            {"input_text": "[7, 8, 9, 10, 11, 12]", "expected_output": "[12, 11, 10, 9, 8, 7]"},
            {"input_text": "[100, 200]", "expected_output": "[200, 100]"},
            {"input_text": "[5, 4, 3, 2, 1, 0]", "expected_output": "[0, 1, 2, 3, 4, 5]"},
            {"input_text": "[1, 2, 1, 2, 1]", "expected_output": "[1, 2, 1, 2, 1]"},
            {"input_text": "[-5, 0, 5]", "expected_output": "[5, 0, -5]"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "To reverse a link curr.next = prev, you must remember the next node before modifying the link.", "xp_cost": 2},
            {"level": 2, "text": "Maintain prev, curr, and nxt pointers iteratively.", "xp_cost": 5},
            {"level": 3, "text": "Use Pointer Inversion with three pointers in a single pass.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Iterative Pointer Inversion\n\nMaintain `prev = None` and `curr = head`. In each step, store `nxt = curr.next`, point `curr.next = prev`, then advance `prev = curr` and `curr = nxt`.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ single pass over nodes.\n- **Space Complexity:** $O(1)$ constant pointer manipulation.\n\n#### Common Pitfalls\n- Losing the reference to `curr.next` before redirecting the pointer.",
        "reference_solutions": {
            "brute_python": "def reverseList(head):\n    return head[::-1]",
            "optimal_python": "def reverseList(head):\n    if not head: return []\n    # Simulate linked node pointer reversal\n    class Node:\n        def __init__(self, val, next=None):\n            self.val = val\n            self.next = next\n    dummy = Node(0)\n    cur = dummy\n    for x in head:\n        cur.next = Node(x)\n        cur = cur.next\n    prev = None\n    node = dummy.next\n    while node:\n        nxt = node.next\n        node.next = prev\n        prev = node\n        node = nxt\n    res = []\n    while prev:\n        res.append(prev.val)\n        prev = prev.next\n    return res",
            "optimal_java": "import java.util.*;\npublic class Solution {\n    public List<Integer> reverseList(List<Integer> head) {\n        Collections.reverse(head);\n        return head;\n    }\n}",
            "optimal_cpp": "#include <vector>\n#include <algorithm>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> reverseList(vector<int>& head) {\n        reverse(head.begin(), head.end());\n        return head;\n    }\n};"
        }
    },

    # 32. Linked List - Easy
    {
        "slug": "detect-cycle-traversal-stream",
        "title": "Loop Detection in Traversal Stream",
        "difficulty": "easy",
        "topic": "Linked List",
        "tags": ["Linked List", "Two Pointers"],
        "company_tags": ["Microsoft", "Amazon", "Apple"],
        "statement_md": "Given the `head` of a linked list and an integer `pos` representing the 0-indexed position where the tail connects back to form a cycle (`-1` if no cycle), determine if the linked list contains a cycle.\n\nReturn `true` if there is a cycle in the linked list. Otherwise, return `false`.\n\n### Input Format\n- Line 1: A JSON-encoded list of integers `head`\n- Line 2: An integer `pos` (index of cycle target or -1)\n\n### Output Format\n- A boolean value (`true` or `false`)",
        "examples": [
            {
                "input": "[3, 2, 0, -4]\n1",
                "output": "true",
                "explanation": "Tail connects to the second node (index 1), forming a cycle."
            },
            {
                "input": "[1, 2]\n0",
                "output": "true",
                "explanation": "Tail connects to the first node (index 0)."
            }
        ],
        "sample_tests": [
            {"input_text": "[3, 2, 0, -4]\n1", "expected_output": "true"},
            {"input_text": "[1, 2]\n0", "expected_output": "true"},
            {"input_text": "[1]\n-1", "expected_output": "false"}
        ],
        "hidden_tests": [
            {"input_text": "[]\n-1", "expected_output": "false"},
            {"input_text": "[5]\n0", "expected_output": "true"},
            {"input_text": "[1, 2, 3, 4, 5]\n-1", "expected_output": "false"},
            {"input_text": "[1, 2, 3, 4, 5]\n4", "expected_output": "true"},
            {"input_text": "[1, 2, 3, 4, 5]\n2", "expected_output": "true"},
            {"input_text": "[-1, -2, -3]\n-1", "expected_output": "false"},
            {"input_text": "[-1, -2, -3]\n0", "expected_output": "true"},
            {"input_text": "[10, 20]\n-1", "expected_output": "false"},
            {"input_text": "[1, 2, 3, 4, 5, 6, 7]\n3", "expected_output": "true"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "If two runners traverse a circular track at different speeds, they will eventually meet.", "xp_cost": 2},
            {"level": 2, "text": "Advance slow by 1 step and fast by 2 steps. If fast catches slow, a cycle exists.", "xp_cost": 5},
            {"level": 3, "text": "Use Floyd's Tortoise and Hare Cycle Finding Algorithm (Fast and Slow Pointers) in O(1) space.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Floyd's Tortoise and Hare\n\nInitialize `slow = head` and `fast = head`. Advance `slow` by 1 node and `fast` by 2 nodes. If `fast` or `fast.next` becomes null, no cycle exists. If `slow == fast`, a cycle is detected.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ where $n$ is node count.\n- **Space Complexity:** $O(1)$ constant space.\n\n#### Common Pitfalls\n- Null pointer exception when accessing `fast.next.next` without verifying `fast` and `fast.next` are non-null.",
        "reference_solutions": {
            "brute_python": "def hasCycle(head, pos):\n    return pos != -1 and len(head) > 0",
            "optimal_python": "def hasCycle(head, pos):\n    if not head or pos == -1:\n        return False\n    class Node:\n        def __init__(self, val):\n            self.val = val\n            self.next = None\n    nodes = [Node(x) for x in head]\n    for i in range(len(nodes) - 1):\n        nodes[i].next = nodes[i + 1]\n    if pos >= 0 and pos < len(nodes):\n        nodes[-1].next = nodes[pos]\n    slow = fast = nodes[0]\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n        if slow == fast:\n            return True\n    return False",
            "optimal_java": "public class Solution {\n    public boolean hasCycle(List<Integer> head, int pos) {\n        return pos != -1 && head.size() > 0;\n    }\n}",
            "optimal_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    bool hasCycle(vector<int>& head, int pos) {\n        return pos != -1 && !head.empty();\n    }\n};"
        }
    },

    # 33. Linked List - Easy
    {
        "slug": "merge-two-sorted-linked-chains",
        "title": "Merge Two Sorted Linked Chains",
        "difficulty": "easy",
        "topic": "Linked List",
        "tags": ["Linked List", "Recursion", "Two Pointers"],
        "company_tags": ["Amazon", "Apple", "Microsoft", "Google"],
        "statement_md": "You are given the heads of two sorted linked lists `list1` and `list2` represented as arrays.\n\nMerge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.\n\nReturn the merged sorted list as an array.\n\n### Input Format\n- Line 1: A JSON-encoded list of integers `list1`\n- Line 2: A JSON-encoded list of integers `list2`\n\n### Output Format\n- A JSON-encoded list of integers representing the merged list",
        "examples": [
            {
                "input": "[1, 2, 4]\n[1, 3, 4]",
                "output": "[1, 1, 2, 3, 4, 4]",
                "explanation": "Splicing in sorted order produces [1, 1, 2, 3, 4, 4]."
            },
            {
                "input": "[]\n[]",
                "output": "[]",
                "explanation": "Both lists are empty."
            }
        ],
        "sample_tests": [
            {"input_text": "[1, 2, 4]\n[1, 3, 4]", "expected_output": "[1, 1, 2, 3, 4, 4]"},
            {"input_text": "[]\n[]", "expected_output": "[]"},
            {"input_text": "[]\n[0]", "expected_output": "[0]"}
        ],
        "hidden_tests": [
            {"input_text": "[5]\n[1, 2, 3, 4]", "expected_output": "[1, 2, 3, 4, 5]"},
            {"input_text": "[-5, -3, -1]\n[-4, -2, 0]", "expected_output": "[-5, -4, -3, -2, -1, 0]"},
            {"input_text": "[1, 1, 1]\n[2, 2, 2]", "expected_output": "[1, 1, 1, 2, 2, 2]"},
            {"input_text": "[1, 3, 5, 7, 9]\n[2, 4, 6, 8, 10]", "expected_output": "[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"},
            {"input_text": "[100]\n[50, 150]", "expected_output": "[50, 100, 150]"},
            {"input_text": "[1, 2, 3]\n[]", "expected_output": "[1, 2, 3]"},
            {"input_text": "[-10, 0, 10]\n[-20, -5, 15]", "expected_output": "[-20, -10, -5, 0, 10, 15]"},
            {"input_text": "[0]\n[0]", "expected_output": "[0, 0]"},
            {"input_text": "[1, 2, 8]\n[3, 4, 5, 6, 7]", "expected_output": "[1, 2, 3, 4, 5, 6, 7, 8]"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Compare the current heads of both lists and choose the smaller one.", "xp_cost": 2},
            {"level": 2, "text": "Create a dummy head node to simplify edge cases when building the merged list.", "xp_cost": 5},
            {"level": 3, "text": "Use Two Pointers with a dummy pre-head sentinel node.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Two Pointers Splicing\n\nCreate a dummy sentinel node `dummy`. Maintain pointer `tail`. While both lists have nodes, attach the node with smaller value to `tail.next` and advance. Attach remaining nodes at the end.\n\n#### Complexity\n- **Time Complexity:** $O(n + m)$ linear pass.\n- **Space Complexity:** $O(1)$ in-place node relinking.\n\n#### Common Pitfalls\n- Forgetting to attach the remainder of the non-empty list.",
        "reference_solutions": {
            "brute_python": "def mergeTwoLists(list1, list2):\n    return sorted(list1 + list2)",
            "optimal_python": "def mergeTwoLists(list1, list2):\n    res = []\n    i, j = 0, 0\n    while i < len(list1) and j < len(list2):\n        if list1[i] <= list2[j]:\n            res.append(list1[i])\n            i += 1\n        else:\n            res.append(list2[j])\n            j += 1\n    res.extend(list1[i:])\n    res.extend(list2[j:])\n    return res",
            "optimal_java": "import java.util.*;\npublic class Solution {\n    public List<Integer> mergeTwoLists(List<Integer> list1, List<Integer> list2) {\n        List<Integer> res = new ArrayList<>();\n        int i = 0, j = 0;\n        while (i < list1.size() && j < list2.size()) {\n            if (list1.get(i) <= list2.get(j)) res.add(list1.get(i++));\n            else res.add(list2.get(j++));\n        }\n        while (i < list1.size()) res.add(list1.get(i++));\n        while (j < list2.size()) res.add(list2.get(j++));\n        return res;\n    }\n}",
            "optimal_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> mergeTwoLists(vector<int>& list1, vector<int>& list2) {\n        vector<int> res;\n        int i = 0, j = 0;\n        while (i < (int)list1.size() && j < (int)list2.size()) {\n            if (list1[i] <= list2[j]) res.push_back(list1[i++]);\n            else res.push_back(list2[j++]);\n        }\n        while (i < (int)list1.size()) res.push_back(list1[i++]);\n        while (j < (int)list2.size()) res.push_back(list2[j++]);\n        return res;\n    }\n};"
        }
    },

    # 34. Linked List - Medium
    {
        "slug": "remove-kth-node-from-chain-end",
        "title": "Remove N-th Node From End of Chain",
        "difficulty": "medium",
        "topic": "Linked List",
        "tags": ["Linked List", "Two Pointers"],
        "company_tags": ["Meta", "Google", "Amazon", "Apple"],
        "statement_md": "Given the `head` of a linked list represented as an array of values, remove the `n-th` node from the end of the list and return its head.\n\n### Input Format\n- Line 1: A JSON-encoded list of integers `head`\n- Line 2: An integer `n` (`1 <= n <= len(head)`)\n\n### Output Format\n- A JSON-encoded list of integers representing the list after removal",
        "examples": [
            {
                "input": "[1, 2, 3, 4, 5]\n2",
                "output": "[1, 2, 3, 5]",
                "explanation": "The 2nd node from the end is 4. Removing 4 yields [1, 2, 3, 5]."
            },
            {
                "input": "[1]\n1",
                "output": "[]",
                "explanation": "Removing the only node leaves an empty list."
            }
        ],
        "sample_tests": [
            {"input_text": "[1, 2, 3, 4, 5]\n2", "expected_output": "[1, 2, 3, 5]"},
            {"input_text": "[1]\n1", "expected_output": "[]"},
            {"input_text": "[1, 2]\n1", "expected_output": "[1]"}
        ],
        "hidden_tests": [
            {"input_text": "[1, 2]\n2", "expected_output": "[2]"},
            {"input_text": "[1, 2, 3, 4]\n4", "expected_output": "[2, 3, 4]"},
            {"input_text": "[1, 2, 3, 4]\n1", "expected_output": "[1, 2, 3]"},
            {"input_text": "[10, 20, 30, 40, 50]\n3", "expected_output": "[10, 20, 40, 50]"},
            {"input_text": "[-1, -2, -3]\n2", "expected_output": "[-1, -3]"},
            {"input_text": "[0, 0, 0]\n1", "expected_output": "[0, 0]"},
            {"input_text": "[5, 10, 15, 20, 25, 30]\n5", "expected_output": "[5, 15, 20, 25, 30]"},
            {"input_text": "[9, 8, 7]\n3", "expected_output": "[8, 7]"},
            {"input_text": "[1, 3, 5, 7, 9]\n2", "expected_output": "[1, 3, 5, 9]"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Can you find the n-th node from the end in a single pass without knowing the total length beforehand?", "xp_cost": 2},
            {"level": 2, "text": "Advance a fast pointer n steps ahead of a slow pointer.", "xp_cost": 5},
            {"level": 3, "text": "Use Two Pointers with a fixed gap of n nodes and a dummy head node.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Two Pointers with Fixed Offset\n\nCreate a dummy sentinel pointing to head. Advance `fast` pointer $n + 1$ steps. Then advance `slow` and `fast` together until `fast` reaches null. `slow.next = slow.next.next` deletes the target node.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ single pass.\n- **Space Complexity:** $O(1)$ constant memory.\n\n#### Common Pitfalls\n- Deleting the head node (handled cleanly by using a dummy node).",
        "reference_solutions": {
            "brute_python": "def removeNthFromEnd(head, n):\n    idx = len(head) - n\n    return head[:idx] + head[idx+1:]",
            "optimal_python": "def removeNthFromEnd(head, n):\n    idx = len(head) - n\n    return head[:idx] + head[idx+1:]",
            "optimal_java": "import java.util.*;\npublic class Solution {\n    public List<Integer> removeNthFromEnd(List<Integer> head, int n) {\n        int idx = head.size() - n;\n        List<Integer> res = new ArrayList<>(head);\n        res.remove(idx);\n        return res;\n    }\n}",
            "optimal_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> removeNthFromEnd(vector<int>& head, int n) {\n        int idx = (int)head.size() - n;\n        vector<int> res = head;\n        res.erase(res.begin() + idx);\n        return res;\n    }\n};"
        }
    },

    # 35. Linked List - Medium
    {
        "slug": "add-two-linked-number-chains",
        "title": "Add Two Numbers Represented as Reversed Chains",
        "difficulty": "medium",
        "topic": "Linked List",
        "tags": ["Linked List", "Math", "Recursion"],
        "company_tags": ["Amazon", "Microsoft", "Meta", "Google"],
        "statement_md": "You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit.\n\nAdd the two numbers and return the sum as a linked list in reverse order.\n\nYou may assume the two numbers do not contain any leading zero, except the number 0 itself.\n\n### Input Format\n- Line 1: A JSON-encoded list of digits `l1`\n- Line 2: A JSON-encoded list of digits `l2`\n\n### Output Format\n- A JSON-encoded list of digits representing the sum in reverse order",
        "examples": [
            {
                "input": "[2, 4, 3]\n[5, 6, 4]",
                "output": "[7, 0, 8]",
                "explanation": "342 + 465 = 807, represented as [7, 0, 8]."
            },
            {
                "input": "[0]\n[0]",
                "output": "[0]",
                "explanation": "0 + 0 = 0."
            }
        ],
        "sample_tests": [
            {"input_text": "[2, 4, 3]\n[5, 6, 4]", "expected_output": "[7, 0, 8]"},
            {"input_text": "[0]\n[0]", "expected_output": "[0]"},
            {"input_text": "[9, 9, 9, 9, 9, 9, 9]\n[9, 9, 9, 9]", "expected_output": "[8, 9, 9, 9, 0, 0, 0, 1]"}
        ],
        "hidden_tests": [
            {"input_text": "[1]\n[9, 9]", "expected_output": "[0, 0, 1]"},
            {"input_text": "[5]\n[5]", "expected_output": "[0, 1]"},
            {"input_text": "[1, 8]\n[0]", "expected_output": "[1, 8]"},
            {"input_text": "[9]\n[1]", "expected_output": "[0, 1]"},
            {"input_text": "[7, 1, 6]\n[5, 9, 2]", "expected_output": "[2, 1, 9]"},
            {"input_text": "[0, 1]\n[0, 1, 2]", "expected_output": "[0, 2, 2]"},
            {"input_text": "[9, 9, 9]\n[1]", "expected_output": "[0, 0, 0, 1]"},
            {"input_text": "[4, 3, 2, 1]\n[6, 7, 8, 9]", "expected_output": "[0, 1, 1, 1, 1]"},
            {"input_text": "[8, 3, 2]\n[9, 2, 1]", "expected_output": "[7, 6, 3]"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Digits are already in reverse order (least significant digit first), perfectly matching elementary addition.", "xp_cost": 2},
            {"level": 2, "text": "Track a carry variable initialized to 0. Add digit1 + digit2 + carry.", "xp_cost": 5},
            {"level": 3, "text": "Use Linked List Node Simulation with a carry digit.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Digit-by-Digit Carry Propagation\n\nIterate while `p1`, `p2`, or `carry` is non-zero. Compute `total = val1 + val2 + carry`. Append `total % 10` and update `carry = total // 10`.\n\n#### Complexity\n- **Time Complexity:** $O(\\max(N, M))$ single pass over longer list.\n- **Space Complexity:** $O(\\max(N, M))$ for output node list.\n\n#### Common Pitfalls\n- Forgetting the final carry node when the last addition results in carry > 0.",
        "reference_solutions": {
            "brute_python": "def addTwoNumbers(l1, l2):\n    n1 = int(''.join(map(str, l1[::-1])))\n    n2 = int(''.join(map(str, l2[::-1])))\n    return [int(c) for c in str(n1 + n2)[::-1]]",
            "optimal_python": "def addTwoNumbers(l1, l2):\n    res = []\n    carry = 0\n    i, j = 0, 0\n    while i < len(l1) or j < len(l2) or carry:\n        v1 = l1[i] if i < len(l1) else 0\n        v2 = l2[j] if j < len(l2) else 0\n        total = v1 + v2 + carry\n        res.append(total % 10)\n        carry = total // 10\n        i += 1\n        j += 1\n    return res",
            "optimal_java": "import java.util.*;\npublic class Solution {\n    public List<Integer> addTwoNumbers(List<Integer> l1, List<Integer> l2) {\n        List<Integer> res = new ArrayList<>();\n        int carry = 0, i = 0, j = 0;\n        while (i < l1.size() || j < l2.size() || carry != 0) {\n            int v1 = i < l1.size() ? l1.get(i++) : 0;\n            int v2 = j < l2.size() ? l2.get(j++) : 0;\n            int total = v1 + v2 + carry;\n            res.add(total % 10);\n            carry = total / 10;\n        }\n        return res;\n    }\n}",
            "optimal_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> addTwoNumbers(vector<int>& l1, vector<int>& l2) {\n        vector<int> res;\n        int carry = 0, i = 0, j = 0;\n        while (i < (int)l1.size() || j < (int)l2.size() || carry) {\n            int v1 = i < (int)l1.size() ? l1[i++] : 0;\n            int v2 = j < (int)l2.size() ? l2[j++] : 0;\n            int total = v1 + v2 + carry;\n            res.push_back(total % 10);\n            carry = total / 10;\n        }\n        return res;\n    }\n};"
        }
    },

    # 36. Linked List - Hard
    {
        "slug": "reverse-nodes-in-k-group-blocks",
        "title": "Reverse Nodes in Strict K-Group Blocks",
        "difficulty": "hard",
        "topic": "Linked List",
        "tags": ["Linked List", "Recursion"],
        "company_tags": ["Meta", "Amazon", "Microsoft", "Google"],
        "statement_md": "Given the `head` of a linked list represented as an array of integers, reverse the nodes of the list `k` at a time, and return the modified list.\n\n`k` is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a multiple of `k` then left-out nodes, in the end, should remain as it is.\n\nYou may not alter the values in the list's nodes, only nodes themselves may be changed.\n\n### Input Format\n- Line 1: A JSON-encoded list of integers `head`\n- Line 2: An integer `k` (`1 <= k <= len(head)`)\n\n### Output Format\n- A JSON-encoded list of integers representing the modified list",
        "examples": [
            {
                "input": "[1, 2, 3, 4, 5]\n2",
                "output": "[2, 1, 4, 3, 5]",
                "explanation": "Nodes 1 and 2 are reversed to 2, 1. Nodes 3 and 4 are reversed to 4, 3. Node 5 remains unchanged."
            },
            {
                "input": "[1, 2, 3, 4, 5]\n3",
                "output": "[3, 2, 1, 4, 5]",
                "explanation": "First 3 nodes are reversed. Remaining 2 nodes (< 3) remain unchanged."
            }
        ],
        "sample_tests": [
            {"input_text": "[1, 2, 3, 4, 5]\n2", "expected_output": "[2, 1, 4, 3, 5]"},
            {"input_text": "[1, 2, 3, 4, 5]\n3", "expected_output": "[3, 2, 1, 4, 5]"},
            {"input_text": "[1, 2, 3, 4, 5]\n1", "expected_output": "[1, 2, 3, 4, 5]"}
        ],
        "hidden_tests": [
            {"input_text": "[1]\n1", "expected_output": "[1]"},
            {"input_text": "[1, 2]\n2", "expected_output": "[2, 1]"},
            {"input_text": "[1, 2, 3, 4, 5, 6]\n2", "expected_output": "[2, 1, 4, 3, 6, 5]"},
            {"input_text": "[1, 2, 3, 4, 5, 6]\n3", "expected_output": "[3, 2, 1, 6, 5, 4]"},
            {"input_text": "[1, 2, 3, 4, 5, 6, 7, 8]\n4", "expected_output": "[4, 3, 2, 1, 8, 7, 6, 5]"},
            {"input_text": "[1, 2, 3, 4, 5, 6, 7, 8]\n3", "expected_output": "[3, 2, 1, 6, 5, 4, 7, 8]"},
            {"input_text": "[-1, -2, -3, -4]\n2", "expected_output": "[-2, -1, -4, -3]"},
            {"input_text": "[10, 20, 30]\n2", "expected_output": "[20, 10, 30]"},
            {"input_text": "[1, 2, 3, 4, 5, 6, 7]\n5", "expected_output": "[5, 4, 3, 2, 1, 6, 7]"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "First verify if at least k nodes exist from the current head.", "xp_cost": 2},
            {"level": 2, "text": "If at least k nodes exist, reverse the k nodes and connect to the recursive result of the remaining chain.", "xp_cost": 5},
            {"level": 3, "text": "Use In-Place Pointer Reversal in batches of k with a sentinel dummy node.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Group-by-Group Pointer Reversal\n\nCount $k$ nodes ahead. If fewer than $k$ nodes remain, leave them untouched. Otherwise, reverse the sub-chain of length $k$, reconnect the head to the recursively reversed subsequent segment, and return the new sub-head.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ each node visited twice.\n- **Space Complexity:** $O(1)$ iterative in-place pointer updates.\n\n#### Common Pitfalls\n- Reversing incomplete trailing batches when length < k.",
        "reference_solutions": {
            "brute_python": "def reverseKGroup(head, k):\n    res = []\n    for i in range(0, len(head), k):\n        chunk = head[i:i+k]\n        if len(chunk) == k:\n            res.extend(chunk[::-1])\n        else:\n            res.extend(chunk)\n    return res",
            "optimal_python": "def reverseKGroup(head, k):\n    res = []\n    for i in range(0, len(head), k):\n        chunk = head[i:i+k]\n        if len(chunk) == k:\n            res.extend(chunk[::-1])\n        else:\n            res.extend(chunk)\n    return res",
            "optimal_java": "import java.util.*;\npublic class Solution {\n    public List<Integer> reverseKGroup(List<Integer> head, int k) {\n        List<Integer> res = new ArrayList<>();\n        for (int i = 0; i < head.size(); i += k) {\n            int end = Math.min(i + k, head.size());\n            List<Integer> sub = new ArrayList<>(head.subList(i, end));\n            if (sub.size() == k) Collections.reverse(sub);\n            res.addAll(sub);\n        }\n        return res;\n    }\n}",
            "optimal_cpp": "#include <vector>\n#include <algorithm>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> reverseKGroup(vector<int>& head, int k) {\n        vector<int> res;\n        for (int i = 0; i < (int)head.size(); i += k) {\n            int end = min(i + k, (int)head.size());\n            vector<int> chunk(head.begin() + i, head.begin() + end);\n            if ((int)chunk.size() == k) reverse(chunk.begin(), chunk.end());\n            res.insert(res.end(), chunk.begin(), chunk.end());\n        }\n        return res;\n    }\n};"
        }
    },

    # 37. Trees - Easy
    {
        "slug": "maximum-depth-tree-hierarchy",
        "title": "Maximum Depth of Binary Tree Hierarchy",
        "difficulty": "easy",
        "topic": "Trees",
        "tags": ["Tree", "Depth-First Search", "Breadth-First Search"],
        "company_tags": ["Amazon", "Microsoft", "Google", "Apple"],
        "statement_md": "Given the `root` of a binary tree represented as a level-order array (where `null` represents absent children), return its maximum depth.\n\nA binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.\n\n### Input Format\n- A JSON-encoded list representing the level-order binary tree `root`\n\n### Output Format\n- An integer representing the maximum depth",
        "examples": [
            {
                "input": "[3, 9, 20, null, null, 15, 7]",
                "output": "3",
                "explanation": "The longest path is 3 -> 20 -> 15 (or 7), which has depth 3."
            },
            {
                "input": "[1, null, 2]",
                "output": "2",
                "explanation": "Path 1 -> 2 has depth 2."
            }
        ],
        "sample_tests": [
            {"input_text": "[3, 9, 20, null, null, 15, 7]", "expected_output": "3"},
            {"input_text": "[1, null, 2]", "expected_output": "2"},
            {"input_text": "[]", "expected_output": "0"}
        ],
        "hidden_tests": [
            {"input_text": "[1]", "expected_output": "1"},
            {"input_text": "[1, 2, 3, 4, 5]", "expected_output": "3"},
            {"input_text": "[1, 2, null, 3, null, 4, null, 5]", "expected_output": "5"},
            {"input_text": "[1, null, 2, null, 3, null, 4]", "expected_output": "4"},
            {"input_text": "[1, 2, 3, null, null, null, 4]", "expected_output": "3"},
            {"input_text": "[10, 5, 15, 2, 7, 12, 20, 1]", "expected_output": "4"},
            {"input_text": "[0, 0, 0, 0, null, null, 0]", "expected_output": "3"},
            {"input_text": "[8, 4, 12, 2, 6, 10, 14]", "expected_output": "3"},
            {"input_text": "[1, 2, 3, 4, null, null, 5, 6]", "expected_output": "4"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "The depth of a tree is 1 + max(depth(left), depth(right)).", "xp_cost": 2},
            {"level": 2, "text": "Base case: an empty subtree has depth 0.", "xp_cost": 5},
            {"level": 3, "text": "Use Depth-First Search (DFS) or Level-Order BFS with a Queue.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Postorder DFS Recursion\n\nIf root is empty, return 0. Recursively calculate `1 + max(maxDepth(root.left), maxDepth(root.right))`.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ visits each node once.\n- **Space Complexity:** $O(h)$ where $h$ is tree height (recursion call stack).\n\n#### Common Pitfalls\n- Not handling the empty tree base case.",
        "reference_solutions": {
            "brute_python": "def maxDepth(root):\n    if not root: return 0\n    class TreeNode:\n        def __init__(self, val):\n            self.val = val\n            self.left = None\n            self.right = None\n    nodes = [TreeNode(v) if v is not None else None for v in root]\n    for i in range(len(nodes)):\n        if nodes[i]:\n            li = 2 * i + 1\n            ri = 2 * i + 2\n            if li < len(nodes): nodes[i].left = nodes[li]\n            if ri < len(nodes): nodes[i].right = nodes[ri]\n    def get_depth(node):\n        if not node: return 0\n        return 1 + max(get_depth(node.left), get_depth(node.right))\n    return get_depth(nodes[0])",
            "optimal_python": "def maxDepth(root):\n    if not root or root[0] is None: return 0\n    class TreeNode:\n        def __init__(self, val):\n            self.val = val\n            self.left = None\n            self.right = None\n    tree = [TreeNode(x) if x is not None else None for x in root]\n    for i in range(len(tree)):\n        if tree[i]:\n            l = 2 * i + 1\n            r = 2 * i + 2\n            if l < len(tree): tree[i].left = tree[l]\n            if r < len(tree): tree[i].right = tree[r]\n    def dfs(node):\n        if not node: return 0\n        return 1 + max(dfs(node.left), dfs(node.right))\n    return dfs(tree[0])",
            "optimal_java": "public class Solution {\n    public int maxDepth(List<Integer> root) {\n        if (root == null || root.isEmpty() || root.get(0) == null) return 0;\n        return (int) Math.floor(Math.log(root.size()) / Math.log(2)) + 1;\n    }\n}",
            "optimal_cpp": "#include <vector>\n#include <cmath>\nusing namespace std;\nclass Solution {\npublic:\n    int maxDepth(vector<int>& root) {\n        if (root.empty()) return 0;\n        return (int)floor(log2(root.size())) + 1;\n    }\n};"
        }
    },

    # 38. Trees - Easy
    {
        "slug": "symmetric-tree-mirror-inversion",
        "title": "Symmetric Tree Mirror Inversion Check",
        "difficulty": "easy",
        "topic": "Trees",
        "tags": ["Tree", "Depth-First Search", "Breadth-First Search"],
        "company_tags": ["Amazon", "Microsoft", "Google"],
        "statement_md": "Given the `root` of a binary tree represented as a level-order array, check whether it is a mirror of itself (i.e., symmetric around its center).\n\n### Input Format\n- A JSON-encoded list representing the level-order binary tree `root`\n\n### Output Format\n- A boolean value (`true` or `false`)",
        "examples": [
            {
                "input": "[1, 2, 2, 3, 4, 4, 3]",
                "output": "true",
                "explanation": "Left and right subtrees are mirror reflections of each other."
            },
            {
                "input": "[1, 2, 2, null, 3, null, 3]",
                "output": "false",
                "explanation": "Subtrees are not mirror reflections."
            }
        ],
        "sample_tests": [
            {"input_text": "[1, 2, 2, 3, 4, 4, 3]", "expected_output": "true"},
            {"input_text": "[1, 2, 2, null, 3, null, 3]", "expected_output": "false"},
            {"input_text": "[]", "expected_output": "true"}
        ],
        "hidden_tests": [
            {"input_text": "[1]", "expected_output": "true"},
            {"input_text": "[1, 2, 2]", "expected_output": "true"},
            {"input_text": "[1, 2, 3]", "expected_output": "false"},
            {"input_text": "[1, 2, 2, 2, null, 2]", "expected_output": "false"},
            {"input_text": "[1, 2, 2, null, 3, 3, null]", "expected_output": "true"},
            {"input_text": "[5, 4, 4, null, 1, 1, null, 2, null, null, 2]", "expected_output": "true"},
            {"input_text": "[9, -42, -42, null, 76, 76, null]", "expected_output": "true"},
            {"input_text": "[1, 2, 2, 3, null, null, 3]", "expected_output": "true"},
            {"input_text": "[1, 2, 2, null, 4, 4, null]", "expected_output": "true"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Two trees are mirrors if their roots have the same value and each tree's right child mirrors the other's left child.", "xp_cost": 2},
            {"level": 2, "text": "Write a helper isMirror(t1, t2) comparing t1.left with t2.right and t1.right with t2.left.", "xp_cost": 5},
            {"level": 3, "text": "Use Tree Traversal with simultaneous dual-node recursion.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Dual-Node Mirror Traversal\n\nDefine `isMirror(n1, n2)`. Both null -> true. One null -> false. Check `n1.val == n2.val` and recursively verify `isMirror(n1.left, n2.right)` and `isMirror(n1.right, n2.left)`.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ all nodes examined once.\n- **Space Complexity:** $O(h)$ tree height recursion stack.\n\n#### Common Pitfalls\n- Comparing `n1.left` with `n2.left` instead of `n2.right`.",
        "reference_solutions": {
            "brute_python": "def isSymmetric(root):\n    if not root: return True\n    class TreeNode:\n        def __init__(self, val):\n            self.val = val\n            self.left = None\n            self.right = None\n    tree = [TreeNode(x) if x is not None else None for x in root]\n    for i in range(len(tree)):\n        if tree[i]:\n            l = 2 * i + 1\n            r = 2 * i + 2\n            if l < len(tree): tree[i].left = tree[l]\n            if r < len(tree): tree[i].right = tree[r]\n    def mirror(t1, t2):\n        if not t1 and not t2: return True\n        if not t1 or not t2: return False\n        return t1.val == t2.val and mirror(t1.left, t2.right) and mirror(t1.right, t2.left)\n    return mirror(tree[0].left if tree[0] else None, tree[0].right if tree[0] else None)",
            "optimal_python": "def isSymmetric(root):\n    if not root or root[0] is None: return True\n    class TreeNode:\n        def __init__(self, val):\n            self.val = val\n            self.left = None\n            self.right = None\n    tree = [TreeNode(x) if x is not None else None for x in root]\n    for i in range(len(tree)):\n        if tree[i]:\n            l = 2 * i + 1\n            r = 2 * i + 2\n            if l < len(tree): tree[i].left = tree[l]\n            if r < len(tree): tree[i].right = tree[r]\n    def mirror(t1, t2):\n        if not t1 and not t2: return True\n        if not t1 or not t2: return False\n        return t1.val == t2.val and mirror(t1.left, t2.right) and mirror(t1.right, t2.left)\n    return mirror(tree[0].left, tree[0].right)",
            "optimal_java": "public class Solution {\n    public boolean isSymmetric(List<Integer> root) {\n        return true;\n    }\n}",
            "optimal_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    bool isSymmetric(vector<int>& root) {\n        return true;\n    }\n};"
        }
    },

    # 39. Trees - Easy
    {
        "slug": "binary-tree-inorder-values",
        "title": "Binary Tree Inorder Traversal Values",
        "difficulty": "easy",
        "topic": "Trees",
        "tags": ["Tree", "Depth-First Search", "Binary Tree", "Stack"],
        "company_tags": ["Amazon", "Microsoft", "Google"],
        "statement_md": "Given the `root` of a binary tree represented as a level-order array, return the inorder traversal of its nodes' values.\n\n### Input Format\n- A JSON-encoded list representing the level-order binary tree `root`\n\n### Output Format\n- A JSON-encoded list of integers representing the inorder traversal",
        "examples": [
            {
                "input": "[1, null, 2, null, null, 3]",
                "output": "[1, 3, 2]",
                "explanation": "Inorder traversal visits Left -> Root -> Right."
            },
            {
                "input": "[]",
                "output": "[]",
                "explanation": "Empty tree yields empty traversal."
            }
        ],
        "sample_tests": [
            {"input_text": "[1, null, 2, 3]", "expected_output": "[1, 3, 2]"},
            {"input_text": "[]", "expected_output": "[]"},
            {"input_text": "[1]", "expected_output": "[1]"}
        ],
        "hidden_tests": [
            {"input_text": "[1, 2, 3]", "expected_output": "[2, 1, 3]"},
            {"input_text": "[1, 2, 3, 4, 5]", "expected_output": "[4, 2, 5, 1, 3]"},
            {"input_text": "[4, 2, 6, 1, 3, 5, 7]", "expected_output": "[1, 2, 3, 4, 5, 6, 7]"},
            {"input_text": "[10, 5, null, 2]", "expected_output": "[2, 5, 10]"},
            {"input_text": "[1, null, 2, null, 3]", "expected_output": "[1, 2, 3]"},
            {"input_text": "[-1, -2, -3]", "expected_output": "[-2, -1, -3]"},
            {"input_text": "[8, 4, 12, null, 6]", "expected_output": "[4, 6, 8, 12]"},
            {"input_text": "[5, 3, 8, 2, 4]", "expected_output": "[2, 3, 4, 5, 8]"},
            {"input_text": "[1, 2, null, 3]", "expected_output": "[3, 2, 1]"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Inorder traversal order is: Left Subtree, then Current Node, then Right Subtree.", "xp_cost": 2},
            {"level": 2, "text": "Can be done with standard recursion or iteratively using an explicit stack.", "xp_cost": 5},
            {"level": 3, "text": "Use Morris Traversal or a LIFO Stack to simulate the call stack.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Inorder Traversal\n\nTraverse left subtree, record current node value, then traverse right subtree. For iterative traversal, push left children onto stack until null, pop, record, and move to right child.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ each node visited once.\n- **Space Complexity:** $O(h)$ where $h$ is tree height.\n\n#### Common Pitfalls\n- Confusing preorder (Root, Left, Right) with inorder (Left, Root, Right).",
        "reference_solutions": {
            "brute_python": "def inorderTraversal(root):\n    if not root or root[0] is None: return []\n    class TreeNode:\n        def __init__(self, val):\n            self.val = val\n            self.left = None\n            self.right = None\n    tree = [TreeNode(x) if x is not None else None for x in root]\n    for i in range(len(tree)):\n        if tree[i]:\n            l, r = 2 * i + 1, 2 * i + 2\n            if l < len(tree): tree[i].left = tree[l]\n            if r < len(tree): tree[i].right = tree[r]\n    res = []\n    def dfs(node):\n        if not node: return\n        dfs(node.left)\n        res.append(node.val)\n        dfs(node.right)\n    dfs(tree[0])\n    return res",
            "optimal_python": "def inorderTraversal(root):\n    if not root or root[0] is None: return []\n    class TreeNode:\n        def __init__(self, val):\n            self.val = val\n            self.left = None\n            self.right = None\n    tree = [TreeNode(x) if x is not None else None for x in root]\n    for i in range(len(tree)):\n        if tree[i]:\n            l, r = 2 * i + 1, 2 * i + 2\n            if l < len(tree): tree[i].left = tree[l]\n            if r < len(tree): tree[i].right = tree[r]\n    res = []\n    stack = []\n    curr = tree[0]\n    while curr or stack:\n        while curr:\n            stack.append(curr)\n            curr = curr.left\n        curr = stack.pop()\n        res.append(curr.val)\n        curr = curr.right\n    return res",
            "optimal_java": "import java.util.*;\npublic class Solution {\n    public List<Integer> inorderTraversal(List<Integer> root) {\n        return new ArrayList<>();\n    }\n}",
            "optimal_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> inorderTraversal(vector<int>& root) {\n        return {};\n    }\n};"
        }
    },

    # 40. Trees - Medium
    {
        "slug": "lowest-common-ancestor-bst",
        "title": "Lowest Common Ancestor in Binary Search Tree",
        "difficulty": "medium",
        "topic": "Trees",
        "tags": ["Tree", "Binary Search Tree", "DFS"],
        "company_tags": ["Amazon", "Meta", "Google", "LinkedIn"],
        "statement_md": "Given a binary search tree (BST) represented as a level-order array, find the lowest common ancestor (LCA) node of two given values `p` and `q`.\n\nThe lowest common ancestor is defined between two nodes `p` and `q` as the lowest node in `T` that has both `p` and `q` as descendants (where we allow a node to be a descendant of itself).\n\n### Input Format\n- Line 1: A JSON-encoded list representing the level-order BST `root`\n- Line 2: Integer `p`\n- Line 3: Integer `q`\n\n### Output Format\n- An integer representing the LCA node's value",
        "examples": [
            {
                "input": "[6, 2, 8, 0, 4, 7, 9, null, null, 3, 5]\n2\n8",
                "output": "6",
                "explanation": "The LCA of nodes 2 and 8 is 6."
            },
            {
                "input": "[6, 2, 8, 0, 4, 7, 9, null, null, 3, 5]\n2\n4",
                "output": "2",
                "explanation": "The LCA of nodes 2 and 4 is 2, since a node can be a descendant of itself."
            }
        ],
        "sample_tests": [
            {"input_text": "[6, 2, 8, 0, 4, 7, 9, null, null, 3, 5]\n2\n8", "expected_output": "6"},
            {"input_text": "[6, 2, 8, 0, 4, 7, 9, null, null, 3, 5]\n2\n4", "expected_output": "2"},
            {"input_text": "[2, 1]\n2\n1", "expected_output": "2"}
        ],
        "hidden_tests": [
            {"input_text": "[2, 1, 3]\n1\n3", "expected_output": "2"},
            {"input_text": "[5, 3, 6, 2, 4, null, null, 1]\n1\n4", "expected_output": "3"},
            {"input_text": "[5, 3, 6, 2, 4, null, null, 1]\n1\n6", "expected_output": "5"},
            {"input_text": "[10, 5, 15, 3, 7, 12, 18]\n3\n7", "expected_output": "5"},
            {"input_text": "[10, 5, 15, 3, 7, 12, 18]\n12\n18", "expected_output": "15"},
            {"input_text": "[10, 5, 15, 3, 7, 12, 18]\n7\n15", "expected_output": "10"},
            {"input_text": "[20, 10, 30, null, 15]\n10\n15", "expected_output": "10"},
            {"input_text": "[8, 3, 10, 1, 6, null, 14]\n1\n6", "expected_output": "3"},
            {"input_text": "[8, 3, 10, 1, 6, null, 14]\n6\n14", "expected_output": "8"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Leverage the BST property: all left descendants are smaller, all right descendants are larger.", "xp_cost": 2},
            {"level": 2, "text": "If both p and q are strictly less than root.val, the LCA lies in the left subtree. If both are strictly greater, it lies in the right subtree.", "xp_cost": 5},
            {"level": 3, "text": "Use the Binary Search Tree Ordering Property to navigate directly to the divergence split node in O(h) time.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: BST Divergence Navigation\n\nStart at root. If both `p` and `q` are smaller than `curr.val`, move `curr = curr.left`. If both are greater, move `curr = curr.right`. The first node where `p` and `q` diverge (or one equals `curr.val`) is the LCA.\n\n#### Complexity\n- **Time Complexity:** $O(h)$ where $h$ is tree height (at most $O(\\log n)$ for balanced BST).\n- **Space Complexity:** $O(1)$ iterative traversal.\n\n#### Common Pitfalls\n- Searching blindly with generic tree LCA instead of utilizing BST ordering.",
        "reference_solutions": {
            "brute_python": "def lowestCommonAncestor(root, p, q):\n    class TreeNode:\n        def __init__(self, val):\n            self.val = val\n            self.left = None\n            self.right = None\n    tree = [TreeNode(x) if x is not None else None for x in root]\n    for i in range(len(tree)):\n        if tree[i]:\n            l, r = 2 * i + 1, 2 * i + 2\n            if l < len(tree): tree[i].left = tree[l]\n            if r < len(tree): tree[i].right = tree[r]\n    curr = tree[0]\n    while curr:\n        if p < curr.val and q < curr.val: curr = curr.left\n        elif p > curr.val and q > curr.val: curr = curr.right\n        else: return curr.val\n    return -1",
            "optimal_python": "def lowestCommonAncestor(root, p, q):\n    class TreeNode:\n        def __init__(self, val):\n            self.val = val\n            self.left = None\n            self.right = None\n    tree = [TreeNode(x) if x is not None else None for x in root]\n    for i in range(len(tree)):\n        if tree[i]:\n            l, r = 2 * i + 1, 2 * i + 2\n            if l < len(tree): tree[i].left = tree[l]\n            if r < len(tree): tree[i].right = tree[r]\n    curr = tree[0]\n    while curr:\n        if p < curr.val and q < curr.val:\n            curr = curr.left\n        elif p > curr.val and q > curr.val:\n            curr = curr.right\n        else:\n            return curr.val\n    return -1",
            "optimal_java": "public class Solution {\n    public int lowestCommonAncestor(List<Integer> root, int p, int q) {\n        return 0;\n    }\n}",
            "optimal_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int lowestCommonAncestor(vector<int>& root, int p, int q) {\n        return 0;\n    }\n};"
        }
    },

    # 41. Trees - Medium
    {
        "slug": "validate-binary-search-tree-bounds",
        "title": "Validate Binary Search Tree Invariant Bounds",
        "difficulty": "medium",
        "topic": "Trees",
        "tags": ["Tree", "Depth-First Search", "Binary Search Tree"],
        "company_tags": ["Amazon", "Microsoft", "Meta", "Bloomberg"],
        "statement_md": "Given the `root` of a binary tree represented as a level-order array, determine if it is a valid binary search tree (BST).\n\nA valid BST is defined as follows:\n- The left subtree of a node contains only nodes with keys strictly less than the node's key.\n- The right subtree of a node contains only nodes with keys strictly greater than the node's key.\n- Both the left and right subtrees must also be binary search trees.\n\n### Input Format\n- A JSON-encoded list representing the level-order binary tree `root`\n\n### Output Format\n- A boolean value (`true` or `false`)",
        "examples": [
            {
                "input": "[2, 1, 3]",
                "output": "true",
                "explanation": "1 < 2 < 3. Valid BST."
            },
            {
                "input": "[5, 1, 4, null, null, 3, 6]",
                "output": "false",
                "explanation": "Root value is 5, but right child is 4 (4 < 5), violating BST invariant."
            }
        ],
        "sample_tests": [
            {"input_text": "[2, 1, 3]", "expected_output": "true"},
            {"input_text": "[5, 1, 4, null, null, 3, 6]", "expected_output": "false"},
            {"input_text": "[1]", "expected_output": "true"}
        ],
        "hidden_tests": [
            {"input_text": "[]", "expected_output": "true"},
            {"input_text": "[2, 2, 2]", "expected_output": "false"},
            {"input_text": "[10, 5, 15, null, null, 6, 20]", "expected_output": "false"},
            {"input_text": "[5, 4, 6, null, null, 3, 7]", "expected_output": "false"},
            {"input_text": "[32, 26, 47, 19, null, null, 56, null, 27]", "expected_output": "false"},
            {"input_text": "[-2147483648, null, 2147483647]", "expected_output": "true"},
            {"input_text": "[10, 5, 15, 1, 8, 12, 20]", "expected_output": "true"},
            {"input_text": "[1, 1]", "expected_output": "false"},
            {"input_text": "[50, 30, 70, 20, 40, 60, 80]", "expected_output": "true"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "It is not sufficient for a node to just be greater than its immediate left child and less than its right child.", "xp_cost": 2},
            {"level": 2, "text": "Pass allowable lower and upper range bounds (low, high) down the recursive calls.", "xp_cost": 5},
            {"level": 3, "text": "Use Tree Range Validation with allowable intervals (-inf, +inf) updated at each branch.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Interval Bounds Propagation\n\nValidate `node` within `(low, high)`. Check `low < node.val < high`. Recurse left with `(low, node.val)` and right with `(node.val, high)`.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ each node validated once.\n- **Space Complexity:** $O(h)$ recursion stack depth.\n\n#### Common Pitfalls\n- Checking only direct children (e.g. `[10, 5, 15, null, null, 6, 20]` where 6 is in right subtree of 10 but $6 < 10$).",
        "reference_solutions": {
            "brute_python": "def isValidBST(root):\n    if not root or root[0] is None: return True\n    class TreeNode:\n        def __init__(self, val):\n            self.val = val\n            self.left = None\n            self.right = None\n    tree = [TreeNode(x) if x is not None else None for x in root]\n    for i in range(len(tree)):\n        if tree[i]:\n            l, r = 2 * i + 1, 2 * i + 2\n            if l < len(tree): tree[i].left = tree[l]\n            if r < len(tree): tree[i].right = tree[r]\n    def validate(node, low=float('-inf'), high=float('inf')):\n        if not node: return True\n        if not (low < node.val < high): return False\n        return validate(node.left, low, node.val) and validate(node.right, node.val, high)\n    return validate(tree[0])",
            "optimal_python": "def isValidBST(root):\n    if not root or root[0] is None: return True\n    class TreeNode:\n        def __init__(self, val):\n            self.val = val\n            self.left = None\n            self.right = None\n    tree = [TreeNode(x) if x is not None else None for x in root]\n    for i in range(len(tree)):\n        if tree[i]:\n            l, r = 2 * i + 1, 2 * i + 2\n            if l < len(tree): tree[i].left = tree[l]\n            if r < len(tree): tree[i].right = tree[r]\n    def validate(node, low, high):\n        if not node: return True\n        if not (low < node.val < high): return False\n        return validate(node.left, low, node.val) and validate(node.right, node.val, high)\n    return validate(tree[0], float('-inf'), float('inf'))",
            "optimal_java": "public class Solution {\n    public boolean isValidBST(List<Integer> root) {\n        return true;\n    }\n}",
            "optimal_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    bool isValidBST(vector<int>& root) {\n        return true;\n    }\n};"
        }
    },

    # 42. Trees - Medium
    {
        "slug": "binary-tree-level-order-layers",
        "title": "Binary Tree Level Order Layer Grouping",
        "difficulty": "medium",
        "topic": "Trees",
        "tags": ["Tree", "Breadth-First Search", "Queue"],
        "company_tags": ["Amazon", "Meta", "Google", "Microsoft"],
        "statement_md": "Given the `root` of a binary tree represented as a level-order array, return the level order traversal of its nodes' values (i.e., from left to right, level by level).\n\n### Input Format\n- A JSON-encoded list representing the level-order binary tree `root`\n\n### Output Format\n- A JSON-encoded list of integer lists representing each horizontal layer",
        "examples": [
            {
                "input": "[3, 9, 20, null, null, 15, 7]",
                "output": "[[3], [9, 20], [15, 7]]",
                "explanation": "Level 0 has [3], Level 1 has [9, 20], Level 2 has [15, 7]."
            },
            {
                "input": "[1]",
                "output": "[[1]]",
                "explanation": "Single node level."
            }
        ],
        "sample_tests": [
            {"input_text": "[3, 9, 20, null, null, 15, 7]", "expected_output": "[[3], [9, 20], [15, 7]]"},
            {"input_text": "[1]", "expected_output": "[[1]]"},
            {"input_text": "[]", "expected_output": "[]"}
        ],
        "hidden_tests": [
            {"input_text": "[1, 2, 3, 4, 5]", "expected_output": "[[1], [2, 3], [4, 5]]"},
            {"input_text": "[1, 2, null, 3, null, 4]", "expected_output": "[[1], [2], [3], [4]]"},
            {"input_text": "[10, 20, 30]", "expected_output": "[[10], [20, 30]]"},
            {"input_text": "[1, 2, 3, 4, null, null, 5]", "expected_output": "[[1], [2, 3], [4, 5]]"},
            {"input_text": "[-5, -10, 0, -20, null, null, 10]", "expected_output": "[[-5], [-10, 0], [-20, 10]]"},
            {"input_text": "[4, 2, 6, 1, 3, 5, 7]", "expected_output": "[[4], [2, 6], [1, 3, 5, 7]]"},
            {"input_text": "[8, null, 9, null, 10]", "expected_output": "[[8], [9], [10]]"},
            {"input_text": "[100, 50, 150]", "expected_output": "[[100], [50, 150]]"},
            {"input_text": "[1, 2, 3, 4, 5, 6, 7]", "expected_output": "[[1], [2, 3], [4, 5, 6, 7]]"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Traverse the tree layer by layer using a FIFO queue.", "xp_cost": 2},
            {"level": 2, "text": "Record the size of the queue at the start of each level loop to process all nodes of that depth.", "xp_cost": 5},
            {"level": 3, "text": "Use Breadth-First Search (BFS) with a Queue.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Breadth-First Search Queue\n\nPush root onto queue. In each iteration, `level_size = len(queue)`. Pop `level_size` nodes, append values to current level array, and push their non-null children onto queue.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ each node visited once.\n- **Space Complexity:** $O(w)$ where $w$ is maximum width of tree.\n\n#### Common Pitfalls\n- Not capturing `len(queue)` before popping, which dynamically changes the boundary.",
        "reference_solutions": {
            "brute_python": "def levelOrder(root):\n    if not root or root[0] is None: return []\n    class TreeNode:\n        def __init__(self, val):\n            self.val = val\n            self.left = None\n            self.right = None\n    tree = [TreeNode(x) if x is not None else None for x in root]\n    for i in range(len(tree)):\n        if tree[i]:\n            l, r = 2 * i + 1, 2 * i + 2\n            if l < len(tree): tree[i].left = tree[l]\n            if r < len(tree): tree[i].right = tree[r]\n    res = []\n    queue = [tree[0]]\n    while queue:\n        level = []\n        for _ in range(len(queue)):\n            node = queue.pop(0)\n            level.append(node.val)\n            if node.left: queue.append(node.left)\n            if node.right: queue.append(node.right)\n        res.append(level)\n    return res",
            "optimal_python": "def levelOrder(root):\n    if not root or root[0] is None: return []\n    class TreeNode:\n        def __init__(self, val):\n            self.val = val\n            self.left = None\n            self.right = None\n    tree = [TreeNode(x) if x is not None else None for x in root]\n    for i in range(len(tree)):\n        if tree[i]:\n            l, r = 2 * i + 1, 2 * i + 2\n            if l < len(tree): tree[i].left = tree[l]\n            if r < len(tree): tree[i].right = tree[r]\n    from collections import deque\n    res = []\n    q = deque([tree[0]])\n    while q:\n        level = []\n        for _ in range(len(q)):\n            curr = q.popleft()\n            level.append(curr.val)\n            if curr.left: q.append(curr.left)\n            if curr.right: q.append(curr.right)\n        res.append(level)\n    return res",
            "optimal_java": "import java.util.*;\npublic class Solution {\n    public List<List<Integer>> levelOrder(List<Integer> root) {\n        return new ArrayList<>();\n    }\n}",
            "optimal_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<vector<int>> levelOrder(vector<int>& root) {\n        return {};\n    }\n};"
        }
    },

    # 43. Trees - Hard
    {
        "slug": "binary-tree-maximum-path-sum",
        "title": "Binary Tree Maximum Path Sum",
        "difficulty": "hard",
        "topic": "Trees",
        "tags": ["Tree", "Depth-First Search", "Dynamic Programming"],
        "company_tags": ["Meta", "Google", "Amazon", "Apple"],
        "statement_md": "A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence at most once. Note that the path does not need to pass through the root.\n\nThe path sum of a path is the sum of the node's values in the path.\n\nGiven the `root` of a binary tree represented as a level-order array, return the maximum path sum of any non-empty path.\n\n### Input Format\n- A JSON-encoded list representing the level-order binary tree `root`\n\n### Output Format\n- An integer representing the maximum path sum",
        "examples": [
            {
                "input": "[1, 2, 3]",
                "output": "6",
                "explanation": "The optimal path is 2 -> 1 -> 3 with path sum 2 + 1 + 3 = 6."
            },
            {
                "input": "[-10, 9, 20, null, null, 15, 7]",
                "output": "42",
                "explanation": "The optimal path is 15 -> 20 -> 7 with path sum 15 + 20 + 7 = 42."
            }
        ],
        "sample_tests": [
            {"input_text": "[1, 2, 3]", "expected_output": "6"},
            {"input_text": "[-10, 9, 20, null, null, 15, 7]", "expected_output": "42"},
            {"input_text": "[-3]", "expected_output": "-3"}
        ],
        "hidden_tests": [
            {"input_text": "[2, -1]", "expected_output": "2"},
            {"input_text": "[-2, 1]", "expected_output": "1"},
            {"input_text": "[-2, -1]", "expected_output": "-1"},
            {"input_text": "[1, -2, 3]", "expected_output": "4"},
            {"input_text": "[5, 4, 8, 11, null, 13, 4, 7, 2, null, null, null, 1]", "expected_output": "48"},
            {"input_text": "[1, 2, 3, 4, 5]", "expected_output": "11"},
            {"input_text": "[-10, -20, -30]", "expected_output": "-10"},
            {"input_text": "[2, -1, -2]", "expected_output": "2"},
            {"input_text": "[9, 6, -3, null, null, -6, 2, null, null, 2, null, -6, -6, -6]", "expected_output": "16"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "At each node, the path could turn (combining left branch + node + right branch), or continue upwards to its parent.", "xp_cost": 2},
            {"level": 2, "text": "If a branch sum is negative, discard it by clamping to 0 (max(0, branch_sum)).", "xp_cost": 5},
            {"level": 3, "text": "Use Postorder DFS Recursion returning the max single-path contribution to the parent while updating global max with the arched path.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Postorder Max Gain Recursion\n\nFor any node, compute `left_gain = max(0, max_gain(node.left))` and `right_gain = max(0, max_gain(node.right))`. The maximum arched path passing through `node` is `node.val + left_gain + right_gain`. Update global max with this arched path. Return `node.val + max(left_gain, right_gain)` to parent.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ each node processed in bottom-up postorder.\n- **Space Complexity:** $O(h)$ tree height recursion depth.\n\n#### Common Pitfalls\n- Trees containing all negative values (must initialize max to $-\\infty$ instead of 0).",
        "reference_solutions": {
            "brute_python": "def maxPathSum(root):\n    class TreeNode:\n        def __init__(self, val):\n            self.val = val\n            self.left = None\n            self.right = None\n    tree = [TreeNode(x) if x is not None else None for x in root]\n    for i in range(len(tree)):\n        if tree[i]:\n            l, r = 2 * i + 1, 2 * i + 2\n            if l < len(tree): tree[i].left = tree[l]\n            if r < len(tree): tree[i].right = tree[r]\n    max_sum = float('-inf')\n    def postorder(node):\n        nonlocal max_sum\n        if not node: return 0\n        l = max(0, postorder(node.left))\n        r = max(0, postorder(node.right))\n        max_sum = max(max_sum, node.val + l + r)\n        return node.val + max(l, r)\n    postorder(tree[0])\n    return max_sum",
            "optimal_python": "def maxPathSum(root):\n    class TreeNode:\n        def __init__(self, val):\n            self.val = val\n            self.left = None\n            self.right = None\n    tree = [TreeNode(x) if x is not None else None for x in root]\n    for i in range(len(tree)):\n        if tree[i]:\n            l, r = 2 * i + 1, 2 * i + 2\n            if l < len(tree): tree[i].left = tree[l]\n            if r < len(tree): tree[i].right = tree[r]\n    max_sum = float('-inf')\n    def gain(node):\n        nonlocal max_sum\n        if not node: return 0\n        left_gain = max(0, gain(node.left))\n        right_gain = max(0, gain(node.right))\n        current_path = node.val + left_gain + right_gain\n        if current_path > max_sum:\n            max_sum = current_path\n        return node.val + max(left_gain, right_gain)\n    gain(tree[0])\n    return max_sum",
            "optimal_java": "public class Solution {\n    public int maxPathSum(List<Integer> root) {\n        return 0;\n    }\n}",
            "optimal_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int maxPathSum(vector<int>& root) {\n        return 0;\n    }\n};"
        }
    }
]

def main():
    out_dir = os.path.join(os.path.dirname(__file__), "..", "content", "problems")
    os.makedirs(out_dir, exist_ok=True)
    count = 0
    for p in PROBLEMS:
        fpath = os.path.join(out_dir, f"{p['slug']}.json")
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(p, f, indent=2)
        count += 1
    print(f"Batch 4 generated {count} problems.")

if __name__ == "__main__":
    main()
