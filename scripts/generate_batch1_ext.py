"""
Problem Generator - Batch 1 Extension:
- Arrays and Hashing (5 more: 4 Medium, 1 Hard) -> Total Arrays = 10 (5 Easy, 4 Medium, 1 Hard)
- Two Pointers & Sliding Window (8 problems: 3 Easy, 4 Medium, 1 Hard)
"""
import os
import json

PROBLEMS = [
    # 6. Arrays & Hashing - Medium
    {
        "slug": "equal-parity-longest-subsegment",
        "title": "Longest Subsegment with Equal Parity Counts",
        "difficulty": "medium",
        "topic": "Arrays and Hashing",
        "tags": ["Array", "Hash Table", "Prefix Sum"],
        "company_tags": ["Google", "Uber", "Amazon"],
        "statement_md": "Given an array of integers `nums`, find the maximum length of a contiguous subarray that contains an equal number of even and odd integers.\n\n### Input Format\n- A JSON-encoded list of integers `nums`\n\n### Output Format\n- An integer representing the maximum length",
        "examples": [
            {
                "input": "[1, 2, 3, 4, 5, 6]",
                "output": "6",
                "explanation": "The entire array has 3 evens (2, 4, 6) and 3 odds (1, 3, 5)."
            },
            {
                "input": "[1, 3, 5, 2]",
                "output": "2",
                "explanation": "Subarrays [5, 2] or [3, 2] or [1, 2] of length 2 have 1 even and 1 odd."
            }
        ],
        "sample_tests": [
            {"input_text": "[1, 2, 3, 4, 5, 6]", "expected_output": "6"},
            {"input_text": "[1, 3, 5, 2]", "expected_output": "2"},
            {"input_text": "[2, 4, 6]", "expected_output": "0"}
        ],
        "hidden_tests": [
            {"input_text": "[]", "expected_output": "0"},
            {"input_text": "[1]", "expected_output": "0"},
            {"input_text": "[1, 2]", "expected_output": "2"},
            {"input_text": "[1, 1, 1, 2, 2, 2]", "expected_output": "6"},
            {"input_text": "[2, 2, 1, 1, 2, 2, 1, 1]", "expected_output": "8"},
            {"input_text": "[-1, -2, -3, -4]", "expected_output": "4"},
            {"input_text": "[0, 0, 0, 1, 1, 1]", "expected_output": "6"},
            {"input_text": "[1, 3, 5, 7, 9, 2, 4]", "expected_output": "4"},
            {"input_text": "[1, 2, 1, 2, 1, 2, 1, 2, 1]", "expected_output": "8"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Transform each odd number to +1 and each even number to -1.", "xp_cost": 2},
            {"level": 2, "text": "The problem reduces to finding the longest subarray whose sum is 0.", "xp_cost": 5},
            {"level": 3, "text": "Use a Hash Map to record the first occurrence of each running prefix sum.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Prefix Balance Map\n\nMap odd elements to +1 and even elements to -1. Calculate running prefix sum. Equal parity count corresponds to prefix sum having the same value at two different indices $i$ and $j$, meaning the subarray sum between them is 0.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ single pass.\n- **Space Complexity:** $O(n)$ hash table storage.\n\n#### Common Pitfalls\n- Not initializing the prefix map with `{0: -1}` for subarrays starting at index 0.",
        "reference_solutions": {
            "brute_python": "def findMaxLength(nums):\n    max_len = 0\n    for i in range(len(nums)):\n        even = odd = 0\n        for j in range(i, len(nums)):\n            if nums[j] % 2 == 0:\n                even += 1\n            else:\n                odd += 1\n            if even == odd:\n                max_len = max(max_len, j - i + 1)\n    return max_len",
            "optimal_python": "def findMaxLength(nums):\n    first_seen = {0: -1}\n    balance = 0\n    max_len = 0\n    for i, x in enumerate(nums):\n        balance += 1 if (x % 2 != 0) else -1\n        if balance in first_seen:\n            max_len = max(max_len, i - first_seen[balance])\n        else:\n            first_seen[balance] = i\n    return max_len",
            "optimal_java": "import java.util.*;\npublic class Solution {\n    public int findMaxLength(int[] nums) {\n        Map<Integer, Integer> map = new HashMap<>();\n        map.put(0, -1);\n        int balance = 0, maxLen = 0;\n        for (int i = 0; i < nums.length; i++) {\n            balance += (nums[i] % 2 != 0) ? 1 : -1;\n            if (map.containsKey(balance)) maxLen = Math.max(maxLen, i - map.get(balance));\n            else map.put(balance, i);\n        }\n        return maxLen;\n    }\n}",
            "optimal_cpp": "#include <vector>\n#include <unordered_map>\n#include <algorithm>\nusing namespace std;\nclass Solution {\npublic:\n    int findMaxLength(vector<int>& nums) {\n        unordered_map<int, int> seen;\n        seen[0] = -1;\n        int balance = 0, maxLen = 0;\n        for (int i = 0; i < (int)nums.size(); i++) {\n            balance += (nums[i] % 2 != 0) ? 1 : -1;\n            if (seen.count(balance)) maxLen = max(maxLen, i - seen[balance]);\n            else seen[balance] = i;\n        }\n        return maxLen;\n    }\n};"
        }
    },

    # 7. Arrays & Hashing - Medium
    {
        "slug": "continuous-subarray-sum-modulo-k",
        "title": "Subarray Sum Divisible by Modulo Factor",
        "difficulty": "medium",
        "topic": "Arrays and Hashing",
        "tags": ["Array", "Hash Table", "Prefix Sum", "Math"],
        "company_tags": ["Meta", "Amazon", "Microsoft"],
        "statement_md": "Given an integer array `nums` and an integer `k`, return `true` if `nums` has a good subarray of length at least 2, or `false` otherwise.\n\nA good subarray is defined as a contiguous subsegment whose element sum is a multiple of `k` (i.e. `sum % k == 0`).\n\n### Input Format\n- Line 1: A JSON-encoded list of integers `nums`\n- Line 2: An integer `k` (`k >= 1`)\n\n### Output Format\n- A boolean value (`true` or `false`)",
        "examples": [
            {
                "input": "[23, 2, 4, 6, 7]\n6",
                "output": "true",
                "explanation": "[2, 4] is a continuous subarray of size 2 whose sum is 6 (6 % 6 == 0)."
            },
            {
                "input": "[23, 2, 6, 4, 7]\n6",
                "output": "true",
                "explanation": "[23, 2, 6, 4, 7] has sum 42, which is a multiple of 6, length 5."
            }
        ],
        "sample_tests": [
            {"input_text": "[23, 2, 4, 6, 7]\n6", "expected_output": "true"},
            {"input_text": "[23, 2, 6, 4, 7]\n6", "expected_output": "true"},
            {"input_text": "[23, 2, 6, 4, 7]\n13", "expected_output": "false"}
        ],
        "hidden_tests": [
            {"input_text": "[0, 0]\n1", "expected_output": "true"},
            {"input_text": "[0]\n1", "expected_output": "false"},
            {"input_text": "[5, 0, 0, 0]\n3", "expected_output": "true"},
            {"input_text": "[1, 2, 3]\n5", "expected_output": "true"},
            {"input_text": "[1, 2, 3]\n7", "expected_output": "false"},
            {"input_text": "[7, 7]\n7", "expected_output": "true"},
            {"input_text": "[1, 0]\n2", "expected_output": "false"},
            {"input_text": "[23, 2, 4, 6, 6]\n7", "expected_output": "true"},
            {"input_text": "[100, 200, 300]\n150", "expected_output": "true"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "If sum(0..i) % k == sum(0..j) % k, then the sum of subarray between i and j is divisible by k.", "xp_cost": 2},
            {"level": 2, "text": "Ensure that the difference between indices (j - i) is at least 2.", "xp_cost": 5},
            {"level": 3, "text": "Use a Hash Map to store the earliest index where each remainder modulo k was encountered.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Prefix Modulo Hash Map\n\nBy modular arithmetic, if two prefix sums have identical remainder modulo $k$, the difference between them is a multiple of $k$. Maintain a map of `remainder -> first_index`. Check `i - first_index >= 2`.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ single pass.\n- **Space Complexity:** $O(\\min(n, k))$ hash map capacity.\n\n#### Common Pitfalls\n- Subarray length must be at least 2 (`i - map[rem] >= 2`).",
        "reference_solutions": {
            "brute_python": "def checkSubarraySum(nums, k):\n    n = len(nums)\n    for i in range(n):\n        cur = nums[i]\n        for j in range(i + 1, n):\n            cur += nums[j]\n            if cur % k == 0:\n                return True\n    return False",
            "optimal_python": "def checkSubarraySum(nums, k):\n    rem_map = {0: -1}\n    running_sum = 0\n    for i, x in enumerate(nums):\n        running_sum += x\n        rem = running_sum % k\n        if rem in rem_map:\n            if i - rem_map[rem] >= 2:\n                return True\n        else:\n            rem_map[rem] = i\n    return False",
            "optimal_java": "import java.util.*;\npublic class Solution {\n    public boolean checkSubarraySum(int[] nums, int k) {\n        Map<Integer, Integer> map = new HashMap<>();\n        map.put(0, -1);\n        int sum = 0;\n        for (int i = 0; i < nums.length; i++) {\n            sum += nums[i];\n            int rem = sum % k;\n            if (map.containsKey(rem)) {\n                if (i - map.get(rem) >= 2) return true;\n            } else {\n                map.put(rem, i);\n            }\n        }\n        return false;\n    }\n}",
            "optimal_cpp": "#include <vector>\n#include <unordered_map>\nusing namespace std;\nclass Solution {\npublic:\n    bool checkSubarraySum(vector<int>& nums, int k) {\n        unordered_map<int, int> remMap;\n        remMap[0] = -1;\n        int sum = 0;\n        for (int i = 0; i < (int)nums.size(); i++) {\n            sum += nums[i];\n            int rem = sum % k;\n            if (remMap.count(rem)) {\n                if (i - remMap[rem] >= 2) return true;\n            } else {\n                remMap[rem] = i;\n            }\n        }\n        return false;\n    }\n};"
        }
    },

    # 8. Arrays & Hashing - Medium
    {
        "slug": "sparse-vector-dot-product-stream",
        "title": "Sparse Vector Dot Product Pipeline",
        "difficulty": "medium",
        "topic": "Arrays and Hashing",
        "tags": ["Array", "Hash Table", "Design"],
        "company_tags": ["Meta", "ByteDance", "Google"],
        "statement_md": "Given two sparse vectors represented as arrays of integers `vec1` and `vec2` of the same length, compute their dot product efficiently without multiplying zeros.\n\nThe dot product is the sum of `vec1[i] * vec2[i]` for all `0 <= i < n`.\n\n### Input Format\n- Line 1: A JSON-encoded list of integers `vec1`\n- Line 2: A JSON-encoded list of integers `vec2`\n\n### Output Format\n- An integer representing the dot product",
        "examples": [
            {
                "input": "[1, 0, 0, 2, 3]\n[0, 3, 0, 4, 0]",
                "output": "8",
                "explanation": "Indices with non-zero products: index 3 -> 2 * 4 = 8. Total dot product = 8."
            },
            {
                "input": "[0, 1, 0, 0, 0]\n[0, 0, 0, 0, 0]",
                "output": "0",
                "explanation": "No common non-zero indices, dot product is 0."
            }
        ],
        "sample_tests": [
            {"input_text": "[1, 0, 0, 2, 3]\n[0, 3, 0, 4, 0]", "expected_output": "8"},
            {"input_text": "[0, 1, 0, 0, 0]\n[0, 0, 0, 0, 0]", "expected_output": "0"},
            {"input_text": "[0, 1, 0, 0, 2, 0, 0]\n[1, 0, 0, 0, 3, 0, 4]", "expected_output": "6"}
        ],
        "hidden_tests": [
            {"input_text": "[0]\n[0]", "expected_output": "0"},
            {"input_text": "[5]\n[4]", "expected_output": "20"},
            {"input_text": "[-1, 0, 2]\n[3, 0, -4]", "expected_output": "-11"},
            {"input_text": "[0, 0, 0, 10]\n[0, 0, 0, -5]", "expected_output": "-50"},
            {"input_text": "[1, 2, 3, 4]\n[5, 6, 7, 8]", "expected_output": "70"},
            {"input_text": "[0, 0, 100, 0, 0]\n[0, 0, 100, 0, 0]", "expected_output": "10000"},
            {"input_text": "[1, 0, -1]\n[-1, 0, 1]", "expected_output": "-2"},
            {"input_text": "[0, 0, 0, 0, 0]\n[1, 2, 3, 4, 5]", "expected_output": "0"},
            {"input_text": "[7, 0, 0, 0, 9]\n[0, 0, 0, 0, 3]", "expected_output": "27"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Store only non-zero values along with their indices.", "xp_cost": 2},
            {"level": 2, "text": "Iterate through the non-zero indices of the vector that has fewer non-zero entries.", "xp_cost": 5},
            {"level": 3, "text": "Use a Hash Map mapping index to value to achieve O(min(L1, L2)) lookups.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Index-Value Map\n\nStore non-zero entries as `{index: value}`. Iterate over the smaller map and lookup corresponding indices in the second map.\n\n#### Complexity\n- **Time Complexity:** $O(L)$ where $L$ is number of non-zero entries.\n- **Space Complexity:** $O(L)$ space for non-zero dictionary.\n\n#### Common Pitfalls\n- Multiplying vectors with negative entries correctly.",
        "reference_solutions": {
            "brute_python": "def dotProduct(vec1, vec2):\n    return sum(a * b for a, b in zip(vec1, vec2))",
            "optimal_python": "def dotProduct(vec1, vec2):\n    map1 = {i: v for i, v in enumerate(vec1) if v != 0}\n    map2 = {i: v for i, v in enumerate(vec2) if v != 0}\n    if len(map1) > len(map2):\n        map1, map2 = map2, map1\n    return sum(v * map2.get(i, 0) for i, v in map1.items())",
            "optimal_java": "import java.util.*;\npublic class Solution {\n    public int dotProduct(int[] vec1, int[] vec2) {\n        Map<Integer, Integer> map = new HashMap<>();\n        for (int i = 0; i < vec1.length; i++) if (vec1[i] != 0) map.put(i, vec1[i]);\n        int result = 0;\n        for (int i = 0; i < vec2.length; i++) {\n            if (vec2[i] != 0 && map.containsKey(i)) {\n                result += vec2[i] * map.get(i);\n            }\n        }\n        return result;\n    }\n}",
            "optimal_cpp": "#include <vector>\n#include <unordered_map>\nusing namespace std;\nclass Solution {\npublic:\n    int dotProduct(vector<int>& vec1, vector<int>& vec2) {\n        unordered_map<int, int> map;\n        for (int i = 0; i < (int)vec1.size(); i++) if (vec1[i] != 0) map[i] = vec1[i];\n        int result = 0;\n        for (int i = 0; i < (int)vec2.size(); i++) {\n            if (vec2[i] != 0 && map.count(i)) {\n                result += vec2[i] * map[i];\n            }\n        }\n        return result;\n    }\n};"
        }
    },

    # 9. Arrays & Hashing - Medium
    {
        "slug": "group-shifted-character-signatures",
        "title": "Group Shifted String Signatures",
        "difficulty": "medium",
        "topic": "Arrays and Hashing",
        "tags": ["Array", "Hash Table", "String"],
        "company_tags": ["Google", "Meta", "Amazon"],
        "statement_md": "Given an array of strings `strings`, group all strings that belong to the same shifting sequence.\n\nTwo strings `s` and `t` belong to the same shifting sequence if we can shift every character of `s` by the same distance modulo 26 to obtain `t` (e.g. `\"abc\"` -> `\"bcd\"` -> `\"xyz\"`).\n\nReturn the grouped strings sorted lexicographically within each group, and return the groups ordered by their first element.\n\n### Input Format\n- A JSON-encoded list of strings `strings`\n\n### Output Format\n- A JSON-encoded list of grouped string lists",
        "examples": [
            {
                "input": "[\"abc\", \"bcd\", \"acef\", \"xyz\", \"az\", \"ba\", \"a\", \"z\"]",
                "output": "[[\"a\", \"z\"], [\"abc\", \"bcd\", \"xyz\"], [\"acef\"], [\"az\", \"ba\"]]",
                "explanation": "\"abc\", \"bcd\", \"xyz\" all have consecutive +1 shifts. \"az\" and \"ba\" both wrap around with distance 25."
            },
            {
                "input": "[\"a\"]",
                "output": "[[\"a\"]]",
                "explanation": "A single character forms its own shift group."
            }
        ],
        "sample_tests": [
            {"input_text": "[\"abc\", \"bcd\", \"acef\", \"xyz\", \"az\", \"ba\", \"a\", \"z\"]", "expected_output": "[[\"a\", \"z\"], [\"abc\", \"bcd\", \"xyz\"], [\"acef\"], [\"az\", \"ba\"]]"},
            {"input_text": "[\"a\"]", "expected_output": "[[\"a\"]]"},
            {"input_text": "[\"ab\", \"cd\", \"ef\"]", "expected_output": "[[\"ab\", \"cd\", \"ef\"]]"}
        ],
        "hidden_tests": [
            {"input_text": "[]", "expected_output": "[]"},
            {"input_text": "[\"z\", \"a\"]", "expected_output": "[[\"a\", \"z\"]]"},
            {"input_text": "[\"ab\", \"ba\"]", "expected_output": "[[\"ab\"], [\"ba\"]]"},
            {"input_text": "[\"eqdf\", \"qcpr\"]", "expected_output": "[[\"eqdf\", \"qcpr\"]]"},
            {"input_text": "[\"ay\", \"bz\"]", "expected_output": "[[\"ay\", \"bz\"]]"},
            {"input_text": "[\"hello\", \"world\"]", "expected_output": "[[\"hello\"], [\"world\"]]"},
            {"input_text": "[\"mno\", \"pqr\", \"stu\"]", "expected_output": "[[\"mno\", \"pqr\", \"stu\"]]"},
            {"input_text": "[\"aaa\", \"bbb\", \"zzz\"]", "expected_output": "[[\"aaa\", \"bbb\", \"zzz\"]]"},
            {"input_text": "[\"za\", \"ab\"]", "expected_output": "[[\"ab\", \"za\"]]"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Notice that the difference between adjacent characters modulo 26 is identical for all strings in the same shift group.", "xp_cost": 2},
            {"level": 2, "text": "Compute a canonical key tuple: ( (ord(s[i]) - ord(s[i-1])) % 26 for i in 1..len(s) ).", "xp_cost": 5},
            {"level": 3, "text": "Use a Hash Map with this canonical difference tuple as key to cluster strings.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Normalized Difference Signature\n\nFor each string, compute the sequence of differences between consecutive characters modulo 26: `(ord(s[i]) - ord(s[i-1])) % 26`. Use this tuple as the hash map key.\n\n#### Complexity\n- **Time Complexity:** $O(N \\cdot L)$ where $N$ is word count and $L$ is string length.\n- **Space Complexity:** $O(N \\cdot L)$ hash table storage.\n\n#### Common Pitfalls\n- Handling negative differences with Python's `% 26` vs C++/Java where `(diff % 26 + 26) % 26` is needed.",
        "reference_solutions": {
            "brute_python": "def groupShiftedStrings(strings):\n    def is_shift(s1, s2):\n        if len(s1) != len(s2):\n            return False\n        shift = (ord(s2[0]) - ord(s1[0])) % 26\n        return all((ord(s2[i]) - ord(s1[i])) % 26 == shift for i in range(len(s1)))\n    groups = []\n    for s in sorted(strings):\n        placed = False\n        for g in groups:\n            if is_shift(g[0], s):\n                g.append(s)\n                placed = True\n                break\n        if not placed:\n            groups.append([s])\n    for g in groups: g.sort()\n    groups.sort(key=lambda x: x[0])\n    return groups",
            "optimal_python": "def groupShiftedStrings(strings):\n    from collections import defaultdict\n    groups = defaultdict(list)\n    for s in strings:\n        key = tuple((ord(s[i]) - ord(s[i-1])) % 26 for i in range(1, len(s)))\n        groups[key].append(s)\n    res = [sorted(v) for v in groups.values()]\n    res.sort(key=lambda x: x[0])\n    return res",
            "optimal_java": "import java.util.*;\npublic class Solution {\n    public List<List<String>> groupShiftedStrings(String[] strings) {\n        Map<String, List<String>> map = new HashMap<>();\n        for (String s : strings) {\n            StringBuilder sb = new StringBuilder();\n            for (int i = 1; i < s.length(); i++) {\n                int diff = (s.charAt(i) - s.charAt(i - 1) + 26) % 26;\n                sb.append(diff).append(\",\");\n            }\n            String key = sb.toString();\n            map.computeIfAbsent(key, k -> new ArrayList<>()).add(s);\n        }\n        List<List<String>> res = new ArrayList<>();\n        for (List<String> list : map.values()) {\n            Collections.sort(list);\n            res.add(list);\n        }\n        res.sort(Comparator.comparing(a -> a.get(0)));\n        return res;\n    }\n}",
            "optimal_cpp": "#include <vector>\n#include <string>\n#include <unordered_map>\n#include <algorithm>\nusing namespace std;\nclass Solution {\npublic:\n    vector<vector<string>> groupShiftedStrings(vector<string>& strings) {\n        unordered_map<string, vector<string>> groups;\n        for (auto& s : strings) {\n            string key = \"\";\n            for (int i = 1; i < (int)s.size(); i++) {\n                int diff = (s[i] - s[i-1] + 26) % 26;\n                key += to_string(diff) + \",\";\n            }\n            groups[key].push_back(s);\n        }\n        vector<vector<string>> res;\n        for (auto& p : groups) {\n            sort(p.second.begin(), p.second.end());\n            res.push_back(p.second);\n        }\n        sort(res.begin(), res.end(), [](const vector<string>& a, const vector<string>& b) {\n            return a[0] < b[0];\n        });\n        return res;\n    }\n};"
        }
    },

    # 10. Arrays & Hashing - Hard
    {
        "slug": "longest-consecutive-sequence-tracker",
        "title": "Longest Consecutive Sequence Discovery",
        "difficulty": "hard",
        "topic": "Arrays and Hashing",
        "tags": ["Array", "Hash Table", "Union Find"],
        "company_tags": ["Google", "Amazon", "Microsoft", "Spotify"],
        "statement_md": "Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence.\n\nYou must write an algorithm that runs in `O(n)` time.\n\n### Input Format\n- A JSON-encoded list of integers `nums`\n\n### Output Format\n- An integer representing the length of the longest consecutive sequence",
        "examples": [
            {
                "input": "[100, 4, 200, 1, 3, 2]",
                "output": "4",
                "explanation": "The longest consecutive elements sequence is [1, 2, 3, 4]. Therefore its length is 4."
            },
            {
                "input": "[0, 3, 7, 2, 5, 8, 4, 6, 0, 1]",
                "output": "9",
                "explanation": "The sequence is [0, 1, 2, 3, 4, 5, 6, 7, 8]. Length is 9."
            }
        ],
        "sample_tests": [
            {"input_text": "[100, 4, 200, 1, 3, 2]", "expected_output": "4"},
            {"input_text": "[0, 3, 7, 2, 5, 8, 4, 6, 0, 1]", "expected_output": "9"},
            {"input_text": "[10, 20, 30]", "expected_output": "1"}
        ],
        "hidden_tests": [
            {"input_text": "[]", "expected_output": "0"},
            {"input_text": "[1]", "expected_output": "1"},
            {"input_text": "[1, 2, 0, 1]", "expected_output": "3"},
            {"input_text": "[-5, -4, -3, -2, -1, 0]", "expected_output": "6"},
            {"input_text": "[-10, 10, -9, 9, -8, 8]", "expected_output": "3"},
            {"input_text": "[9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6]", "expected_output": "7"},
            {"input_text": "[100, 4, 200, 1, 3, 2, 5]", "expected_output": "5"},
            {"input_text": "[5, 5, 5, 5]", "expected_output": "1"},
            {"input_text": "[1000000, 1000001, 1000002]", "expected_output": "3"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Notice that an element x can only be the start of a consecutive streak if x - 1 does not exist in the collection.", "xp_cost": 2},
            {"level": 2, "text": "Only expand streaks starting from numbers where x - 1 is absent.", "xp_cost": 5},
            {"level": 3, "text": "Use a Hash Set for O(1) membership lookups to ensure each number is visited at most twice.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Hash Set Boundary Scan\n\nStore all elements in a hash set. Iterate through each number `x`. If `x - 1` is not in the set, `x` is the beginning of a sequence. Count upwards (`x + 1`, `x + 2`, ...) until reaching an absent number.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ because each element is visited at most twice (once in the outer loop, and once during sequence extension).\n- **Space Complexity:** $O(n)$ hash set storage.\n\n#### Common Pitfalls\n- Starting expansion from every number instead of only sequence starters `x - 1 not in set` (leads to $O(n^2)$ worst case).",
        "reference_solutions": {
            "brute_python": "def longestConsecutive(nums):\n    if not nums: return 0\n    nums = sorted(list(set(nums)))\n    longest = cur = 1\n    for i in range(1, len(nums)):\n        if nums[i] == nums[i-1] + 1:\n            cur += 1\n            longest = max(longest, cur)\n        else:\n            cur = 1\n    return longest",
            "optimal_python": "def longestConsecutive(nums):\n    num_set = set(nums)\n    longest = 0\n    for x in num_set:\n        if (x - 1) not in num_set:\n            cur = x\n            streak = 1\n            while (cur + 1) in num_set:\n                cur += 1\n                streak += 1\n            longest = max(longest, streak)\n    return longest",
            "optimal_java": "import java.util.*;\npublic class Solution {\n    public int longestConsecutive(int[] nums) {\n        Set<Integer> set = new HashSet<>();\n        for (int x : nums) set.add(x);\n        int longest = 0;\n        for (int x : set) {\n            if (!set.contains(x - 1)) {\n                int cur = x;\n                int streak = 1;\n                while (set.contains(cur + 1)) {\n                    cur++;\n                    streak++;\n                }\n                longest = Math.max(longest, streak);\n            }\n        }\n        return longest;\n    }\n}",
            "optimal_cpp": "#include <vector>\n#include <unordered_set>\n#include <algorithm>\nusing namespace std;\nclass Solution {\npublic:\n    int longestConsecutive(vector<int>& nums) {\n        unordered_set<int> s(nums.begin(), nums.end());\n        int longest = 0;\n        for (int x : s) {\n            if (!s.count(x - 1)) {\n                int cur = x;\n                int streak = 1;\n                while (s.count(cur + 1)) {\n                    cur++;\n                    streak++;\n                }\n                longest = max(longest, streak);\n            }\n        }\n        return longest;\n    }\n};"
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
    print(f"Batch 1 Ext generated {count} problems.")

if __name__ == "__main__":
    main()
