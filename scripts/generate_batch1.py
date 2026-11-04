"""
Problem Generator - Batch 1: Arrays & Hashing (10 problems) + Two Pointers & Sliding Window (part 1: 5 problems)
"""
import os
import json

PROBLEMS = [
    # 1. Arrays & Hashing - Easy
    {
        "slug": "pair-target-difference",
        "title": "Pair with Exact Target Difference",
        "difficulty": "easy",
        "topic": "Arrays and Hashing",
        "tags": ["Array", "Hash Table", "Two Pointers"],
        "company_tags": ["Google", "Amazon", "Meta"],
        "statement_md": "You are given an array of integers `nums` and an integer `k`. Your task is to determine whether there exists any pair of distinct indices `i` and `j` such that `|nums[i] - nums[j]| == k`.\n\nReturn `true` if such a pair exists, or `false` otherwise.\n\n### Input Format\n- Line 1: A JSON-encoded list of integers `nums`\n- Line 2: An integer `k` (where `k >= 0`)\n\n### Output Format\n- A boolean value (`true` or `false`)",
        "examples": [
            {
                "input": "[1, 5, 3, 4, 2]\n2",
                "output": "true",
                "explanation": "The pair (5, 3) has difference |5 - 3| = 2. Also (1, 3), (3, 1), etc."
            },
            {
                "input": "[8, 12, 16]\n10",
                "output": "false",
                "explanation": "No pair in the array has an absolute difference equal to 10."
            }
        ],
        "sample_tests": [
            {"input_text": "[1, 5, 3, 4, 2]\n2", "expected_output": "true"},
            {"input_text": "[8, 12, 16]\n10", "expected_output": "false"},
            {"input_text": "[1, 1, 1]\n0", "expected_output": "true"}
        ],
        "hidden_tests": [
            {"input_text": "[]\n5", "expected_output": "false"},
            {"input_text": "[42]\n0", "expected_output": "false"},
            {"input_text": "[42, 42]\n0", "expected_output": "true"},
            {"input_text": "[-5, -2, 3, 8]\n5", "expected_output": "true"},
            {"input_text": "[-10, -20, -30]\n15", "expected_output": "false"},
            {"input_text": "[100, 200, 300, 400, 500]\n100", "expected_output": "true"},
            {"input_text": "[1, 2, 4, 8, 16, 32]\n7", "expected_output": "true"},
            {"input_text": "[0, 0]\n1", "expected_output": "false"},
            {"input_text": "[-1000000, 1000000]\n2000000", "expected_output": "true"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Consider rewriting the condition: for each number x, does either x + k or x - k exist in the collection?", "xp_cost": 2},
            {"level": 2, "text": "If k is 0, we require at least one element that occurs two or more times.", "xp_cost": 5},
            {"level": 3, "text": "Use a Hash Map or Frequency Counter to store counts of elements and check complements in constant time.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Frequency Map / Hash Set\n\nWe iterate through the array while maintaining a count of observed elements. When `k == 0`, we simply need any number with frequency at least 2. When `k > 0`, for each element `x`, we check if `x - k` or `x + k` was already seen.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ single pass over array.\n- **Space Complexity:** $O(n)$ to store elements in hash table.\n\n#### Common Pitfalls\n- Forgetting that `k == 0` requires distinct indices $i \\neq j$ (i.e. at least two occurrences of the same value).",
        "reference_solutions": {
            "brute_python": "def findPairDifference(nums, k):\n    n = len(nums)\n    for i in range(n):\n        for j in range(i + 1, n):\n            if abs(nums[i] - nums[j]) == k:\n                return True\n    return False",
            "optimal_python": "def findPairDifference(nums, k):\n    if len(nums) < 2:\n        return False\n    counts = {}\n    for x in nums:\n        counts[x] = counts.get(x, 0) + 1\n    if k == 0:\n        return any(v >= 2 for v in counts.values())\n    for x in counts:\n        if (x + k) in counts:\n            return True\n    return False",
            "optimal_java": "import java.util.*;\npublic class Solution {\n    public boolean findPairDifference(int[] nums, int k) {\n        if (nums.length < 2) return false;\n        Map<Integer, Integer> counts = new HashMap<>();\n        for (int x : nums) counts.put(x, counts.getOrDefault(x, 0) + 1);\n        if (k == 0) {\n            for (int c : counts.values()) if (c >= 2) return true;\n            return false;\n        }\n        for (int x : counts.keySet()) if (counts.containsKey(x + k)) return true;\n        return false;\n    }\n}",
            "optimal_cpp": "#include <vector>\n#include <unordered_map>\nusing namespace std;\nclass Solution {\npublic:\n    bool findPairDifference(vector<int>& nums, int k) {\n        if (nums.size() < 2) return false;\n        unordered_map<int, int> counts;\n        for (int x : nums) counts[x]++;\n        if (k == 0) {\n            for (auto& p : counts) if (p.second >= 2) return true;\n            return false;\n        }\n        for (auto& p : counts) if (counts.count(p.first + k)) return true;\n        return false;\n    }\n};"
        }
    },

    # 2. Arrays & Hashing - Easy
    {
        "slug": "unique-element-frequency-sum",
        "title": "Sum of Unique Frequency Elements",
        "difficulty": "easy",
        "topic": "Arrays and Hashing",
        "tags": ["Array", "Hash Table", "Counting"],
        "company_tags": ["Amazon", "Apple", "Microsoft"],
        "statement_md": "Given an integer array `nums`, compute the sum of all elements that appear exactly once in the array.\n\nIf no element appears exactly once, return `0`.\n\n### Input Format\n- A JSON-encoded list of integers `nums`\n\n### Output Format\n- An integer representing the total sum of unique elements",
        "examples": [
            {
                "input": "[1, 2, 3, 2]",
                "output": "4",
                "explanation": "Elements 1 and 3 appear once (1 + 3 = 4). Element 2 appears twice."
            },
            {
                "input": "[1, 1, 1, 1]",
                "output": "0",
                "explanation": "All elements are duplicates, sum is 0."
            }
        ],
        "sample_tests": [
            {"input_text": "[1, 2, 3, 2]", "expected_output": "4"},
            {"input_text": "[1, 1, 1, 1]", "expected_output": "0"},
            {"input_text": "[1, 2, 3, 4, 5]", "expected_output": "15"}
        ],
        "hidden_tests": [
            {"input_text": "[]", "expected_output": "0"},
            {"input_text": "[10]", "expected_output": "10"},
            {"input_text": "[-5, -5, -2, 3, 3]", "expected_output": "-2"},
            {"input_text": "[-10, 10, -10, 10]", "expected_output": "0"},
            {"input_text": "[0, 0, 0, 7]", "expected_output": "7"},
            {"input_text": "[100, 200, 300, 200, 100]", "expected_output": "300"},
            {"input_text": "[-1, -2, -3, -4]", "expected_output": "-10"},
            {"input_text": "[9, 9, 8, 8, 7, 7, 6]", "expected_output": "6"},
            {"input_text": "[5, 5, 5, 5, 5, 5]", "expected_output": "0"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Count the frequency of each number in the array first.", "xp_cost": 2},
            {"level": 2, "text": "Iterate over the frequency table and sum keys with frequency equal to 1.", "xp_cost": 5},
            {"level": 3, "text": "Use a Hash Map or Frequency Dictionary to tally frequencies in O(n) time.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Frequency Map Tally\n\nCompute element frequencies using a hash map. Filter keys where frequency equals 1 and sum them.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ to build frequency map and sum keys.\n- **Space Complexity:** $O(n)$ auxiliary hash map storage.\n\n#### Common Pitfalls\n- Handling negative numbers properly when summing.",
        "reference_solutions": {
            "brute_python": "def sumOfUnique(nums):\n    return sum(x for x in nums if nums.count(x) == 1)",
            "optimal_python": "def sumOfUnique(nums):\n    counts = {}\n    for x in nums:\n        counts[x] = counts.get(x, 0) + 1\n    return sum(x for x, c in counts.items() if c == 1)",
            "optimal_java": "import java.util.*;\npublic class Solution {\n    public int sumOfUnique(int[] nums) {\n        Map<Integer, Integer> counts = new HashMap<>();\n        for (int x : nums) counts.put(x, counts.getOrDefault(x, 0) + 1);\n        int sum = 0;\n        for (Map.Entry<Integer, Integer> entry : counts.entrySet()) {\n            if (entry.getValue() == 1) sum += entry.getKey();\n        }\n        return sum;\n    }\n}",
            "optimal_cpp": "#include <vector>\n#include <unordered_map>\nusing namespace std;\nclass Solution {\npublic:\n    int sumOfUnique(vector<int>& nums) {\n        unordered_map<int, int> counts;\n        for (int x : nums) counts[x]++;\n        int sum = 0;\n        for (auto& p : counts) {\n            if (p.second == 1) sum += p.first;\n        }\n        return sum;\n    }\n};"
        }
    },

    # 3. Arrays & Hashing - Easy
    {
        "slug": "dominant-majority-threshold",
        "title": "Dominant Majority Threshold Element",
        "difficulty": "easy",
        "topic": "Arrays and Hashing",
        "tags": ["Array", "Hash Table", "Boyer-Moore"],
        "company_tags": ["Google", "Microsoft", "Bloomberg"],
        "statement_md": "Given an integer array `nums` of size `n`, find the dominant majority element that appears strictly more than `floor(n / 2)` times.\n\nYou may assume that the majority element always exists in the given input array.\n\n### Input Format\n- A JSON-encoded list of integers `nums`\n\n### Output Format\n- An integer value representing the dominant element",
        "examples": [
            {
                "input": "[3, 2, 3]",
                "output": "3",
                "explanation": "Size is 3, floor(3/2) = 1. Element 3 appears 2 times (> 1)."
            },
            {
                "input": "[2, 2, 1, 1, 1, 2, 2]",
                "output": "2",
                "explanation": "Size is 7, floor(7/2) = 3. Element 2 appears 4 times (> 3)."
            }
        ],
        "sample_tests": [
            {"input_text": "[3, 2, 3]", "expected_output": "3"},
            {"input_text": "[2, 2, 1, 1, 1, 2, 2]", "expected_output": "2"},
            {"input_text": "[1]", "expected_output": "1"}
        ],
        "hidden_tests": [
            {"input_text": "[5, 5, 5, 2, 2]", "expected_output": "5"},
            {"input_text": "[-1, -1, -1, 2, 3, -1, -1]", "expected_output": "-1"},
            {"input_text": "[0, 1, 0]", "expected_output": "0"},
            {"input_text": "[100, 100, 200]", "expected_output": "100"},
            {"input_text": "[6, 6, 6, 6, 1, 2, 3]", "expected_output": "6"},
            {"input_text": "[-4, -4, -4, -4, 0]", "expected_output": "-4"},
            {"input_text": "[8, 8, 8, 8, 8]", "expected_output": "8"},
            {"input_text": "[7, 3, 7, 3, 7]", "expected_output": "7"},
            {"input_text": "[999999, 999999, 1, 999999]", "expected_output": "999999"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Can you track a candidate and cancel out different elements when encountered?", "xp_cost": 2},
            {"level": 2, "text": "If a majority element appears more than n/2 times, its count remains positive even after cancelling all other elements.", "xp_cost": 5},
            {"level": 3, "text": "Use the Boyer-Moore Voting Algorithm to maintain a candidate and count in O(1) space.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Boyer-Moore Voting Algorithm\n\nMaintain `candidate` and `count`. For each element, if count is 0, pick the current element as candidate. If `x == candidate`, increment count; otherwise decrement count.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ single pass.\n- **Space Complexity:** $O(1)$ constant auxiliary memory.\n\n#### Common Pitfalls\n- Resetting candidate when count drops to zero.",
        "reference_solutions": {
            "brute_python": "def dominantElement(nums):\n    n = len(nums)\n    for x in nums:\n        if nums.count(x) > n // 2:\n            return x\n    return nums[0]",
            "optimal_python": "def dominantElement(nums):\n    candidate = None\n    count = 0\n    for x in nums:\n        if count == 0:\n            candidate = x\n            count = 1\n        elif x == candidate:\n            count += 1\n        else:\n            count -= 1\n    return candidate",
            "optimal_java": "public class Solution {\n    public int dominantElement(int[] nums) {\n        int candidate = nums[0];\n        int count = 0;\n        for (int x : nums) {\n            if (count == 0) {\n                candidate = x;\n                count = 1;\n            } else if (x == candidate) {\n                count++;\n            } else {\n                count--;\n            }\n        }\n        return candidate;\n    }\n}",
            "optimal_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int dominantElement(vector<int>& nums) {\n        int candidate = nums[0];\n        int count = 0;\n        for (int x : nums) {\n            if (count == 0) {\n                candidate = x;\n                count = 1;\n            } else if (x == candidate) {\n                count++;\n            } else {\n                count--;\n            }\n        }\n        return candidate;\n    }\n};"
        }
    },

    # 4. Arrays & Hashing - Easy
    {
        "slug": "equilibrium-pivot-index",
        "title": "Equilibrium Pivot Balance Index",
        "difficulty": "easy",
        "topic": "Arrays and Hashing",
        "tags": ["Array", "Prefix Sum"],
        "company_tags": ["Adobe", "Amazon", "Cisco"],
        "statement_md": "Given an array of integers `nums`, calculate the pivot index of this array.\n\nThe pivot index is the index where the sum of all the numbers strictly to the left of the index is equal to the sum of all the numbers strictly to the index's right.\n\nIf the index is on the left edge of the array, then the left sum is `0` because there are no elements to the left. This also applies to the right edge of the array.\n\nReturn the leftmost pivot index. If no such index exists, return `-1`.\n\n### Input Format\n- A JSON-encoded list of integers `nums`\n\n### Output Format\n- An integer index",
        "examples": [
            {
                "input": "[1, 7, 3, 6, 5, 6]",
                "output": "3",
                "explanation": "Left sum = nums[0] + nums[1] + nums[2] = 1 + 7 + 3 = 11. Right sum = nums[4] + nums[5] = 5 + 6 = 11."
            },
            {
                "input": "[1, 2, 3]",
                "output": "-1",
                "explanation": "There is no index that satisfies the equilibrium condition."
            }
        ],
        "sample_tests": [
            {"input_text": "[1, 7, 3, 6, 5, 6]", "expected_output": "3"},
            {"input_text": "[1, 2, 3]", "expected_output": "-1"},
            {"input_text": "[2, 1, -1]", "expected_output": "0"}
        ],
        "hidden_tests": [
            {"input_text": "[]", "expected_output": "-1"},
            {"input_text": "[5]", "expected_output": "0"},
            {"input_text": "[0, 0, 0, 0]", "expected_output": "0"},
            {"input_text": "[-1, -1, -1, -1, -1, 0]", "expected_output": "2"},
            {"input_text": "[-1, -1, 0, 1, 1, 0]", "expected_output": "5"},
            {"input_text": "[10, -10, 5, -5, 3]", "expected_output": "4"},
            {"input_text": "[2, 3, 5, 5]", "expected_output": "2"},
            {"input_text": "[1, -1, 1, -1, 1]", "expected_output": "0"},
            {"input_text": "[100, 200, 300]", "expected_output": "-1"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Notice that right_sum can be derived as total_sum - left_sum - current_value.", "xp_cost": 2},
            {"level": 2, "text": "Precompute the total sum of the array in a first pass.", "xp_cost": 5},
            {"level": 3, "text": "Use Prefix Sum tracking left_sum incrementally during a second pass.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Prefix Sum Accumulator\n\nCompute `total = sum(nums)`. Then iterate with `left_sum = 0`. For index `i`, right sum is `total - left_sum - nums[i]`. If `left_sum == right_sum`, return `i`. Otherwise `left_sum += nums[i]`.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ two passes.\n- **Space Complexity:** $O(1)$ constant extra space.\n\n#### Common Pitfalls\n- Forgetting that left_sum is 0 at index 0 and right_sum is 0 at index n - 1.",
        "reference_solutions": {
            "brute_python": "def pivotIndex(nums):\n    for i in range(len(nums)):\n        if sum(nums[:i]) == sum(nums[i+1:]):\n            return i\n    return -1",
            "optimal_python": "def pivotIndex(nums):\n    total = sum(nums)\n    left_sum = 0\n    for i, x in enumerate(nums):\n        if left_sum == total - left_sum - x:\n            return i\n        left_sum += x\n    return -1",
            "optimal_java": "public class Solution {\n    public int pivotIndex(int[] nums) {\n        int total = 0;\n        for (int x : nums) total += x;\n        int leftSum = 0;\n        for (int i = 0; i < nums.length; i++) {\n            if (leftSum == total - leftSum - nums[i]) return i;\n            leftSum += nums[i];\n        }\n        return -1;\n    }\n}",
            "optimal_cpp": "#include <vector>\n#include <numeric>\nusing namespace std;\nclass Solution {\npublic:\n    int pivotIndex(vector<int>& nums) {\n        long long total = 0;\n        for (int x : nums) total += x;\n        long long leftSum = 0;\n        for (int i = 0; i < (int)nums.size(); i++) {\n            if (leftSum == total - leftSum - nums[i]) return i;\n            leftSum += nums[i];\n        }\n        return -1;\n    }\n};"
        }
    },

    # 5. Arrays & Hashing - Easy
    {
        "slug": "missing-stream-identifier",
        "title": "Missing Stream Identifier in Consecutive Range",
        "difficulty": "easy",
        "topic": "Arrays and Hashing",
        "tags": ["Array", "Math", "Bit Manipulation"],
        "company_tags": ["Amazon", "Microsoft", "Oracle"],
        "statement_md": "Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return the only number in the range that is missing from the array.\n\n### Input Format\n- A JSON-encoded list of integers `nums`\n\n### Output Format\n- An integer representing the missing number",
        "examples": [
            {
                "input": "[3, 0, 1]",
                "output": "2",
                "explanation": "n = 3 since there are 3 numbers, so all numbers are in the range [0, 3]. 2 is the missing number."
            },
            {
                "input": "[0, 1]",
                "output": "2",
                "explanation": "n = 2, range is [0, 2]. 2 is the missing number."
            }
        ],
        "sample_tests": [
            {"input_text": "[3, 0, 1]", "expected_output": "2"},
            {"input_text": "[0, 1]", "expected_output": "2"},
            {"input_text": "[9, 6, 4, 2, 3, 5, 7, 0, 1]", "expected_output": "8"}
        ],
        "hidden_tests": [
            {"input_text": "[0]", "expected_output": "1"},
            {"input_text": "[1]", "expected_output": "0"},
            {"input_text": "[1, 2]", "expected_output": "0"},
            {"input_text": "[0, 2]", "expected_output": "1"},
            {"input_text": "[4, 3, 2, 1]", "expected_output": "0"},
            {"input_text": "[0, 1, 2, 3, 4, 6]", "expected_output": "5"},
            {"input_text": "[5, 4, 3, 2, 1, 0]", "expected_output": "6"},
            {"input_text": "[2, 3, 4, 5, 0]", "expected_output": "1"},
            {"input_text": "[7, 0, 1, 2, 4, 5, 6]", "expected_output": "3"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "The sum of integers from 0 to n has a closed-form formula: n * (n + 1) // 2.", "xp_cost": 2},
            {"level": 2, "text": "Alternatively, XORing every number in [0, n] and every element in nums cancels out present numbers.", "xp_cost": 5},
            {"level": 3, "text": "Use Gauss summation or Bitwise XOR to find the difference in O(1) space.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Gauss Summation / XOR Accumulator\n\nThe sum of numbers from 0 to $n$ is $n(n+1)/2$. Subtracting the sum of array elements yields the missing value directly.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ single pass.\n- **Space Complexity:** $O(1)$ auxiliary memory.\n\n#### Common Pitfalls\n- Potential integer overflow in languages with fixed integer width (mitigated with 64-bit integers or XOR).",
        "reference_solutions": {
            "brute_python": "def missingNumber(nums):\n    n = len(nums)\n    for i in range(n + 1):\n        if i not in nums:\n            return i\n    return -1",
            "optimal_python": "def missingNumber(nums):\n    n = len(nums)\n    expected = n * (n + 1) // 2\n    return expected - sum(nums)",
            "optimal_java": "public class Solution {\n    public int missingNumber(int[] nums) {\n        int n = nums.length;\n        long expected = (long) n * (n + 1) / 2;\n        long actual = 0;\n        for (int x : nums) actual += x;\n        return (int) (expected - actual);\n    }\n}",
            "optimal_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int missingNumber(vector<int>& nums) {\n        long long n = nums.size();\n        long long expected = n * (n + 1) / 2;\n        long long actual = 0;\n        for (int x : nums) actual += x;\n        return (int)(expected - actual);\n    }\n};"
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
    print(f"Batch 1 generated {count} problems.")

if __name__ == "__main__":
    main()
