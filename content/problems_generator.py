import json
import os

problems = [
    {
        "slug": "two-sum",
        "title": "Two Sum",
        "difficulty": "easy",
        "topic": "Arrays",
        "tags": ["Array", "Hash Map"],
        "company_tags": ["Google", "Amazon", "Meta", "Microsoft"],
        "statement_md": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.\n\nYou may assume that each input would have **exactly one solution**, and you may not use the same element twice.\n\nYou can return the answer in any order.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {"input_text": "[2, 7, 11, 15]\n9", "expected_output": "[0, 1]"},
            {"input_text": "[3, 2, 4]\n6", "expected_output": "[1, 2]"},
            {"input_text": "[3, 3]\n6", "expected_output": "[0, 1]"}
        ],
        "hidden_tests": [
            {"input_text": "[1, 5, 7, 12, 19]\n13", "expected_output": "[0, 3]"},
            {"input_text": "[-3, 4, 3, 90]\n0", "expected_output": "[0, 2]"},
            {"input_text": "[0, 4, 3, 0]\n0", "expected_output": "[0, 3]"},
            {"input_text": "[-1, -2, -3, -4, -5]\n-8", "expected_output": "[2, 4]"},
            {"input_text": "[1000000, 500, 1000000]\n2000000", "expected_output": "[0, 2]"}
        ],
        "hints": [
            {"level": 1, "text": "Can you check if the complement (target - current) exists?", "xp_cost": 2},
            {"level": 2, "text": "Use a Hash Map to record previously visited numbers and their indices.", "xp_cost": 5},
            {"level": 3, "text": "As you iterate over `nums`, lookup `target - num` in your dictionary. If found, return `[seen[target - num], i]`. Otherwise store `seen[num] = i`.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: One-Pass Hash Map\n\nStore indices in a map `seen`. At each number `x`, check if `target - x` is in `seen`. If so, return `[seen[target - x], index]`. Otherwise record `seen[x] = index`.\n\n- Time Complexity: $O(n)$\n- Space Complexity: $O(n)$"
    },
    {
        "slug": "valid-parentheses",
        "title": "Valid Parentheses",
        "difficulty": "easy",
        "topic": "Stack and Queue",
        "tags": ["Stack", "String"],
        "company_tags": ["Amazon", "Bloomberg", "Google"],
        "statement_md": "Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.\n\nAn input string is valid if:\n1. Open brackets must be closed by the same type of brackets.\n2. Open brackets must be closed in the correct order.\n3. Every close bracket has a corresponding open bracket of the same type.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {"input_text": "\"()\"", "expected_output": "true"},
            {"input_text": "\"()[]{}\"", "expected_output": "true"},
            {"input_text": "\"(]\"", "expected_output": "false"}
        ],
        "hidden_tests": [
            {"input_text": "\"([{}])\"", "expected_output": "true"},
            {"input_text": "\"(((\"", "expected_output": "false"},
            {"input_text": "\")))\"", "expected_output": "false"},
            {"input_text": "\"{[]}\"", "expected_output": "true"},
            {"input_text": "\"[(])\"", "expected_output": "false"}
        ],
        "hints": [
            {"level": 1, "text": "Think of what data structure gives Last-In-First-Out access.", "xp_cost": 2},
            {"level": 2, "text": "A stack allows you to push opening brackets and pop them when matching closing ones appear.", "xp_cost": 5},
            {"level": 3, "text": "Map each closing bracket to its opening counterpart. Pop on close, check matching, and ensure stack is empty at the end.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Stack\n\nPush open brackets onto a stack. When finding a closed bracket, check if top of stack matches. Finally, verify stack is empty.\n\n- Time Complexity: $O(n)$\n- Space Complexity: $O(n)$"
    },
    {
        "slug": "best-time-to-buy-and-sell-stock",
        "title": "Best Time to Buy and Sell Stock",
        "difficulty": "easy",
        "topic": "Arrays",
        "tags": ["Array", "Dynamic Programming"],
        "company_tags": ["Amazon", "Apple", "Microsoft"],
        "statement_md": "You are given an array `prices` where `prices[i]` is the price of a given stock on the $i$-th day.\n\nYou want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.\n\nReturn the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {"input_text": "[7, 1, 5, 3, 6, 4]", "expected_output": "5"},
            {"input_text": "[7, 6, 4, 3, 1]", "expected_output": "0"}
        ],
        "hidden_tests": [
            {"input_text": "[2, 4, 1]", "expected_output": "2"},
            {"input_text": "[3, 2, 6, 5, 0, 3]", "expected_output": "4"},
            {"input_text": "[1, 2]", "expected_output": "1"},
            {"input_text": "[1]", "expected_output": "0"},
            {"input_text": "[2, 1, 2, 1, 0, 1, 2]", "expected_output": "2"}
        ],
        "hints": [
            {"level": 1, "text": "Can you track the minimum price seen so far while iterating?", "xp_cost": 2},
            {"level": 2, "text": "Every day you consider selling at `price`, compare with `min_price` to update `max_profit`.", "xp_cost": 5},
            {"level": 3, "text": "Maintain `lowest = min(lowest, price)` and `best = max(best, price - lowest)`. Single pass.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: One-Pass Tracking\n\nKeep track of the minimum price encountered so far. At each step, calculate the potential profit if sold today, updating maximum profit.\n\n- Time Complexity: $O(n)$\n- Space Complexity: $O(1)$"
    },
    {
        "slug": "binary-search",
        "title": "Binary Search",
        "difficulty": "easy",
        "topic": "Binary Search",
        "tags": ["Binary Search", "Array"],
        "company_tags": ["Google", "Microsoft"],
        "statement_md": "Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`. If `target` exists, then return its index. Otherwise, return -1.\n\nYou must write an algorithm with $O(\\log n)$ runtime complexity.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {"input_text": "[-1, 0, 3, 5, 9, 12]\n9", "expected_output": "4"},
            {"input_text": "[-1, 0, 3, 5, 9, 12]\n2", "expected_output": "-1"}
        ],
        "hidden_tests": [
            {"input_text": "[5]\n5", "expected_output": "0"},
            {"input_text": "[5]\n-5", "expected_output": "-1"},
            {"input_text": "[1, 3, 5, 7, 9, 11]\n1", "expected_output": "0"},
            {"input_text": "[1, 3, 5, 7, 9, 11]\n11", "expected_output": "5"},
            {"input_text": "[2, 5]\n5", "expected_output": "1"}
        ],
        "hints": [
            {"level": 1, "text": "Since the array is sorted, comparing target with the middle element halves the search space.", "xp_cost": 2},
            {"level": 2, "text": "Use two pointers `lo` and `hi`. Calculate `mid = (lo + hi) // 2`.", "xp_cost": 5},
            {"level": 3, "text": "If `nums[mid] == target`, return `mid`. If `nums[mid] < target`, set `lo = mid + 1`, else `hi = mid - 1`.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Classical Binary Search\n\nDivide and conquer by inspecting the midpoint. Halving the problem at each iteration guarantees logarithmic running time.\n\n- Time Complexity: $O(\\log n)$\n- Space Complexity: $O(1)$"
    },
    {
        "slug": "reverse-linked-list",
        "title": "Reverse Linked List",
        "difficulty": "easy",
        "topic": "Linked List",
        "tags": ["Linked List", "Recursion"],
        "company_tags": ["Amazon", "Adobe", "Meta"],
        "statement_md": "Given the head of a singly linked list, reverse the list, and return the reversed list.\n\nInput representation is given as a list of numbers representing the node values.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {"input_text": "[1, 2, 3, 4, 5]", "expected_output": "[5, 4, 3, 2, 1]"},
            {"input_text": "[1, 2]", "expected_output": "[2, 1]"},
            {"input_text": "[]", "expected_output": "[]"}
        ],
        "hidden_tests": [
            {"input_text": "[42]", "expected_output": "[42]"},
            {"input_text": "[1, 2, 3]", "expected_output": "[3, 2, 1]"},
            {"input_text": "[9, 8, 7, 6, 5, 4, 3, 2, 1]", "expected_output": "[1, 2, 3, 4, 5, 6, 7, 8, 9]"}
        ],
        "hints": [
            {"level": 1, "text": "You need to change the `next` pointer of each node to point to its predecessor.", "xp_cost": 2},
            {"level": 2, "text": "Keep track of `prev`, `curr`, and `nxt` pointers.", "xp_cost": 5},
            {"level": 3, "text": "At each node: `nxt = curr.next; curr.next = prev; prev = curr; curr = nxt`. Return `prev`.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Iterative 3-Pointers\n\nIterate through the linked list, redirecting each node's `next` pointer to the previously visited node.\n\n- Time Complexity: $O(n)$\n- Space Complexity: $O(1)$"
    },
    {
        "slug": "maximum-subarray",
        "title": "Maximum Subarray",
        "difficulty": "medium",
        "topic": "Arrays",
        "tags": ["Array", "Dynamic Programming", "Divide and Conquer"],
        "company_tags": ["Amazon", "Microsoft", "LinkedIn"],
        "statement_md": "Given an integer array `nums`, find the subarray with the largest sum, and return its sum.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {"input_text": "[-2, 1, -3, 4, -1, 2, 1, -5, 4]", "expected_output": "6"},
            {"input_text": "[1]", "expected_output": "1"},
            {"input_text": "[5, 4, -1, 7, 8]", "expected_output": "23"}
        ],
        "hidden_tests": [
            {"input_text": "[-1]", "expected_output": "-1"},
            {"input_text": "[-2, -1]", "expected_output": "-1"},
            {"input_text": "[-3, -2, -2, -3]", "expected_output": "-2"},
            {"input_text": "[1, 2, 3, 4, 5]", "expected_output": "15"}
        ],
        "hints": [
            {"level": 1, "text": "If a prefix sum becomes negative, would keeping it benefit the rest of the subarray?", "xp_cost": 2},
            {"level": 2, "text": "Kadane's algorithm: at each position, choose between extending the existing subarray or starting fresh.", "xp_cost": 5},
            {"level": 3, "text": "`current = max(x, current + x)` and `best = max(best, current)`.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Kadane's Algorithm\n\nAt each position $i$, decide whether to add `nums[i]` to the accumulated sum or start a new subarray at `nums[i]`.\n\n- Time Complexity: $O(n)$\n- Space Complexity: $O(1)$"
    },
    {
        "slug": "climbing-stairs",
        "title": "Climbing Stairs",
        "difficulty": "easy",
        "topic": "DP",
        "tags": ["Dynamic Programming", "Math", "Memoization"],
        "company_tags": ["Amazon", "Google", "Uber"],
        "statement_md": "You are climbing a staircase. It takes `n` steps to reach the top.\n\nEach time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {"input_text": "2", "expected_output": "2"},
            {"input_text": "3", "expected_output": "3"}
        ],
        "hidden_tests": [
            {"input_text": "1", "expected_output": "1"},
            {"input_text": "4", "expected_output": "5"},
            {"input_text": "5", "expected_output": "8"},
            {"input_text": "10", "expected_output": "89"},
            {"input_text": "20", "expected_output": "10946"}
        ],
        "hints": [
            {"level": 1, "text": "To reach step n, you could have come from step n-1 or n-2.", "xp_cost": 2},
            {"level": 2, "text": "This matches the Fibonacci recurrence: `ways(n) = ways(n-1) + ways(n-2)`.", "xp_cost": 5},
            {"level": 3, "text": "Store just the previous two values instead of an entire array for $O(1)$ space.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Dynamic Programming (Space Optimized)\n\nThe recurrence relation is $dp[i] = dp[i-1] + dp[i-2]$ with base cases $dp[1]=1, dp[2]=2$.\n\n- Time Complexity: $O(n)$\n- Space Complexity: $O(1)$"
    },
    {
        "slug": "number-of-islands",
        "title": "Number of Islands",
        "difficulty": "medium",
        "topic": "Graphs",
        "tags": ["Graph", "BFS", "DFS", "Union Find"],
        "company_tags": ["Amazon", "Google", "Bloomberg", "DoorDash"],
        "statement_md": "Given an `m x n` 2D binary grid `grid` which represents a map of `'1'`s (land) and `'0'`s (water), return the number of islands.\n\nAn island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.",
        "time_limit_ms": 1500,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "[[\"1\",\"1\",\"1\",\"1\",\"0\"],[\"1\",\"1\",\"0\",\"1\",\"0\"],[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"0\",\"0\",\"0\",\"0\",\"0\"]]",
                "expected_output": "1"
            },
            {
                "input_text": "[[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"0\",\"0\",\"1\",\"0\",\"0\"],[\"0\",\"0\",\"0\",\"1\",\"1\"]]",
                "expected_output": "3"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "[[\"1\"]]",
                "expected_output": "1"
            },
            {
                "input_text": "[[\"0\"]]",
                "expected_output": "0"
            },
            {
                "input_text": "[[\"1\",\"0\",\"1\"],[\"0\",\"1\",\"0\"],[\"1\",\"0\",\"1\"]]",
                "expected_output": "5"
            }
        ],
        "hints": [
            {"level": 1, "text": "Iterate over every cell. When you find an unvisited '1', trigger a graph search.", "xp_cost": 2},
            {"level": 2, "text": "Use BFS with a queue or DFS with recursion to visit all connected 4-directional cells.", "xp_cost": 5},
            {"level": 3, "text": "Mark visited cells in a set or mutate visited land to '0' to avoid cycles.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: BFS / DFS Traversal\n\nTraverse the matrix cell by cell. Whenever an unvisited `'1'` is spotted, increment island count and use Breadth-First Search (Queue) to sink or mark all connected land.\n\n- Time Complexity: $O(m \\times n)$\n- Space Complexity: $O(m \\times n)$"
    },
    {
        "slug": "merge-intervals",
        "title": "Merge Intervals",
        "difficulty": "medium",
        "topic": "Arrays",
        "tags": ["Array", "Sorting"],
        "company_tags": ["Google", "Facebook", "Microsoft"],
        "statement_md": "Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {"input_text": "[[1,3],[2,6],[8,10],[15,18]]", "expected_output": "[[1,6],[8,10],[15,18]]"},
            {"input_text": "[[1,4],[4,5]]", "expected_output": "[[1,5]]"}
        ],
        "hidden_tests": [
            {"input_text": "[[1,4],[2,3]]", "expected_output": "[[1,4]]"},
            {"input_text": "[[1,4]]", "expected_output": "[[1,4]]"},
            {"input_text": "[[1,4],[0,2],[3,5]]", "expected_output": "[[0,5]]"}
        ],
        "hints": [
            {"level": 1, "text": "Sorting the intervals by their start time makes overlap detection straightforward.", "xp_cost": 2},
            {"level": 2, "text": "After sorting, two intervals overlap if the start of the second is $\\le$ end of the first.", "xp_cost": 5},
            {"level": 3, "text": "Extend `out[-1][1] = max(out[-1][1], current_end)` when overlapping, otherwise append new interval.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Sort by Start\n\nSorting intervals guarantees that any interval that could overlap with previous ones will appear adjacent.\n\n- Time Complexity: $O(n \\log n)$\n- Space Complexity: $O(n)$"
    },
    {
        "slug": "longest-substring-without-repeating-characters",
        "title": "Longest Substring Without Repeating Characters",
        "difficulty": "medium",
        "topic": "Strings",
        "tags": ["Hash Table", "String", "Sliding Window"],
        "company_tags": ["Amazon", "Bloomberg", "Google"],
        "statement_md": "Given a string `s`, find the length of the longest substring without duplicate characters.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {"input_text": "\"abcabcbb\"", "expected_output": "3"},
            {"input_text": "\"bbbbb\"", "expected_output": "1"},
            {"input_text": "\"pwwkew\"", "expected_output": "3"}
        ],
        "hidden_tests": [
            {"input_text": "\"\"", "expected_output": "0"},
            {"input_text": "\" \"", "expected_output": "1"},
            {"input_text": "\"au\"", "expected_output": "2"},
            {"input_text": "\"dvdf\"", "expected_output": "3"}
        ],
        "hints": [
            {"level": 1, "text": "Use a sliding window `[left, right]` where characters within the window are all unique.", "xp_cost": 2},
            {"level": 2, "text": "Store the last seen index of each character in a hash map.", "xp_cost": 5},
            {"level": 3, "text": "When a repeat occurs, fast-forward `left` to `last[c] + 1` if it is greater than `left`.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Sliding Window with Hash Map\n\nMaintain window boundaries `[left, right]`. When encountering a previously seen character in the current window, move `left` pointer to avoid duplicates.\n\n- Time Complexity: $O(n)$\n- Space Complexity: $O(\\min(n, m))$ where $m$ is charset size"
    },
    {
        "slug": "coin-change",
        "title": "Coin Change",
        "difficulty": "medium",
        "topic": "DP",
        "tags": ["Array", "Dynamic Programming", "Breadth-First Search"],
        "company_tags": ["Amazon", "Google", "Goldman Sachs"],
        "statement_md": "You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.\n\nReturn the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.\n\nYou may assume that you have an infinite number of each kind of coin.",
        "time_limit_ms": 1500,
        "memory_limit_mb": 128,
        "sample_tests": [
            {"input_text": "[1, 2, 5]\n11", "expected_output": "3"},
            {"input_text": "[2]\n3", "expected_output": "-1"},
            {"input_text": "[1]\n0", "expected_output": "0"}
        ],
        "hidden_tests": [
            {"input_text": "[1, 3, 4]\n6", "expected_output": "2"},
            {"input_text": "[186, 419, 83, 408]\n6249", "expected_output": "20"},
            {"input_text": "[2, 5, 10, 1]\n27", "expected_output": "4"}
        ],
        "hints": [
            {"level": 1, "text": "Bottom-up Dynamic Programming: let `dp[i]` be minimum coins to make amount `i`.", "xp_cost": 2},
            {"level": 2, "text": "Initialize `dp` array with infinity, set `dp[0] = 0`.", "xp_cost": 5},
            {"level": 3, "text": "For each coin, update `dp[i] = min(dp[i], dp[i - coin] + 1)`. If `dp[amount] == inf` return -1.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Dynamic Programming\n\nBuild solutions iteratively from $1$ up to `amount`. For each sub-amount $a$, test each coin $c$.\n\n- Time Complexity: $O(\\text{amount} \\times \\text{len(coins)})$\n- Space Complexity: $O(\\text{amount})$"
    },
    {
        "slug": "binary-tree-inorder-traversal",
        "title": "Binary Tree Inorder Traversal",
        "difficulty": "easy",
        "topic": "Trees",
        "tags": ["Stack", "Tree", "Depth-First Search", "Binary Tree"],
        "company_tags": ["Amazon", "Microsoft", "Meta"],
        "statement_md": "Given the root of a binary tree, return the inorder traversal of its nodes' values.\n\nBinary tree input is represented as level-order serialization with `null` indicating empty branches.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {"input_text": "[1, null, 2, 3]", "expected_output": "[1, 3, 2]"},
            {"input_text": "[]", "expected_output": "[]"},
            {"input_text": "[1]", "expected_output": "[1]"}
        ],
        "hidden_tests": [
            {"input_text": "[1, 2, 3, 4, 5, null, 8, null, null, 6, 7, 9]", "expected_output": "[4, 2, 6, 5, 7, 1, 3, 9, 8]"},
            {"input_text": "[3, 1, 2]", "expected_output": "[1, 3, 2]"}
        ],
        "hints": [
            {"level": 1, "text": "Inorder traversal visits: Left subtree -> Current Node -> Right subtree.", "xp_cost": 2},
            {"level": 2, "text": "Can be done recursively, or iteratively using an explicit stack.", "xp_cost": 5},
            {"level": 3, "text": "Push all left nodes onto a stack until reaching null. Pop, visit, then pivot to `node.right`.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Iterative Stack\n\nTraverse leftwards continuously pushing nodes into stack. Once null is reached, pop the top node, append to result, and move right.\n\n- Time Complexity: $O(n)$\n- Space Complexity: $O(h)$ where $h$ is tree height"
    }
]

os.makedirs("content/problems", exist_ok=True)
for p in problems:
    filepath = os.path.join("content/problems", f"{p['slug']}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(p, f, indent=2)

print(f"Successfully generated {len(problems)} problem definitions in content/problems/")
