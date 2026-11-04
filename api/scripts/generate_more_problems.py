import os
import json

PROBLEMS_DATA = [
    {
        "slug": "three-sum",
        "title": "3Sum",
        "difficulty": "medium",
        "topic": "Arrays",
        "tags": ["Array", "Two Pointers", "Sorting"],
        "company_tags": ["Google", "Amazon", "Meta", "Microsoft"],
        "statement_md": "Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.\n\nNotice that the solution set must not contain duplicate triplets.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "[-1, 0, 1, 2, -1, -4]",
                "expected_output": "[[-1, -1, 2], [-1, 0, 1]]"
            },
            {
                "input_text": "[0, 1, 1]",
                "expected_output": "[]"
            },
            {
                "input_text": "[0, 0, 0]",
                "expected_output": "[[0, 0, 0]]"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "[-2, 0, 1, 1, 2]",
                "expected_output": "[[-2, 0, 2], [-2, 1, 1]]"
            },
            {
                "input_text": "[-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6]",
                "expected_output": "[[-4, -2, 6], [-4, 0, 4], [-4, 1, 3], [-4, 2, 2], [-2, -2, 4], [-2, 0, 2]]"
            },
            {
                "input_text": "[1, 2, -2, -1]",
                "expected_output": "[]"
            }
        ],
        "hints": [
            {"level": 1, "text": "Can sorting the array simplify finding triplets?", "xp_cost": 2},
            {"level": 2, "text": "Fix the first element at index i, then use two pointers (left and right) to find pairs that sum to -nums[i].", "xp_cost": 5},
            {"level": 3, "text": "To prevent duplicates, skip consecutive identical elements for both the outer loop i and the inner pointers left and right.", "xp_cost": 10}
        ],
        "editorial_md": """### Two Pointers with Sorting

1. Sort the input array `nums`.
2. Iterate `i` from $0$ to $n - 3$. If $nums[i] > 0$, break early because three positive numbers cannot sum to 0.
3. If $i > 0$ and $nums[i] == nums[i - 1]$, skip to avoid duplicates.
4. Set $left = i + 1$ and $right = n - 1$.
5. While $left < right$:
   - Calculate $total = nums[i] + nums[left] + nums[right]$.
   - If $total == 0$, add $[nums[i], nums[left], nums[right]]$ to results, then advance $left$ past duplicate values and decrement $right$ past duplicate values.
   - If $total < 0$, increment $left$.
   - If $total > 0$, decrement $right$.

#### Complexity
- **Time Complexity:** $O(n^2)$ due to sorting $O(n \\log n)$ and the two-pointer pass $O(n^2)$.
- **Space Complexity:** $O(1)$ auxiliary (or $O(n)$ depending on sorting implementation).

```python
def threeSum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    res = []
    n = len(nums)
    for i in range(n - 2):
        if nums[i] > 0:
            break
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        l, r = i + 1, n - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s < 0:
                l += 1
            elif s > 0:
                r -= 1
            else:
                res.append([nums[i], nums[l], nums[r]])
                while l < r and nums[l] == nums[l + 1]:
                    l += 1
                while l < r and nums[r] == nums[r - 1]:
                    r -= 1
                l += 1
                r -= 1
    return res
```"""
    },
    {
        "slug": "container-with-most-water",
        "title": "Container With Most Water",
        "difficulty": "medium",
        "topic": "Arrays",
        "tags": ["Array", "Two Pointers", "Greedy"],
        "company_tags": ["Amazon", "Google", "Apple", "Adobe"],
        "statement_md": "You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the $i$-th line are `(i, 0)` and `(i, height[i])`.\n\nFind two lines that together with the x-axis form a container, such that the container contains the most water.\n\nReturn the maximum amount of water a container can store.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "[1, 8, 6, 2, 5, 4, 8, 3, 7]",
                "expected_output": "49"
            },
            {
                "input_text": "[1, 1]",
                "expected_output": "1"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "[4, 3, 2, 1, 4]",
                "expected_output": "16"
            },
            {
                "input_text": "[1, 2, 1]",
                "expected_output": "2"
            },
            {
                "input_text": "[2, 3, 10, 5, 7, 8, 9]",
                "expected_output": "36"
            }
        ],
        "hints": [
            {"level": 1, "text": "The area between indices i and j is min(height[i], height[j]) * (j - i).", "xp_cost": 2},
            {"level": 2, "text": "Start with two pointers at the widest possible span: left = 0 and right = n - 1.", "xp_cost": 5},
            {"level": 3, "text": "To find a taller boundary, always move the pointer pointing to the shorter vertical line inward.", "xp_cost": 10}
        ],
        "editorial_md": """### Greedy Two Pointers

The container capacity is constrained by the shorter boundary: $Area = \\min(height[l], height[r]) \\times (r - l)$.
Moving the taller pointer inward can only reduce or maintain width while never increasing the limiting height. Moving the shorter pointer inward is the only way that might discover a taller bar to offset the shrinking width.

```python
def maxArea(height: list[int]) -> int:
    l, r = 0, len(height) - 1
    max_w = 0
    while l < r:
        h = min(height[l], height[r])
        max_w = max(max_w, h * (r - l))
        if height[l] < height[r]:
            l += 1
        else:
            r -= 1
    return max_w
```

- **Time Complexity:** $O(n)$ single pass.
- **Space Complexity:** $O(1)$ constant memory."""
    },
    {
        "slug": "linked-list-cycle",
        "title": "Linked List Cycle",
        "difficulty": "easy",
        "topic": "Linked List",
        "tags": ["Linked List", "Two Pointers", "Floyd's Cycle"],
        "company_tags": ["Microsoft", "Amazon", "Apple", "Spotify"],
        "statement_md": "Given the `head` of a linked list represented as an array of values and a cycle index `pos` (-1 if no cycle), determine if the linked list has a cycle in it.\n\nReturn `true` if there is a cycle in the linked list. Otherwise, return `false`.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "[3, 2, 0, -4]\n1",
                "expected_output": "true"
            },
            {
                "input_text": "[1, 2]\n0",
                "expected_output": "true"
            },
            {
                "input_text": "[1]\n-1",
                "expected_output": "false"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "[]\n-1",
                "expected_output": "false"
            },
            {
                "input_text": "[1, 2, 3, 4, 5]\n-1",
                "expected_output": "false"
            },
            {
                "input_text": "[1, 2, 3, 4, 5]\n4",
                "expected_output": "true"
            }
        ],
        "hints": [
            {"level": 1, "text": "Can two runners on a circular track at different speeds ever meet?", "xp_cost": 2},
            {"level": 2, "text": "Use Floyd's Tortoise and Hare algorithm with a slow pointer moving 1 step and a fast pointer moving 2 steps.", "xp_cost": 5},
            {"level": 3, "text": "If fast reaches None/null, no cycle exists. If fast meets slow, a cycle is guaranteed.", "xp_cost": 10}
        ],
        "editorial_md": """### Floyd's Tortoise and Hare Algorithm

1. Initialize `slow = head` and `fast = head`.
2. In each iteration, advance `slow` by 1 node and `fast` by 2 nodes.
3. If `fast` or `fast.next` is null, list terminates, return `False`.
4. If `slow == fast`, the pointers met within a loop, return `True`.

- **Time Complexity:** $O(n)$ where $n$ is node count.
- **Space Complexity:** $O(1)$ in-place detection."""
    },
    {
        "slug": "product-of-array-except-self",
        "title": "Product of Array Except Self",
        "difficulty": "medium",
        "topic": "Arrays",
        "tags": ["Array", "Prefix Sum"],
        "company_tags": ["Amazon", "Apple", "Meta", "Microsoft"],
        "statement_md": "Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`.\n\nThe product of any prefix or suffix of `nums` is guaranteed to fit in a 32-bit integer.\n\nYou must write an algorithm that runs in $O(n)$ time and without using the division operation.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "[1, 2, 3, 4]",
                "expected_output": "[24, 12, 8, 6]"
            },
            {
                "input_text": "[-1, 1, 0, -3, 3]",
                "expected_output": "[0, 0, 9, 0, 0]"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "[2, 3]",
                "expected_output": "[3, 2]"
            },
            {
                "input_text": "[0, 0]",
                "expected_output": "[0, 0]"
            },
            {
                "input_text": "[4, 5, 1, 8, 2]",
                "expected_output": "[80, 64, 320, 40, 160]"
            }
        ],
        "hints": [
            {"level": 1, "text": "The answer for index i is (product of elements before i) * (product of elements after i).", "xp_cost": 2},
            {"level": 2, "text": "Can you compute prefix products in a forward pass and suffix products in a backward pass?", "xp_cost": 5},
            {"level": 3, "text": "Construct the output array with prefix products first, then maintain a running suffix variable from the right.", "xp_cost": 10}
        ],
        "editorial_md": """### Prefix and Suffix Running Products

1. Create output array `ans` of length $n$.
2. Traverse left to right: set `ans[i]` to prefix product of all elements to the left of $i$.
3. Traverse right to left: maintain a running scalar `suffix` and multiply `ans[i] *= suffix`, then update `suffix *= nums[i]`.

```python
def productExceptSelf(nums: list[int]) -> list[int]:
    n = len(nums)
    res = [1] * n
    prefix = 1
    for i in range(n):
        res[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        res[i] *= suffix
        suffix *= nums[i]
    return res
```

- **Time Complexity:** $O(n)$
- **Space Complexity:** $O(1)$ auxiliary space excluding output array."""
    },
    {
        "slug": "valid-anagram",
        "title": "Valid Anagram",
        "difficulty": "easy",
        "topic": "Strings",
        "tags": ["Hash Table", "String", "Sorting"],
        "company_tags": ["Google", "Amazon", "Bloomberg", "Uber"],
        "statement_md": "Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.\n\nAn Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "\"anagram\"\n\"nagaram\"",
                "expected_output": "true"
            },
            {
                "input_text": "\"rat\"\n\"car\"",
                "expected_output": "false"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "\"a\"\n\"ab\"",
                "expected_output": "false"
            },
            {
                "input_text": "\"listen\"\n\"silent\"",
                "expected_output": "true"
            },
            {
                "input_text": "\"fluster\"\n\"restful\"",
                "expected_output": "true"
            }
        ],
        "hints": [
            {"level": 1, "text": "If lengths are unequal, can they be anagrams?", "xp_cost": 2},
            {"level": 2, "text": "Count the frequency of each character in both strings.", "xp_cost": 5},
            {"level": 3, "text": "Use a fixed array of size 26 or a hash map to compare counts.", "xp_cost": 10}
        ],
        "editorial_md": """### Character Frequency Counting

1. If $len(s) \\neq len(t)$, return `False`.
2. Count character frequencies using a fixed 26-element array or hash table.
3. Increment counts for $s$ and decrement for $t$.
4. Check if all values are 0.

- **Time Complexity:** $O(n)$ where $n = len(s)$.
- **Space Complexity:** $O(1)$ since alphabet size is bounded (26 letters)."""
    },
    {
        "slug": "invert-binary-tree",
        "title": "Invert Binary Tree",
        "difficulty": "easy",
        "topic": "Trees",
        "tags": ["Tree", "DFS", "BFS", "Binary Tree"],
        "company_tags": ["Google", "Amazon", "Meta", "Twitter"],
        "statement_md": "Given the `root` of a binary tree represented as an array in level-order, invert the tree, and return its root representation.\n\nInverting a tree swaps every left child with its right child.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "[4, 2, 7, 1, 3, 6, 9]",
                "expected_output": "[4, 7, 2, 9, 6, 3, 1]"
            },
            {
                "input_text": "[2, 1, 3]",
                "expected_output": "[2, 3, 1]"
            },
            {
                "input_text": "[]",
                "expected_output": "[]"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "[1, 2]",
                "expected_output": "[1, null, 2]"
            },
            {
                "input_text": "[1]",
                "expected_output": "[1]"
            }
        ],
        "hints": [
            {"level": 1, "text": "What does inverting a node mean? Swapping its left and right pointers.", "xp_cost": 2},
            {"level": 2, "text": "Recursively invert the left subtree, recursively invert the right subtree, and swap them.", "xp_cost": 5},
            {"level": 3, "text": "Base case: if node is None/null, return None.", "xp_cost": 10}
        ],
        "editorial_md": """### Recursive Depth-First Search

For each node:
1. Base case: if node is null, return null.
2. Swap left and right child pointers.
3. Recursively call invert on left and right children.

```python
def invertTree(root):
    if not root:
        return None
    root.left, root.right = invertTree(root.right), invertTree(root.left)
    return root
```

- **Time Complexity:** $O(n)$ visiting each node once.
- **Space Complexity:** $O(h)$ recursion stack where $h$ is tree height."""
    },
    {
        "slug": "same-tree",
        "title": "Same Tree",
        "difficulty": "easy",
        "topic": "Trees",
        "tags": ["Tree", "Depth-First Search", "Binary Tree"],
        "company_tags": ["Google", "Amazon", "Microsoft", "LinkedIn"],
        "statement_md": "Given the roots of two binary trees `p` and `q`, write a function to check if they are the same or not.\n\nTwo binary trees are considered the same if they are structurally identical, and the nodes have the same value.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "[1, 2, 3]\n[1, 2, 3]",
                "expected_output": "true"
            },
            {
                "input_text": "[1, 2]\n[1, null, 2]",
                "expected_output": "false"
            },
            {
                "input_text": "[1, 2, 1]\n[1, 1, 2]",
                "expected_output": "false"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "[]\n[]",
                "expected_output": "true"
            },
            {
                "input_text": "[10, 5, 15]\n[10, 5, 15]",
                "expected_output": "true"
            }
        ],
        "hints": [
            {"level": 1, "text": "Check if both nodes are null at the same time.", "xp_cost": 2},
            {"level": 2, "text": "If only one is null, they cannot be identical.", "xp_cost": 5},
            {"level": 3, "text": "If values match, recursively verify both left subtrees and right subtrees.", "xp_cost": 10}
        ],
        "editorial_md": """### Structural and Value Tree Equality

```python
def isSameTree(p, q):
    if not p and not q:
        return True
    if not p or not q or p.val != q.val:
        return False
    return isSameTree(p.left, q.left) and isSameTree(p.right, q.right)
```

- **Time Complexity:** $O(n)$
- **Space Complexity:** $O(h)$"""
    },
    {
        "slug": "binary-tree-level-order-traversal",
        "title": "Binary Tree Level Order Traversal",
        "difficulty": "medium",
        "topic": "Trees",
        "tags": ["Tree", "BFS", "Binary Tree"],
        "company_tags": ["Amazon", "Microsoft", "Bloomberg", "Meta"],
        "statement_md": "Given the `root` of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "[3, 9, 20, null, null, 15, 7]",
                "expected_output": "[[3], [9, 20], [15, 7]]"
            },
            {
                "input_text": "[1]",
                "expected_output": "[[1]]"
            },
            {
                "input_text": "[]",
                "expected_output": "[]"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "[1, 2, 3, 4, 5]",
                "expected_output": "[[1], [2, 3], [4, 5]]"
            },
            {
                "input_text": "[1, 2, null, 3, null, 4]",
                "expected_output": "[[1], [2], [3], [4]]"
            }
        ],
        "hints": [
            {"level": 1, "text": "What data structure processes items in first-in-first-out (FIFO) order?", "xp_cost": 2},
            {"level": 2, "text": "Use a queue (collections.deque in Python).", "xp_cost": 5},
            {"level": 3, "text": "At each level, record queue length N, pop N elements, and append their children.", "xp_cost": 10}
        ],
        "editorial_md": """### Breadth-First Search with Queue

```python
from collections import deque

def levelOrder(root):
    if not root:
        return []
    res = []
    q = deque([root])
    while q:
        level_size = len(q)
        current_level = []
        for _ in range(level_size):
            node = q.popleft()
            current_level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        res.append(current_level)
    return res
```

- **Time Complexity:** $O(n)$
- **Space Complexity:** $O(n)$"""
    },
    {
        "slug": "validate-binary-search-tree",
        "title": "Validate Binary Search Tree",
        "difficulty": "medium",
        "topic": "Trees",
        "tags": ["Tree", "DFS", "Binary Search Tree"],
        "company_tags": ["Amazon", "Meta", "Google", "Microsoft"],
        "statement_md": "Given the `root` of a binary tree, determine if it is a valid binary search tree (BST).\n\nA **valid BST** is defined as follows:\n- The left subtree of a node contains only nodes with keys **strictly less than** the node's key.\n- The right subtree of a node contains only nodes with keys **strictly greater than** the node's key.\n- Both the left and right subtrees must also be binary search trees.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "[2, 1, 3]",
                "expected_output": "true"
            },
            {
                "input_text": "[5, 1, 4, null, null, 3, 6]",
                "expected_output": "false"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "[5, 4, 6, null, null, 3, 7]",
                "expected_output": "false"
            },
            {
                "input_text": "[2, 2, 2]",
                "expected_output": "false"
            },
            {
                "input_text": "[2147483647]",
                "expected_output": "true"
            }
        ],
        "hints": [
            {"level": 1, "text": "Checking only immediate children is not sufficient; all left descendants must be strictly smaller.", "xp_cost": 2},
            {"level": 2, "text": "Pass allowable valid range (low, high) down during traversal.", "xp_cost": 5},
            {"level": 3, "text": "Alternatively, an in-order traversal of a valid BST must yield strictly ascending values.", "xp_cost": 10}
        ],
        "editorial_md": """### Recursive Range Validation

```python
def isValidBST(root, low=float('-inf'), high=float('inf')) -> bool:
    if not root:
        return True
    if not (low < root.val < high):
        return False
    return isValidBST(root.left, low, root.val) and isValidBST(root.right, root.val, high)
```

- **Time Complexity:** $O(n)$
- **Space Complexity:** $O(h)$"""
    },
    {
        "slug": "jump-game",
        "title": "Jump Game",
        "difficulty": "medium",
        "topic": "Dynamic Programming",
        "tags": ["Array", "Dynamic Programming", "Greedy"],
        "company_tags": ["Amazon", "Apple", "Google", "Microsoft"],
        "statement_md": "You are given an integer array `nums`. You are initially positioned at the array's **first index**, and each element in the array represents your maximum jump length at that position.\n\nReturn `true` if you can reach the last index, or `false` otherwise.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "[2, 3, 1, 1, 4]",
                "expected_output": "true"
            },
            {
                "input_text": "[3, 2, 1, 0, 4]",
                "expected_output": "false"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "[0]",
                "expected_output": "true"
            },
            {
                "input_text": "[2, 0, 0]",
                "expected_output": "true"
            },
            {
                "input_text": "[1, 0, 1, 0]",
                "expected_output": "false"
            }
        ],
        "hints": [
            {"level": 1, "text": "Track the furthest index reachable so far.", "xp_cost": 2},
            {"level": 2, "text": "If the current index i exceeds the max reachable index, you are stuck.", "xp_cost": 5},
            {"level": 3, "text": "At each step: max_reach = max(max_reach, i + nums[i]). If max_reach >= n - 1, return true.", "xp_cost": 10}
        ],
        "editorial_md": """### Greedy Reachability

Maintain variable `max_reach = 0`. Iterate through array:
1. If $i > max\\_reach$, index $i$ cannot be reached -> return `False`.
2. Update $max\\_reach = \\max(max\\_reach, i + nums[i])$.
3. If $max\\_reach \\ge n - 1$, return `True`.

```python
def canJump(nums: list[int]) -> bool:
    max_reach = 0
    for i, jump in enumerate(nums):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + jump)
    return True
```

- **Time Complexity:** $O(n)$
- **Space Complexity:** $O(1)$"""
    },
    {
        "slug": "unique-paths",
        "title": "Unique Paths",
        "difficulty": "medium",
        "topic": "Dynamic Programming",
        "tags": ["Math", "Dynamic Programming", "Combinatorics"],
        "company_tags": ["Google", "Amazon", "Meta", "Adobe"],
        "statement_md": "There is a robot on an `m x n` grid. The robot is initially located at the top-left corner `(grid[0][0])` and tries to move to the bottom-right corner `(grid[m - 1][n - 1])`. The robot can only move either down or right at any point in time.\n\nGiven the two integers `m` and `n`, return the number of possible unique paths that the robot can take to reach the bottom-right corner.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "3\n7",
                "expected_output": "28"
            },
            {
                "input_text": "3\n2",
                "expected_output": "3"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "1\n1",
                "expected_output": "1"
            },
            {
                "input_text": "10\n10",
                "expected_output": "48620"
            },
            {
                "input_text": "1\n10",
                "expected_output": "1"
            }
        ],
        "hints": [
            {"level": 1, "text": "To reach cell (r, c), you must arrive from either (r-1, c) or (r, c-1).", "xp_cost": 2},
            {"level": 2, "text": "dp[r][c] = dp[r-1][c] + dp[r][c-1].", "xp_cost": 5},
            {"level": 3, "text": "You can optimize space to O(n) by using a single row.", "xp_cost": 10}
        ],
        "editorial_md": """### 1D Space Optimized Dynamic Programming

The recurrence is $dp[c] = dp[c] + dp[c-1]$.

```python
def uniquePaths(m: int, n: int) -> int:
    row = [1] * n
    for _ in range(m - 1):
        for c in range(1, n):
            row[c] += row[c - 1]
    return row[-1]
```

- **Time Complexity:** $O(m \\times n)$
- **Space Complexity:** $O(n)$"""
    },
    {
        "slug": "longest-common-subsequence",
        "title": "Longest Common Subsequence",
        "difficulty": "medium",
        "topic": "Dynamic Programming",
        "tags": ["String", "Dynamic Programming"],
        "company_tags": ["Amazon", "Microsoft", "Google", "Apple"],
        "statement_md": "Given two strings `text1` and `text2`, return the length of their longest common subsequence. If there is no common subsequence, return `0`.\n\nA **subsequence** of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "\"abcde\"\n\"ace\"",
                "expected_output": "3"
            },
            {
                "input_text": "\"abc\"\n\"abc\"",
                "expected_output": "3"
            },
            {
                "input_text": "\"abc\"\n\"def\"",
                "expected_output": "0"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "\"oxcp\"\n\"pxo\"",
                "expected_output": "1"
            },
            {
                "input_text": "\"ezupkr\"\n\"ubmrapg\"",
                "expected_output": "2"
            }
        ],
        "hints": [
            {"level": 1, "text": "If text1[i] == text2[j], LCS increases by 1.", "xp_cost": 2},
            {"level": 2, "text": "Otherwise, take max(LCS(i-1, j), LCS(i, j-1)).", "xp_cost": 5},
            {"level": 3, "text": "Build a 2D DP table of size (len(text1)+1) x (len(text2)+1).", "xp_cost": 10}
        ],
        "editorial_md": """### 2D Dynamic Programming

Let $dp[i][j]$ be LCS length for prefixes $text1[:i]$ and $text2[:j]$.
- If $text1[i-1] == text2[j-1]$: $dp[i][j] = 1 + dp[i-1][j-1]$
- Else: $dp[i][j] = \\max(dp[i-1][j], dp[i][j-1])$

```python
def longestCommonSubsequence(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]
```

- **Time Complexity:** $O(m \\times n)$
- **Space Complexity:** $O(m \\times n)$"""
    },
    {
        "slug": "combination-sum",
        "title": "Combination Sum",
        "difficulty": "medium",
        "topic": "Arrays",
        "tags": ["Array", "Backtracking"],
        "company_tags": ["Airbnb", "Meta", "Amazon", "Microsoft"],
        "statement_md": "Given an array of **distinct** integers `candidates` and a target integer `target`, return a list of all **unique combinations** of `candidates` where the chosen numbers sum to `target`. You may return the combinations in any order.\n\nThe **same** number may be chosen from `candidates` an unlimited number of times.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "[2, 3, 6, 7]\n7",
                "expected_output": "[[2, 2, 3], [7]]"
            },
            {
                "input_text": "[2, 3, 5]\n8",
                "expected_output": "[[2, 2, 2, 2], [2, 3, 3], [3, 5]]"
            },
            {
                "input_text": "[2]\n1",
                "expected_output": "[]"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "[1]\n2",
                "expected_output": "[[1, 1]]"
            },
            {
                "input_text": "[3, 5, 8]\n11",
                "expected_output": "[[3, 3, 5], [3, 8]]"
            }
        ],
        "hints": [
            {"level": 1, "text": "At each step, you can either pick the current number again or move to the next candidate.", "xp_cost": 2},
            {"level": 2, "text": "Backtrack by pushing the candidate, exploring, and popping it off.", "xp_cost": 5},
            {"level": 3, "text": "Prune branches where running total exceeds target.", "xp_cost": 10}
        ],
        "editorial_md": """### Backtracking Search

```python
def combinationSum(candidates: list[int], target: int) -> list[list[int]]:
    res = []
    def backtrack(idx, current, remaining):
        if remaining == 0:
            res.append(list(current))
            return
        if remaining < 0 or idx >= len(candidates):
            return
        
        # Include current candidate
        current.append(candidates[idx])
        backtrack(idx, current, remaining - candidates[idx])
        current.pop()
        
        # Skip current candidate
        backtrack(idx + 1, current, remaining)
        
    backtrack(0, [], target)
    return res
```

- **Time Complexity:** $O(2^t)$ where $t = target / \\min(candidates)$.
- **Space Complexity:** $O(t)$ recursion depth."""
    },
    {
        "slug": "rotting-oranges",
        "title": "Rotting Oranges",
        "difficulty": "medium",
        "topic": "Graphs",
        "tags": ["Array", "BFS", "Matrix"],
        "company_tags": ["Amazon", "Microsoft", "Google", "Oracle"],
        "statement_md": "You are given an `m x n` grid where each cell can have one of three values:\n- `0` representing an empty cell,\n- `1` representing a fresh orange, or\n- `2` representing a rotten orange.\n\nEvery minute, any fresh orange that is **4-directionally adjacent** to a rotten orange becomes rotten.\n\nReturn the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return `-1`.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "[[2, 1, 1], [1, 1, 0], [0, 1, 1]]",
                "expected_output": "4"
            },
            {
                "input_text": "[[2, 1, 1], [0, 1, 1], [1, 0, 1]]",
                "expected_output": "-1"
            },
            {
                "input_text": "[[0, 2]]",
                "expected_output": "0"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "[[1]]",
                "expected_output": "-1"
            },
            {
                "input_text": "[[2, 2], [1, 1], [0, 0], [2, 0]]",
                "expected_output": "1"
            }
        ],
        "hints": [
            {"level": 1, "text": "This is a multi-source shortest path problem.", "xp_cost": 2},
            {"level": 2, "text": "Initialize a queue with all initially rotten oranges (cells with value 2) and count total fresh oranges.", "xp_cost": 5},
            {"level": 3, "text": "Process minute-by-minute with level-by-level BFS. If fresh count drops to 0, return elapsed minutes.", "xp_cost": 10}
        ],
        "editorial_md": """### Multi-Source Breadth-First Search

```python
from collections import deque

def orangesRotting(grid: list[list[int]]) -> int:
    R, C = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 2:
                q.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1
                
    if fresh == 0:
        return 0
        
    minutes = 0
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while q and fresh > 0:
        minutes += 1
        for _ in range(len(q)):
            r, c = q.popleft()
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    q.append((nr, nc))
                    
    return minutes if fresh == 0 else -1
```

- **Time Complexity:** $O(R \\times C)$
- **Space Complexity:** $O(R \\times C)$"""
    },
    {
        "slug": "top-k-frequent-elements",
        "title": "Top K Frequent Elements",
        "difficulty": "medium",
        "topic": "Arrays",
        "tags": ["Array", "Hash Table", "Heap", "Bucket Sort"],
        "company_tags": ["Amazon", "Meta", "Google", "Microsoft"],
        "statement_md": "Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in **any order**.\n\nYour algorithm's time complexity must be better than $O(n \\log n)$, where $n$ is the array's size.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "[1, 1, 1, 2, 2, 3]\n2",
                "expected_output": "[1, 2]"
            },
            {
                "input_text": "[1]\n1",
                "expected_output": "[1]"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "[4, 1, -1, 2, -1, 2, 3]\n2",
                "expected_output": "[-1, 2]"
            },
            {
                "input_text": "[1, 2, 3, 4, 5, 5, 5, 6, 6, 7]\n1",
                "expected_output": "[5]"
            }
        ],
        "hints": [
            {"level": 1, "text": "First, create a frequency map of each number.", "xp_cost": 2},
            {"level": 2, "text": "A min-heap of size k gives O(n log k) time.", "xp_cost": 5},
            {"level": 3, "text": "Bucket sort by frequency (max possible count is n) achieves optimal O(n) time.", "xp_cost": 10}
        ],
        "editorial_md": """### Linear Time Bucket Sort

1. Count frequency using a hash map: $O(n)$.
2. Allocate array of buckets from index 0 to $n$. Place numbers into bucket index equal to their frequency.
3. Traverse buckets from index $n$ down to 1, collecting elements until $k$ elements are retrieved.

```python
from collections import Counter

def topKFrequent(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in count.items():
        buckets[freq].append(num)
        
    res = []
    for freq in range(len(buckets) - 1, 0, -1):
        for num in buckets[freq]:
            res.append(num)
            if len(res) == k:
                return res
    return res
```

- **Time Complexity:** $O(n)$
- **Space Complexity:** $O(n)$"""
    },
    {
        "slug": "insert-interval",
        "title": "Insert Interval",
        "difficulty": "medium",
        "topic": "Arrays",
        "tags": ["Array"],
        "company_tags": ["Google", "Meta", "LinkedIn", "Amazon"],
        "statement_md": "You are given an array of non-overlapping intervals `intervals` where `intervals[i] = [start_i, end_i]` sorted in ascending order by `start_i`. You are also given an interval `newInterval = [start, end]`.\n\nInsert `newInterval` into `intervals` such that `intervals` is still sorted in ascending order and has no overlapping intervals (merge overlapping intervals if necessary).\n\nReturn `intervals` after the insertion.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "[[1, 3], [6, 9]]\n[2, 5]",
                "expected_output": "[[1, 5], [6, 9]]"
            },
            {
                "input_text": "[[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]]\n[4, 8]",
                "expected_output": "[[1, 2], [3, 10], [12, 16]]"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "[]\n[5, 7]",
                "expected_output": "[[5, 7]]"
            },
            {
                "input_text": "[[1, 5]]\n[2, 3]",
                "expected_output": "[[1, 5]]"
            },
            {
                "input_text": "[[1, 5]]\n[6, 8]",
                "expected_output": "[[1, 5], [6, 8]]"
            }
        ],
        "hints": [
            {"level": 1, "text": "Three phases: intervals strictly before newInterval, overlapping intervals to merge, intervals strictly after.", "xp_cost": 2},
            {"level": 2, "text": "While interval[1] < newInterval[0], append to result.", "xp_cost": 5},
            {"level": 3, "text": "While interval[0] <= newInterval[1], merge: newInterval = [min(new[0], int[0]), max(new[1], int[1])].", "xp_cost": 10}
        ],
        "editorial_md": """### Three-Phase Linear Sweep

```python
def insert(intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
    res = []
    i, n = 0, len(intervals)
    
    # 1. Add all intervals before newInterval
    while i < n and intervals[i][1] < newInterval[0]:
        res.append(intervals[i])
        i += 1
        
    # 2. Merge overlapping intervals
    while i < n and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        i += 1
    res.append(newInterval)
    
    # 3. Add remaining intervals
    while i < n:
        res.append(intervals[i])
        i += 1
        
    return res
```

- **Time Complexity:** $O(n)$
- **Space Complexity:** $O(n)$ for output list."""
    },
    {
        "slug": "non-overlapping-intervals",
        "title": "Non-overlapping Intervals",
        "difficulty": "medium",
        "topic": "Arrays",
        "tags": ["Array", "Dynamic Programming", "Greedy", "Sorting"],
        "company_tags": ["Meta", "Amazon", "Google", "Microsoft"],
        "statement_md": "Given an array of intervals `intervals` where `intervals[i] = [start_i, end_i]`, return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "[[1, 2], [2, 3], [3, 4], [1, 3]]",
                "expected_output": "1"
            },
            {
                "input_text": "[[1, 2], [1, 2], [1, 2]]",
                "expected_output": "2"
            },
            {
                "input_text": "[[1, 2], [2, 3]]",
                "expected_output": "0"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "[[1, 100], [11, 22], [1, 11], [2, 12]]",
                "expected_output": "2"
            },
            {
                "input_text": "[[-52, 31], [-73, -26], [82, 97], [-65, -11], [-62, -49]]",
                "expected_output": "3"
            }
        ],
        "hints": [
            {"level": 1, "text": "This is equivalent to finding the maximum number of compatible non-overlapping intervals (Interval Scheduling).", "xp_cost": 2},
            {"level": 2, "text": "Sort intervals by their ending times.", "xp_cost": 5},
            {"level": 3, "text": "Greedily keep the interval that finishes earliest to leave room for future intervals.", "xp_cost": 10}
        ],
        "editorial_md": """### Greedy Interval Scheduling by End Time

1. Sort intervals by end time `intervals.sort(key=lambda x: x[1])`.
2. Maintain `prev_end = float('-inf')` and `removed = 0`.
3. If `start >= prev_end`, keep interval and update `prev_end = end`.
4. Otherwise, it overlaps with the earliest finishing interval, so discard it: `removed += 1`.

- **Time Complexity:** $O(n \\log n)$
- **Space Complexity:** $O(1)$ auxiliary."""
    },
    {
        "slug": "rotate-image",
        "title": "Rotate Image",
        "difficulty": "medium",
        "topic": "Arrays",
        "tags": ["Array", "Math", "Matrix"],
        "company_tags": ["Amazon", "Microsoft", "Apple", "Uber"],
        "statement_md": "You are given an `n x n` 2D `matrix` representing an image, rotate the image by **90 degrees clockwise**.\n\nYou have to rotate the image **in-place**, which means you have to modify the input 2D matrix directly.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "[[1, 2, 3], [4, 5, 6], [7, 8, 9]]",
                "expected_output": "[[7, 4, 1], [8, 5, 2], [9, 6, 3]]"
            },
            {
                "input_text": "[[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]",
                "expected_output": "[[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]]"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "[[1]]",
                "expected_output": "[[1]]"
            },
            {
                "input_text": "[[1, 2], [3, 4]]",
                "expected_output": "[[3, 1], [4, 2]]"
            }
        ],
        "hints": [
            {"level": 1, "text": "Rotating by 90 degrees clockwise is identical to transposing the matrix then reversing each row.", "xp_cost": 2},
            {"level": 2, "text": "Transpose: swap matrix[i][j] with matrix[j][i].", "xp_cost": 5},
            {"level": 3, "text": "Reverse each row: matrix[i].reverse().", "xp_cost": 10}
        ],
        "editorial_md": """### Transpose and Reflect

1. **Transpose** the matrix: Swap `matrix[i][j]` with `matrix[j][i]` for $i < j$.
2. **Reflect** horizontally: Reverse each row `matrix[i] = matrix[i][::-1]`.

```python
def rotate(matrix: list[list[int]]) -> list[list[int]]:
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:
        row.reverse()
    return matrix
```

- **Time Complexity:** $O(n^2)$
- **Space Complexity:** $O(1)$ in-place."""
    },
    {
        "slug": "spiral-matrix",
        "title": "Spiral Matrix",
        "difficulty": "medium",
        "topic": "Arrays",
        "tags": ["Array", "Matrix", "Simulation"],
        "company_tags": ["Microsoft", "Amazon", "Apple", "Google"],
        "statement_md": "Given an `m x n` matrix, return all elements of the `matrix` in spiral order.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "[[1, 2, 3], [4, 5, 6], [7, 8, 9]]",
                "expected_output": "[1, 2, 3, 6, 9, 8, 7, 4, 5]"
            },
            {
                "input_text": "[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]",
                "expected_output": "[1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "[[1]]",
                "expected_output": "[1]"
            },
            {
                "input_text": "[[1, 2, 3, 4]]",
                "expected_output": "[1, 2, 3, 4]"
            },
            {
                "input_text": "[[1], [2], [3], [4]]",
                "expected_output": "[1, 2, 3, 4]"
            }
        ],
        "hints": [
            {"level": 1, "text": "Maintain 4 boundary pointers: top, bottom, left, and right.", "xp_cost": 2},
            {"level": 2, "text": "Traverse left->right along top, top->bottom along right, right->left along bottom, bottom->top along left.", "xp_cost": 5},
            {"level": 3, "text": "Contract the respective boundary after each traversal direction.", "xp_cost": 10}
        ],
        "editorial_md": """### Boundary Traversal Simulation

```python
def spiralOrder(matrix: list[list[int]]) -> list[int]:
    res = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            res.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1):
            res.append(matrix[r][right])
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1):
                res.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1):
                res.append(matrix[r][left])
            left += 1
            
    return res
```

- **Time Complexity:** $O(m \\times n)$
- **Space Complexity:** $O(1)$ auxiliary."""
    },
    {
        "slug": "palindromic-substrings",
        "title": "Palindromic Substrings",
        "difficulty": "medium",
        "topic": "Strings",
        "tags": ["Two Pointers", "String", "Dynamic Programming"],
        "company_tags": ["Meta", "Amazon", "Twitter", "Goldman Sachs"],
        "statement_md": "Given a string `s`, return the number of **palindromic substrings** in it.\n\nA string is a **palindrome** when it reads the same backward as forward.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "\"abc\"",
                "expected_output": "3"
            },
            {
                "input_text": "\"aaa\"",
                "expected_output": "6"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "\"a\"",
                "expected_output": "1"
            },
            {
                "input_text": "\"abccba\"",
                "expected_output": "9"
            }
        ],
        "hints": [
            {"level": 1, "text": "Every palindrome has a center.", "xp_cost": 2},
            {"level": 2, "text": "There are 2n - 1 potential centers (odd-length center at i, even-length center between i and i+1).", "xp_cost": 5},
            {"level": 3, "text": "Expand outward from each center while characters match.", "xp_cost": 10}
        ],
        "editorial_md": """### Expand Around Centers

```python
def countSubstrings(s: str) -> int:
    n = len(s)
    total = 0
    def count_from(l, r):
        c = 0
        while l >= 0 and r < n and s[l] == s[r]:
            c += 1
            l -= 1
            r += 1
        return c
    for i in range(n):
        total += count_from(i, i)     # Odd length
        total += count_from(i, i + 1) # Even length
    return total
```

- **Time Complexity:** $O(n^2)$
- **Space Complexity:** $O(1)$"""
    },
    {
        "slug": "decode-ways",
        "title": "Decode Ways",
        "difficulty": "medium",
        "topic": "Dynamic Programming",
        "tags": ["String", "Dynamic Programming"],
        "company_tags": ["Meta", "Amazon", "Uber", "Google"],
        "statement_md": "A message containing letters from A-Z can be encoded into numbers using the following mapping:\n'A' -> \"1\", 'B' -> \"2\", ... 'Z' -> \"26\".\n\nTo decode an encoded message, all the digits must be grouped and mapped back into letters.\n\nGiven a string `s` containing only digits, return the **number of ways** to decode it.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "\"12\"",
                "expected_output": "2"
            },
            {
                "input_text": "\"226\"",
                "expected_output": "3"
            },
            {
                "input_text": "\"06\"",
                "expected_output": "0"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "\"0\"",
                "expected_output": "0"
            },
            {
                "input_text": "\"10\"",
                "expected_output": "1"
            },
            {
                "input_text": "\"27\"",
                "expected_output": "1"
            },
            {
                "input_text": "\"1111111111\"",
                "expected_output": "89"
            }
        ],
        "hints": [
            {"level": 1, "text": "A leading zero can never be decoded.", "xp_cost": 2},
            {"level": 2, "text": "At index i, consider decoding 1 digit s[i-1] (valid if != '0') and 2 digits s[i-2:i] (valid if between 10 and 26).", "xp_cost": 5},
            {"level": 3, "text": "Similar to Fibonacci sequence with conditional additions.", "xp_cost": 10}
        ],
        "editorial_md": """### Constant-Space Dynamic Programming

```python
def numDecodings(s: str) -> int:
    if not s or s[0] == '0':
        return 0
    prev2, prev1 = 1, 1
    for i in range(1, len(s)):
        cur = 0
        if s[i] != '0':
            cur += prev1
        two_digit = int(s[i - 1:i + 1])
        if 10 <= two_digit <= 26:
            cur += prev2
        prev2, prev1 = prev1, cur
    return prev1
```

- **Time Complexity:** $O(n)$
- **Space Complexity:** $O(1)$"""
    },
    {
        "slug": "redundant-connection",
        "title": "Redundant Connection",
        "difficulty": "medium",
        "topic": "Graphs",
        "tags": ["Tree", "Union Find", "Graph"],
        "company_tags": ["Google", "Amazon", "Microsoft", "Uber"],
        "statement_md": "In this problem, a tree is an undirected graph that is connected and has no cycles.\n\nYou are given a graph that started as a tree with `n` nodes labeled from `1` to `n`, with one additional edge added. The added edge has two different vertices chosen from `1` to `n`, and was not an edge that already existed.\n\nReturn an edge that can be removed so that the resulting graph is a tree of `n` nodes. If there are multiple answers, return the answer that occurs last in the input.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "[[1, 2], [1, 3], [2, 3]]",
                "expected_output": "[2, 3]"
            },
            {
                "input_text": "[[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]",
                "expected_output": "[1, 4]"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "[[1, 3], [3, 4], [1, 5], [3, 5], [2, 3]]",
                "expected_output": "[3, 5]"
            },
            {
                "input_text": "[[2, 7], [7, 8], [3, 6], [2, 5], [6, 8], [4, 8], [2, 8], [1, 8], [7, 10], [3, 9]]",
                "expected_output": "[2, 8]"
            }
        ],
        "hints": [
            {"level": 1, "text": "An edge creating a cycle connects two nodes that are already in the same connected component.", "xp_cost": 2},
            {"level": 2, "text": "Use the Disjoint Set Union (Union-Find) data structure.", "xp_cost": 5},
            {"level": 3, "text": "If find(u) == find(v), edge [u, v] is the redundant edge.", "xp_cost": 10}
        ],
        "editorial_md": """### Disjoint Set Union (DSU)

```python
def findRedundantConnection(edges: list[list[int]]) -> list[int]:
    parent = list(range(len(edges) + 1))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
        
    for u, v in edges:
        root_u, root_v = find(u), find(v)
        if root_u == root_v:
            return [u, v]
        parent[root_u] = root_v
        
    return []
```

- **Time Complexity:** $O(n \\cdot \\alpha(n)) \\approx O(n)$
- **Space Complexity:** $O(n)$"""
    },
    {
        "slug": "word-search",
        "title": "Word Search",
        "difficulty": "medium",
        "topic": "Graphs",
        "tags": ["Array", "Backtracking", "Matrix"],
        "company_tags": ["Bloomberg", "Amazon", "Microsoft", "Twitter"],
        "statement_md": "Given an `m x n` grid of characters `board` and a string `word`, return `true` if `word` exists in the grid.\n\nThe word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "[[\"A\", \"B\", \"C\", \"E\"], [\"S\", \"F\", \"C\", \"S\"], [\"A\", \"D\", \"E\", \"E\"]]\n\"ABCCED\"",
                "expected_output": "true"
            },
            {
                "input_text": "[[\"A\", \"B\", \"C\", \"E\"], [\"S\", \"F\", \"C\", \"S\"], [\"A\", \"D\", \"E\", \"E\"]]\n\"SEE\"",
                "expected_output": "true"
            },
            {
                "input_text": "[[\"A\", \"B\", \"C\", \"E\"], [\"S\", \"F\", \"C\", \"S\"], [\"A\", \"D\", \"E\", \"E\"]]\n\"ABCB\"",
                "expected_output": "false"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "[[\"a\"]]\n\"a\"",
                "expected_output": "true"
            },
            {
                "input_text": "[[\"a\", \"b\"]]\n\"ba\"",
                "expected_output": "true"
            }
        ],
        "hints": [
            {"level": 1, "text": "Iterate through every cell to find a match with word[0].", "xp_cost": 2},
            {"level": 2, "text": "Perform depth-first search in 4 directions.", "xp_cost": 5},
            {"level": 3, "text": "Temporarily mark board[r][c] as visited (e.g. '#') and restore it upon backtracking.", "xp_cost": 10}
        ],
        "editorial_md": """### Backtracking DFS with In-Place Visited Mask

```python
def exist(board: list[list[str]], word: str) -> bool:
    R, C = len(board), len(board[0])
    
    def dfs(r, c, idx):
        if idx == len(word):
            return True
        if not (0 <= r < R and 0 <= c < C) or board[r][c] != word[idx]:
            return False
        
        temp = board[r][c]
        board[r][c] = '#'
        found = (dfs(r + 1, c, idx + 1) or
                 dfs(r - 1, c, idx + 1) or
                 dfs(r, c + 1, idx + 1) or
                 dfs(r, c - 1, idx + 1))
        board[r][c] = temp
        return found

    for r in range(R):
        for c in range(C):
            if dfs(r, c, 0):
                return True
    return False
```

- **Time Complexity:** $O(R \\times C \\times 4^L)$ where $L = len(word)$.
- **Space Complexity:** $O(L)$ stack depth."""
    },
    {
        "slug": "gas-station",
        "title": "Gas Station",
        "difficulty": "medium",
        "topic": "Arrays",
        "tags": ["Array", "Greedy"],
        "company_tags": ["Amazon", "Google", "Microsoft", "Bloomberg"],
        "statement_md": "There are `n` gas stations along a circular route, where the amount of gas at the $i$-th station is `gas[i]`.\n\nYou have a car with an unlimited gas tank and it costs `cost[i]` of gas to travel from the $i$-th station to its next $(i + 1)$-th station. You begin the journey with an empty tank at one of the gas stations.\n\nGiven two integer arrays `gas` and `cost`, return the starting gas station's index if you can travel around the circuit once in the clockwise direction, otherwise return `-1`.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "[1, 2, 3, 4, 5]\n[3, 4, 5, 1, 2]",
                "expected_output": "3"
            },
            {
                "input_text": "[2, 3, 4]\n[3, 4, 3]",
                "expected_output": "-1"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "[5, 1, 2, 3, 4]\n[4, 4, 1, 5, 1]",
                "expected_output": "4"
            },
            {
                "input_text": "[3, 1, 1]\n[1, 2, 2]",
                "expected_output": "0"
            }
        ],
        "hints": [
            {"level": 1, "text": "If total sum(gas) < sum(cost), it is mathematically impossible to complete the circuit.", "xp_cost": 2},
            {"level": 2, "text": "If tank drops below zero traveling from i to j, no station between i and j can be the starting station.", "xp_cost": 5},
            {"level": 3, "text": "Reset current_tank to 0 and set start = i + 1 whenever current_tank < 0.", "xp_cost": 10}
        ],
        "editorial_md": """### One-Pass Greedy Algorithm

```python
def canCompleteCircuit(gas: list[int], cost: list[int]) -> int:
    if sum(gas) < sum(cost):
        return -1
    total_surplus, current_surplus, start = 0, 0, 0
    for i in range(len(gas)):
        current_surplus += gas[i] - cost[i]
        if current_surplus < 0:
            start = i + 1
            current_surplus = 0
    return start
```

- **Time Complexity:** $O(n)$
- **Space Complexity:** $O(1)$"""
    },
    {
        "slug": "median-of-two-sorted-arrays",
        "title": "Median of Two Sorted Arrays",
        "difficulty": "hard",
        "topic": "Binary Search",
        "tags": ["Array", "Binary Search", "Divide and Conquer"],
        "company_tags": ["Google", "Amazon", "Apple", "Microsoft", "Goldman Sachs"],
        "statement_md": "Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the **median** of the two sorted arrays.\n\nThe overall run time complexity should be $O(\\log (m+n))$.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "[1, 3]\n[2]",
                "expected_output": "2.0"
            },
            {
                "input_text": "[1, 2]\n[3, 4]",
                "expected_output": "2.5"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "[0, 0]\n[0, 0]",
                "expected_output": "0.0"
            },
            {
                "input_text": "[]\n[1]",
                "expected_output": "1.0"
            },
            {
                "input_text": "[2]\n[]",
                "expected_output": "2.0"
            }
        ],
        "hints": [
            {"level": 1, "text": "Binary search on the partition of the smaller array.", "xp_cost": 2},
            {"level": 2, "text": "Partition both arrays such that left half and right half contain equal elements.", "xp_cost": 5},
            {"level": 3, "text": "Ensure maxLeftA <= minRightB and maxLeftB <= minRightA.", "xp_cost": 10}
        ],
        "editorial_md": """### Optimal Binary Search on Partition

Binary search on smaller array $A$ (size $m$) to find partition index $i$:
1. $j = (m + n + 1) // 2 - i$
2. If $maxLeftA \\le minRightB$ and $maxLeftB \\le minRightA$, valid partition found!
3. If total length is odd: $\\max(maxLeftA, maxLeftB)$.
4. If even: $(\\max(maxLeftA, maxLeftB) + \\min(minRightA, minRightB)) / 2.0$.

```python
def findMedianSortedArrays(nums1: list[int], nums2: list[int]) -> float:
    A, B = nums1, nums2
    if len(A) > len(B):
        A, B = B, A
    m, n = len(A), len(B)
    half = (m + n + 1) // 2
    l, r = 0, m
    
    while l <= r:
        i = (l + r) // 2
        j = half - i
        
        A_left = A[i - 1] if i > 0 else float('-inf')
        A_right = A[i] if i < m else float('inf')
        B_left = B[j - 1] if j > 0 else float('-inf')
        B_right = B[j] if j < n else float('inf')
        
        if A_left <= B_right and B_left <= A_right:
            if (m + n) % 2:
                return float(max(A_left, B_left))
            return (max(A_left, B_left) + min(A_right, B_right)) / 2.0
        elif A_left > B_right:
            r = i - 1
        else:
            l = i + 1
    return 0.0
```

- **Time Complexity:** $O(\\log(\\min(m, n)))$
- **Space Complexity:** $O(1)$"""
    }
]

def main():
    target_dir = os.path.join(os.path.dirname(__file__), "..", "..", "content", "problems")
    os.makedirs(target_dir, exist_ok=True)
    count = 0
    for p in PROBLEMS_DATA:
        fpath = os.path.join(target_dir, f"{p['slug']}.json")
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(p, f, indent=2)
        count += 1
    print(f"Generated {count} problems in {target_dir}")

if __name__ == "__main__":
    main()
