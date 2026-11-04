import os
import json

BATCH2 = [
    {
        "slug": "longest-repeating-character-replacement",
        "title": "Longest Repeating Character Replacement",
        "difficulty": "medium",
        "topic": "Strings",
        "tags": ["Hash Table", "String", "Sliding Window"],
        "company_tags": ["Amazon", "Google", "Meta", "Uber"],
        "statement_md": "You are given a string `s` and an integer `k`. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most `k` times.\n\nReturn the length of the longest substring containing the same letter you can get after performing the above operations.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "\"ABAB\"\n2",
                "expected_output": "4"
            },
            {
                "input_text": "\"AABABBA\"\n1",
                "expected_output": "4"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "\"AAAA\"\n2",
                "expected_output": "4"
            },
            {
                "input_text": "\"ABCDE\"\n1",
                "expected_output": "2"
            }
        ],
        "hints": [
            {"level": 1, "text": "Use a sliding window [l, r]. Window length is (r - l + 1).", "xp_cost": 2},
            {"level": 2, "text": "The number of replacements needed in the window is window_length - max_frequency.", "xp_cost": 5},
            {"level": 3, "text": "If (r - l + 1) - max_freq > k, shrink window from left.", "xp_cost": 10}
        ],
        "editorial_md": """### Sliding Window with Character Frequency

Maintain a counts map of characters in the window and track `max_freq`.
Condition for valid window: `(r - l + 1) - max_freq <= k`.
When invalid, decrement count of `s[l]` and increment `l`.

```python
def characterReplacement(s: str, k: int) -> int:
    counts = {}
    l = 0
    max_f = 0
    max_len = 0
    for r in range(len(s)):
        counts[s[r]] = counts.get(s[r], 0) + 1
        max_f = max(max_f, counts[s[r]])
        while (r - l + 1) - max_f > k:
            counts[s[l]] -= 1
            l += 1
        max_len = max(max_len, r - l + 1)
    return max_len
```

- **Time Complexity:** $O(n)$
- **Space Complexity:** $O(1)$ (26 letters)."""
    },
    {
        "slug": "sliding-window-maximum",
        "title": "Sliding Window Maximum",
        "difficulty": "hard",
        "topic": "Stack and Queue",
        "tags": ["Array", "Queue", "Sliding Window", "Monotonic Queue"],
        "company_tags": ["Amazon", "Google", "Citadel", "Meta"],
        "statement_md": "You are given an array of integers `nums`, there is a sliding window of size `k` which is moving from the very left of the array to the very right. You can only see the `k` numbers in the window. Each time the sliding window moves right by one position.\n\nReturn the max sliding window.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "[1, 3, -1, -3, 5, 3, 6, 7]\n3",
                "expected_output": "[3, 3, 5, 5, 6, 7]"
            },
            {
                "input_text": "[1]\n1",
                "expected_output": "[1]"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "[1, -1]\n1",
                "expected_output": "[1, -1]"
            },
            {
                "input_text": "[9, 11]\n2",
                "expected_output": "[11]"
            },
            {
                "input_text": "[4, -2]\n2",
                "expected_output": "[4]"
            }
        ],
        "hints": [
            {"level": 1, "text": "Maintain a monotonic decreasing queue storing indices.", "xp_cost": 2},
            {"level": 2, "text": "Remove elements smaller than current element from back of deque.", "xp_cost": 5},
            {"level": 3, "text": "Remove front elements that have fallen outside window (index <= i - k).", "xp_cost": 10}
        ],
        "editorial_md": """### Monotonic Deque

```python
from collections import deque

def maxSlidingWindow(nums: list[int], k: int) -> list[int]:
    q = deque()  # stores indices
    res = []
    for i, n in enumerate(nums):
        while q and nums[q[-1]] < n:
            q.pop()
        q.append(i)
        if q[0] <= i - k:
            q.popleft()
        if i >= k - 1:
            res.append(nums[q[0]])
    return res
```

- **Time Complexity:** $O(n)$
- **Space Complexity:** $O(k)$"""
    },
    {
        "slug": "evaluate-reverse-polish-notation",
        "title": "Evaluate Reverse Polish Notation",
        "difficulty": "medium",
        "topic": "Stack and Queue",
        "tags": ["Array", "Math", "Stack"],
        "company_tags": ["LinkedIn", "Amazon", "Microsoft"],
        "statement_md": "You are given an array of strings `tokens` that represents an arithmetic expression in a Reverse Polish Notation.\n\nEvaluate the expression. Return an integer that represents the value of the expression.\n\nNote that division between two integers always **truncates toward zero**.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "[\"2\", \"1\", \"+\", \"3\", \"*\"]",
                "expected_output": "9"
            },
            {
                "input_text": "[\"4\", \"13\", \"5\", \"/\", \"+\"]",
                "expected_output": "6"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "[\"10\", \"6\", \"9\", \"3\", \"+\", \"-11\", \"*\", \"/\", \"*\", \"17\", \"+\", \"5\", \"+\"]",
                "expected_output": "22"
            },
            {
                "input_text": "[\"3\"]",
                "expected_output": "3"
            }
        ],
        "hints": [
            {"level": 1, "text": "Use a stack. Push numbers onto the stack.", "xp_cost": 2},
            {"level": 2, "text": "When encountering an operator, pop two operands, apply operator, and push result back.", "xp_cost": 5},
            {"level": 3, "text": "Be careful with operand order for subtraction and division: b = pop(), a = pop(), calculate a op b.", "xp_cost": 10}
        ],
        "editorial_md": """### Stack Evaluation

```python
def evalRPN(tokens: list[str]) -> int:
    stack = []
    for token in tokens:
        if token in "+-*/":
            b = stack.pop()
            a = stack.pop()
            if token == '+': stack.append(a + b)
            elif token == '-': stack.append(a - b)
            elif token == '*': stack.append(a * b)
            elif token == '/': stack.append(int(a / b))
        else:
            stack.append(int(token))
    return stack[0]
```

- **Time Complexity:** $O(n)$
- **Space Complexity:** $O(n)$"""
    },
    {
        "slug": "generate-parentheses",
        "title": "Generate Parentheses",
        "difficulty": "medium",
        "topic": "Strings",
        "tags": ["String", "Dynamic Programming", "Backtracking"],
        "company_tags": ["Google", "Amazon", "Microsoft", "Meta"],
        "statement_md": "Given `n` pairs of parentheses, write a function to generate all combinations of well-formed parentheses.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "3",
                "expected_output": "[\"((()))\", \"(()())\", \"(())()\", \"()(())\", \"()()()\"]"
            },
            {
                "input_text": "1",
                "expected_output": "[\"()\"]"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "2",
                "expected_output": "[\"(())\", \"()()\"]"
            },
            {
                "input_text": "4",
                "expected_output": "[\"(((())))\", \"((()()))\", \"((())())\", \"((()))()\", \"(()(()))\", \"(()()())\", \"(()())()\", \"(())(())\", \"(())()()\", \"()((()))\", \"()(()())\", \"()(())()\", \"()()(())\", \"()()()()\"]"
            }
        ],
        "hints": [
            {"level": 1, "text": "Track open count and closed count.", "xp_cost": 2},
            {"level": 2, "text": "You can add '(' if open < n.", "xp_cost": 5},
            {"level": 3, "text": "You can add ')' if close < open.", "xp_cost": 10}
        ],
        "editorial_md": """### Backtracking Search

```python
def generateParenthesis(n: int) -> list[str]:
    res = []
    def backtrack(curr, open_c, close_c):
        if len(curr) == 2 * n:
            res.append(curr)
            return
        if open_c < n:
            backtrack(curr + '(', open_c + 1, close_c)
        if close_c < open_c:
            backtrack(curr + ')', open_c, close_c + 1)
    backtrack("", 0, 0)
    return res
```

- **Time Complexity:** $O(\\frac{4^n}{\\sqrt{n}})$ (Catalan number $C_n$).
- **Space Complexity:** $O(n)$ recursion depth."""
    },
    {
        "slug": "letter-combinations-of-a-phone-number",
        "title": "Letter Combinations of a Phone Number",
        "difficulty": "medium",
        "topic": "Strings",
        "tags": ["Hash Table", "String", "Backtracking"],
        "company_tags": ["Amazon", "Meta", "Google", "Microsoft"],
        "statement_md": "Given a string containing digits from `2-9` inclusive, return all possible letter combinations that the number could represent. Return the answer in **any order**.\n\nA mapping of digits to letters (just like on telephone buttons) is given:\n2: 'abc', 3: 'def', 4: 'ghi', 5: 'jkl', 6: 'mno', 7: 'pqrs', 8: 'tuv', 9: 'wxyz'.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "\"23\"",
                "expected_output": "[\"ad\", \"ae\", \"af\", \"bd\", \"be\", \"bf\", \"cd\", \"ce\", \"cf\"]"
            },
            {
                "input_text": "\"\"",
                "expected_output": "[]"
            },
            {
                "input_text": "\"2\"",
                "expected_output": "[\"a\", \"b\", \"c\"]"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "\"7\"",
                "expected_output": "[\"p\", \"q\", \"r\", \"s\"]"
            },
            {
                "input_text": "\"234\"",
                "expected_output": "[\"adg\", \"adh\", \"adi\", \"aeg\", \"aeh\", \"aei\", \"afg\", \"afh\", \"afi\", \"bdg\", \"bdh\", \"bdi\", \"beg\", \"beh\", \"bei\", \"bfg\", \"bfh\", \"bfi\", \"cdg\", \"cdh\", \"cdi\", \"ceg\", \"ceh\", \"cei\", \"cfg\", \"cfh\", \"cfi\"]"
            }
        ],
        "hints": [
            {"level": 1, "text": "Map digits to characters using a dictionary.", "xp_cost": 2},
            {"level": 2, "text": "Use depth-first search where each digit level branches out to its mapped characters.", "xp_cost": 5},
            {"level": 3, "text": "Base case: when current combination length equals digits length, add to results.", "xp_cost": 10}
        ],
        "editorial_md": """### Backtracking Search

```python
def letterCombinations(digits: str) -> list[str]:
    if not digits:
        return []
    mapping = {
        '2': "abc", '3': "def", '4': "ghi", '5': "jkl",
        '6': "mno", '7': "pqrs", '8': "tuv", '9': "wxyz"
    }
    res = []
    def backtrack(idx, current):
        if idx == len(digits):
            res.append(current)
            return
        for char in mapping[digits[idx]]:
            backtrack(idx + 1, current + char)
    backtrack(0, "")
    return res
```

- **Time Complexity:** $O(4^n)$
- **Space Complexity:** $O(n)$"""
    },
    {
        "slug": "maximum-product-subarray",
        "title": "Maximum Product Subarray",
        "difficulty": "medium",
        "topic": "Dynamic Programming",
        "tags": ["Array", "Dynamic Programming"],
        "company_tags": ["Amazon", "LinkedIn", "Google", "Microsoft"],
        "statement_md": "Given an integer array `nums`, find a subarray that has the largest product, and return the product.\n\nThe test cases are generated so that the answer will fit in a 32-bit integer.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "[2, 3, -2, 4]",
                "expected_output": "6"
            },
            {
                "input_text": "[-2, 0, -1]",
                "expected_output": "0"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "[-2, 3, -4]",
                "expected_output": "24"
            },
            {
                "input_text": "[0, 2]",
                "expected_output": "2"
            },
            {
                "input_text": "[-2]",
                "expected_output": "-2"
            }
        ],
        "hints": [
            {"level": 1, "text": "A negative number multiplied by a minimum (most negative) product becomes a maximum product.", "xp_cost": 2},
            {"level": 2, "text": "Keep track of both the maximum and minimum product ending at the current position.", "xp_cost": 5},
            {"level": 3, "text": "When current number is negative, swap max_prod and min_prod before updating.", "xp_cost": 10}
        ],
        "editorial_md": """### Dynamic Programming with Sign Flipping

```python
def maxProduct(nums: list[int]) -> int:
    res = nums[0]
    cur_min, cur_max = 1, 1
    for n in nums:
        vals = (n, n * cur_max, n * cur_min)
        cur_max = max(vals)
        cur_min = min(vals)
        res = max(res, cur_max)
    return res
```

- **Time Complexity:** $O(n)$
- **Space Complexity:** $O(1)$"""
    },
    {
        "slug": "edit-distance",
        "title": "Edit Distance",
        "difficulty": "hard",
        "topic": "Dynamic Programming",
        "tags": ["String", "Dynamic Programming"],
        "company_tags": ["Google", "Amazon", "Microsoft"],
        "statement_md": "Given two strings `word1` and `word2`, return the minimum number of operations required to convert `word1` to `word2`.\n\nYou have the following three operations permitted on a word:\n- Insert a character\n- Delete a character\n- Replace a character",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "\"horse\"\n\"ros\"",
                "expected_output": "3"
            },
            {
                "input_text": "\"intention\"\n\"execution\"",
                "expected_output": "5"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "\"\"\n\"a\"",
                "expected_output": "1"
            },
            {
                "input_text": "\"abc\"\n\"abc\"",
                "expected_output": "0"
            }
        ],
        "hints": [
            {"level": 1, "text": "Define dp[i][j] as minimum operations to convert word1[:i] to word2[:j].", "xp_cost": 2},
            {"level": 2, "text": "If word1[i-1] == word2[j-1], dp[i][j] = dp[i-1][j-1].", "xp_cost": 5},
            {"level": 3, "text": "Otherwise, dp[i][j] = 1 + min(insert: dp[i][j-1], delete: dp[i-1][j], replace: dp[i-1][j-1]).", "xp_cost": 10}
        ],
        "editorial_md": """### 2D Levenshtein Distance Dynamic Programming

```python
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
        
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]
```

- **Time Complexity:** $O(m \\times n)$
- **Space Complexity:** $O(m \\times n)$"""
    },
    {
        "slug": "coin-change-ii",
        "title": "Coin Change II",
        "difficulty": "medium",
        "topic": "Dynamic Programming",
        "tags": ["Array", "Dynamic Programming"],
        "company_tags": ["Amazon", "Google", "Bloomberg"],
        "statement_md": "You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.\n\nReturn the number of combinations that make up that amount. If that amount of money cannot be made up by any combination of the coins, return `0`.\n\nYou may assume that you have an infinite number of each kind of coin.",
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "sample_tests": [
            {
                "input_text": "5\n[1, 2, 5]",
                "expected_output": "4"
            },
            {
                "input_text": "3\n[2]",
                "expected_output": "0"
            },
            {
                "input_text": "10\n[10]",
                "expected_output": "1"
            }
        ],
        "hidden_tests": [
            {
                "input_text": "0\n[7]",
                "expected_output": "1"
            },
            {
                "input_text": "500\n[1, 2, 5]",
                "expected_output": "12701"
            }
        ],
        "hints": [
            {"level": 1, "text": "This is the unbounded knapsack counting combinations problem.", "xp_cost": 2},
            {"level": 2, "text": "Loop over coins in the outer loop to prevent permutation duplicates.", "xp_cost": 5},
            {"level": 3, "text": "For each coin, iterate x from coin to amount: dp[x] += dp[x - coin].", "xp_cost": 10}
        ],
        "editorial_md": """### Unbounded Knapsack Dynamic Programming

```python
def change(amount: int, coins: list[int]) -> int:
    dp = [0] * (amount + 1)
    dp[0] = 1
    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] += dp[x - coin]
    return dp[amount]
```

- **Time Complexity:** $O(N \\times amount)$
- **Space Complexity:** $O(amount)$"""
    }
]

def main():
    target_dir = os.path.join(os.path.dirname(__file__), "..", "..", "content", "problems")
    count = 0
    for p in BATCH2:
        fpath = os.path.join(target_dir, f"{p['slug']}.json")
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(p, f, indent=2)
        count += 1
    print(f"Generated {count} batch2 problems in {target_dir}")

if __name__ == "__main__":
    main()
