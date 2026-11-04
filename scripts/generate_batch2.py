"""
Problem Generator - Batch 2: Two Pointers & Sliding Window (8 problems)
Mix: 3 Easy, 4 Medium, 1 Hard
"""
import os
import json

PROBLEMS = [
    # 11. Two Pointers - Easy
    {
        "slug": "two-sum-sorted-offsets",
        "title": "Two Sum in Ascending Sorted Sequence",
        "difficulty": "easy",
        "topic": "Two Pointers and Sliding Window",
        "tags": ["Two Pointers", "Array", "Binary Search"],
        "company_tags": ["Amazon", "Google", "Apple"],
        "statement_md": "Given a 1-indexed array of integers `numbers` that is already sorted in non-decreasing order, find two numbers such that they add up to a specific `target` number.\n\nReturn the indices of the two numbers, `[index1, index2]`, as a 1-indexed integer array of length 2.\n\nYou may not use the same element twice. There is guaranteed to be exactly one solution.\n\n### Input Format\n- Line 1: A JSON-encoded list of integers `numbers`\n- Line 2: An integer `target`\n\n### Output Format\n- A 1-indexed JSON-encoded list `[index1, index2]`",
        "examples": [
            {
                "input": "[2, 7, 11, 15]\n9",
                "output": "[1, 2]",
                "explanation": "The sum of 2 and 7 is 9. Therefore index1 = 1, index2 = 2."
            },
            {
                "input": "[2, 3, 4]\n6",
                "output": "[1, 3]",
                "explanation": "The sum of 2 and 4 is 6. Therefore index1 = 1, index2 = 3."
            }
        ],
        "sample_tests": [
            {"input_text": "[2, 7, 11, 15]\n9", "expected_output": "[1, 2]"},
            {"input_text": "[2, 3, 4]\n6", "expected_output": "[1, 3]"},
            {"input_text": "[-1, 0]\n-1", "expected_output": "[1, 2]"}
        ],
        "hidden_tests": [
            {"input_text": "[1, 2]\n3", "expected_output": "[1, 2]"},
            {"input_text": "[0, 0, 3, 4]\n0", "expected_output": "[1, 2]"},
            {"input_text": "[-5, -3, 0, 2, 4, 6, 8]\n5", "expected_output": "[2, 7]"},
            {"input_text": "[1, 3, 5, 7, 9, 11]\n14", "expected_output": "[2, 6]"},
            {"input_text": "[-10, -8, -6, -4, -2]\n-14", "expected_output": "[1, 4]"},
            {"input_text": "[1, 2, 3, 4, 4, 9, 12]\n8", "expected_output": "[4, 5]"},
            {"input_text": "[5, 25, 75]\n100", "expected_output": "[2, 3]"},
            {"input_text": "[-1000, -500, 0, 500, 1000]\n0", "expected_output": "[1, 5]"},
            {"input_text": "[1, 2, 3, 7, 11]\n9", "expected_output": "[2, 4]"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Take advantage of the sorted property of numbers.", "xp_cost": 2},
            {"level": 2, "text": "Place one pointer at index 0 and another at index n - 1.", "xp_cost": 5},
            {"level": 3, "text": "Use Two Pointers converging inward based on whether the current sum is less than or greater than target.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Inward Converging Two Pointers\n\nInitialize `left = 0` and `right = len(numbers) - 1`. Sum `numbers[left] + numbers[right]`. If equal to target, return `[left + 1, right + 1]`. If sum < target, advance `left`. If sum > target, decrement `right`.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ single pass.\n- **Space Complexity:** $O(1)$ auxiliary storage.\n\n#### Common Pitfalls\n- Returning 0-indexed indices instead of 1-indexed.",
        "reference_solutions": {
            "brute_python": "def twoSumSorted(numbers, target):\n    n = len(numbers)\n    for i in range(n):\n        for j in range(i + 1, n):\n            if numbers[i] + numbers[j] == target:\n                return [i + 1, j + 1]\n    return []",
            "optimal_python": "def twoSumSorted(numbers, target):\n    left, right = 0, len(numbers) - 1\n    while left < right:\n        cur = numbers[left] + numbers[right]\n        if cur == target:\n            return [left + 1, right + 1]\n        elif cur < target:\n            left += 1\n        else:\n            right -= 1\n    return []",
            "optimal_java": "public class Solution {\n    public int[] twoSumSorted(int[] numbers, int target) {\n        int left = 0, right = numbers.length - 1;\n        while (left < right) {\n            int sum = numbers[left] + numbers[right];\n            if (sum == target) return new int[]{left + 1, right + 1};\n            else if (sum < target) left++;\n            else right--;\n        }\n        return new int[]{};\n    }\n}",
            "optimal_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> twoSumSorted(vector<int>& numbers, int target) {\n        int left = 0, right = numbers.size() - 1;\n        while (left < right) {\n            int sum = numbers[left] + numbers[right];\n            if (sum == target) return {left + 1, right + 1};\n            else if (sum < target) left++;\n            else right--;\n        }\n        return {};\n    }\n};"
        }
    },

    # 12. Two Pointers - Easy
    {
        "slug": "reverse-vowels-preserving-order",
        "title": "Reverse Vowels While Preserving Consonants",
        "difficulty": "easy",
        "topic": "Two Pointers and Sliding Window",
        "tags": ["Two Pointers", "String"],
        "company_tags": ["Apple", "Google", "Amazon"],
        "statement_md": "Given a string `s`, reverse only all the vowels in the string and return it.\n\nThe vowels are `'a'`, `'e'`, `'i'`, `'o'`, and `'u'`, and they can appear in both lower and upper cases, more than once.\n\n### Input Format\n- A JSON string `s`\n\n### Output Format\n- A string with vowels reversed",
        "examples": [
            {
                "input": "\"IceCreAm\"",
                "output": "\"AceCreIm\"",
                "explanation": "The vowels are ['I', 'e', 'e', 'A']. In reverse order they become ['A', 'e', 'e', 'I']."
            },
            {
                "input": "\"leetcode\"",
                "output": "\"leotcede\"",
                "explanation": "The vowels are ['e', 'e', 'o', 'e']. In reverse order they become ['e', 'o', 'e', 'e']."
            }
        ],
        "sample_tests": [
            {"input_text": "\"IceCreAm\"", "expected_output": "\"AceCreIm\""},
            {"input_text": "\"leetcode\"", "expected_output": "\"leotcede\""},
            {"input_text": "\"hello\"", "expected_output": "\"holle\""}
        ],
        "hidden_tests": [
            {"input_text": "\"\"", "expected_output": "\"\""},
            {"input_text": "\"a\"", "expected_output": "\"a\""},
            {"input_text": "\"bcdfg\"", "expected_output": "\"bcdfg\""},
            {"input_text": "\"aeiou\"", "expected_output": "\"uoiea\""},
            {"input_text": "\"AEIOU\"", "expected_output": "\"UOIEA\""},
            {"input_text": "\"aA\"", "expected_output": "\"Aa\""},
            {"input_text": "\"Ready2Code\"", "expected_output": "\"Reody2Cade\""},
            {"input_text": "\"race car\"", "expected_output": "\"race car\""},
            {"input_text": "\"algorithmic\"", "expected_output": "\"ilgirothmac\""}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Set up a pointer at the beginning and a pointer at the end of the character array.", "xp_cost": 2},
            {"level": 2, "text": "Advance left until pointing to a vowel, and decrement right until pointing to a vowel, then swap.", "xp_cost": 5},
            {"level": 3, "text": "Use Two Pointers converging inward while checking vowel membership in a lookup set.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Two-Pointer Vowel Swap\n\nConvert string to character list. Use `left = 0` and `right = len(s) - 1`. Advance `left` until a vowel is found; decrement `right` until a vowel is found. Swap characters and move inward.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ each character visited at most twice.\n- **Space Complexity:** $O(n)$ for mutable character array.\n\n#### Common Pitfalls\n- Missing uppercase vowels (`A, E, I, O, U`).",
        "reference_solutions": {
            "brute_python": "def reverseVowels(s):\n    vowels = set('aeiouAEIOU')\n    extracted = [c for c in s if c in vowels]\n    res = []\n    for c in s:\n        if c in vowels:\n            res.append(extracted.pop())\n        else:\n            res.append(c)\n    return ''.join(res)",
            "optimal_python": "def reverseVowels(s):\n    vowels = set('aeiouAEIOU')\n    arr = list(s)\n    left, right = 0, len(arr) - 1\n    while left < right:\n        while left < right and arr[left] not in vowels:\n            left += 1\n        while left < right and arr[right] not in vowels:\n            right -= 1\n        if left < right:\n            arr[left], arr[right] = arr[right], arr[left]\n            left += 1\n            right -= 1\n    return ''.join(arr)",
            "optimal_java": "public class Solution {\n    public String reverseVowels(String s) {\n        char[] arr = s.toCharArray();\n        String vowels = \"aeiouAEIOU\";\n        int left = 0, right = arr.length - 1;\n        while (left < right) {\n            while (left < right && vowels.indexOf(arr[left]) == -1) left++;\n            while (left < right && vowels.indexOf(arr[right]) == -1) right--;\n            if (left < right) {\n                char tmp = arr[left];\n                arr[left] = arr[right];\n                arr[right] = tmp;\n                left++;\n                right--;\n            }\n        }\n        return new String(arr);\n    }\n}",
            "optimal_cpp": "#include <string>\n#include <unordered_set>\nusing namespace std;\nclass Solution {\npublic:\n    string reverseVowels(string s) {\n        unordered_set<char> vowels = {'a','e','i','o','u','A','E','I','O','U'};\n        int left = 0, right = (int)s.size() - 1;\n        while (left < right) {\n            while (left < right && !vowels.count(s[left])) left++;\n            while (left < right && !vowels.count(s[right])) right--;\n            if (left < right) {\n                swap(s[left], s[right]);\n                left++;\n                right--;\n            }\n        }\n        return s;\n    }\n};"
        }
    },

    # 13. Two Pointers - Easy
    {
        "slug": "remove-duplicates-at-most-twice",
        "title": "Remove Duplicates Allowing At Most Two Occurrences",
        "difficulty": "easy",
        "topic": "Two Pointers and Sliding Window",
        "tags": ["Two Pointers", "Array"],
        "company_tags": ["Meta", "Microsoft", "Amazon"],
        "statement_md": "Given an integer array `nums` sorted in non-decreasing order, remove some duplicates in-place such that each unique element appears at most twice. The relative order of the elements should be kept the same.\n\nReturn the integer length `k` of the modified array.\n\n### Input Format\n- A JSON-encoded list of sorted integers `nums`\n\n### Output Format\n- An integer representing length `k`",
        "examples": [
            {
                "input": "[1, 1, 1, 2, 2, 3]",
                "output": "5",
                "explanation": "Your function should return k = 5, with the first five elements of nums being 1, 1, 2, 2 and 3."
            },
            {
                "input": "[0, 0, 1, 1, 1, 1, 2, 3, 3]",
                "output": "7",
                "explanation": "Your function should return k = 7, elements: 0, 0, 1, 1, 2, 3, 3."
            }
        ],
        "sample_tests": [
            {"input_text": "[1, 1, 1, 2, 2, 3]", "expected_output": "5"},
            {"input_text": "[0, 0, 1, 1, 1, 1, 2, 3, 3]", "expected_output": "7"},
            {"input_text": "[1, 2, 3]", "expected_output": "3"}
        ],
        "hidden_tests": [
            {"input_text": "[]", "expected_output": "0"},
            {"input_text": "[1]", "expected_output": "1"},
            {"input_text": "[1, 1]", "expected_output": "2"},
            {"input_text": "[1, 1, 1, 1, 1]", "expected_output": "2"},
            {"input_text": "[-3, -3, -3, -2, -2, 0, 0, 0, 1]", "expected_output": "7"},
            {"input_text": "[1, 1, 2, 2, 3, 3]", "expected_output": "6"},
            {"input_text": "[-10, -10, -10, -5, -5, -5, 0, 0, 0]", "expected_output": "6"},
            {"input_text": "[5, 5, 5, 5, 5, 5, 5, 5]", "expected_output": "2"},
            {"input_text": "[1, 2, 2, 2, 3, 4, 4, 4, 5]", "expected_output": "7"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Since the array is sorted, any valid element to insert at write index w cannot equal nums[w - 2].", "xp_cost": 2},
            {"level": 2, "text": "Maintain a write pointer starting at index 2.", "xp_cost": 5},
            {"level": 3, "text": "Use Fast and Slow Pointers to scan with read index and overwrite at write index.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Fast & Slow Pointer Partition\n\nIf array length $\\le 2$, return length directly. Otherwise, maintain `write = 2`. For each `x` from index 2 onwards, if `x != nums[write - 2]`, set `nums[write] = x` and `write += 1`.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ single pass.\n- **Space Complexity:** $O(1)$ in-place modification.\n\n#### Common Pitfalls\n- Comparing with `nums[write - 1]` instead of `nums[write - 2]` (which would limit to 1 occurrence instead of 2).",
        "reference_solutions": {
            "brute_python": "def removeDuplicates(nums):\n    res = []\n    for x in nums:\n        if res.count(x) < 2:\n            res.append(x)\n    for i in range(len(res)): nums[i] = res[i]\n    return len(res)",
            "optimal_python": "def removeDuplicates(nums):\n    if len(nums) <= 2:\n        return len(nums)\n    write = 2\n    for i in range(2, len(nums)):\n        if nums[i] != nums[write - 2]:\n            nums[write] = nums[i]\n            write += 1\n    return write",
            "optimal_java": "public class Solution {\n    public int removeDuplicates(int[] nums) {\n        if (nums.length <= 2) return nums.length;\n        int write = 2;\n        for (int i = 2; i < nums.length; i++) {\n            if (nums[i] != nums[write - 2]) {\n                nums[write++] = nums[i];\n            }\n        }\n        return write;\n    }\n}",
            "optimal_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int removeDuplicates(vector<int>& nums) {\n        if (nums.size() <= 2) return nums.size();\n        int write = 2;\n        for (int i = 2; i < (int)nums.size(); i++) {\n            if (nums[i] != nums[write - 2]) {\n                nums[write++] = nums[i];\n            }\n        }\n        return write;\n    }\n};"
        }
    },

    # 14. Two Pointers - Medium
    {
        "slug": "triplet-sum-closest-to-bound",
        "title": "Triplet Sum Closest to Target Bound",
        "difficulty": "medium",
        "topic": "Two Pointers and Sliding Window",
        "tags": ["Two Pointers", "Sorting", "Array"],
        "company_tags": ["Bloomberg", "Google", "Amazon"],
        "statement_md": "Given an integer array `nums` of length `n` and an integer `target`, find three integers in `nums` such that the sum is closest to `target`.\n\nReturn the sum of the three integers.\n\nYou may assume that each input would have exactly one solution.\n\n### Input Format\n- Line 1: A JSON-encoded list of integers `nums` (length >= 3)\n- Line 2: An integer `target`\n\n### Output Format\n- An integer representing the closest triplet sum",
        "examples": [
            {
                "input": "[-1, 2, 1, -4]\n1",
                "output": "2",
                "explanation": "The sum that is closest to target is 2 (-1 + 2 + 1 = 2)."
            },
            {
                "input": "[0, 0, 0]\n1",
                "output": "0",
                "explanation": "The sum that is closest to target is 0 (0 + 0 + 0 = 0)."
            }
        ],
        "sample_tests": [
            {"input_text": "[-1, 2, 1, -4]\n1", "expected_output": "2"},
            {"input_text": "[0, 0, 0]\n1", "expected_output": "0"},
            {"input_text": "[1, 1, 1, 1]\n0", "expected_output": "3"}
        ],
        "hidden_tests": [
            {"input_text": "[1, 2, 3]\n6", "expected_output": "6"},
            {"input_text": "[1, 2, 3]\n100", "expected_output": "6"},
            {"input_text": "[-5, -4, -3, -2, -1]\n-10", "expected_output": "-10"},
            {"input_text": "[0, 1, 2]\n3", "expected_output": "3"},
            {"input_text": "[-10, 0, 10, 20, 30]\n16", "expected_output": "20"},
            {"input_text": "[4, 0, 5, -5, 3, 3, 0, -4, -5]\n-2", "expected_output": "-2"},
            {"input_text": "[1, 1, -1, -1, 3]\n-1", "expected_output": "-1"},
            {"input_text": "[10, 20, 30, 40, 50]\n85", "expected_output": "80"},
            {"input_text": "[-100, -98, -2, -1]\n-101", "expected_output": "-101"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Sort the array first so you can guide the search with two pointers.", "xp_cost": 2},
            {"level": 2, "text": "For each fixed first element nums[i], use left = i + 1 and right = n - 1.", "xp_cost": 5},
            {"level": 3, "text": "Use Two Pointers after sorting, tracking the minimum absolute difference |current_sum - target|.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Two Pointers with Sorting\n\nSort `nums`. For each index `i`, set `left = i + 1` and `right = len(nums) - 1`. If `abs(sum - target) < abs(best - target)`, update `best`. Adjust pointers according to whether sum is less or greater than target.\n\n#### Complexity\n- **Time Complexity:** $O(n^2)$ outer loop times two-pointer convergence.\n- **Space Complexity:** $O(1)$ auxiliary space.\n\n#### Common Pitfalls\n- Comparing signed differences instead of absolute differences.",
        "reference_solutions": {
            "brute_python": "def threeSumClosest(nums, target):\n    n = len(nums)\n    closest = nums[0] + nums[1] + nums[2]\n    for i in range(n):\n        for j in range(i + 1, n):\n            for k in range(j + 1, n):\n                cur = nums[i] + nums[j] + nums[k]\n                if abs(cur - target) < abs(closest - target):\n                    closest = cur\n    return closest",
            "optimal_python": "def threeSumClosest(nums, target):\n    nums.sort()\n    closest = nums[0] + nums[1] + nums[2]\n    n = len(nums)\n    for i in range(n - 2):\n        left, right = i + 1, n - 1\n        while left < right:\n            cur = nums[i] + nums[left] + nums[right]\n            if cur == target:\n                return cur\n            if abs(cur - target) < abs(closest - target):\n                closest = cur\n            if cur < target:\n                left += 1\n            else:\n                right -= 1\n    return closest",
            "optimal_java": "import java.util.Arrays;\npublic class Solution {\n    public int threeSumClosest(int[] nums, int target) {\n        Arrays.sort(nums);\n        int closest = nums[0] + nums[1] + nums[2];\n        for (int i = 0; i < nums.length - 2; i++) {\n            int left = i + 1, right = nums.length - 1;\n            while (left < right) {\n                int cur = nums[i] + nums[left] + nums[right];\n                if (cur == target) return cur;\n                if (Math.abs(cur - target) < Math.abs(closest - target)) closest = cur;\n                if (cur < target) left++;\n                else right--;\n            }\n        }\n        return closest;\n    }\n}",
            "optimal_cpp": "#include <vector>\n#include <algorithm>\n#include <cmath>\nusing namespace std;\nclass Solution {\npublic:\n    int threeSumClosest(vector<int>& nums, int target) {\n        sort(nums.begin(), nums.end());\n        int closest = nums[0] + nums[1] + nums[2];\n        int n = nums.size();\n        for (int i = 0; i < n - 2; i++) {\n            int left = i + 1, right = n - 1;\n            while (left < right) {\n                int cur = nums[i] + nums[left] + nums[right];\n                if (cur == target) return cur;\n                if (abs(cur - target) < abs(closest - target)) closest = cur;\n                if (cur < target) left++;\n                else right--;\n            }\n        }\n        return closest;\n    }\n};"
        }
    },

    # 15. Two Pointers - Medium
    {
        "slug": "longest-substring-k-distinct-chars",
        "title": "Longest Substring with At Most K Distinct Characters",
        "difficulty": "medium",
        "topic": "Two Pointers and Sliding Window",
        "tags": ["Sliding Window", "Hash Table", "String"],
        "company_tags": ["Google", "Amazon", "Microsoft"],
        "statement_md": "Given a string `s` and an integer `k`, return the length of the longest substring of `s` that contains at most `k` distinct characters.\n\n### Input Format\n- Line 1: A string `s`\n- Line 2: An integer `k` (`k >= 0`)\n\n### Output Format\n- An integer representing the maximum substring length",
        "examples": [
            {
                "input": "\"eceba\"\n2",
                "output": "3",
                "explanation": "The substring is \"ece\" with length 3."
            },
            {
                "input": "\"aa\"\n1",
                "output": "2",
                "explanation": "The substring is \"aa\" with length 2."
            }
        ],
        "sample_tests": [
            {"input_text": "\"eceba\"\n2", "expected_output": "3"},
            {"input_text": "\"aa\"\n1", "expected_output": "2"},
            {"input_text": "\"a\"\n0", "expected_output": "0"}
        ],
        "hidden_tests": [
            {"input_text": "\"\"\n2", "expected_output": "0"},
            {"input_text": "\"a\"\n1", "expected_output": "1"},
            {"input_text": "\"abcadcacacaca\"\n3", "expected_output": "11"},
            {"input_text": "\"abcdefg\"\n1", "expected_output": "1"},
            {"input_text": "\"abcdefg\"\n7", "expected_output": "7"},
            {"input_text": "\"abaccc\"\n2", "expected_output": "4"},
            {"input_text": "\"araaci\"\n2", "expected_output": "4"},
            {"input_text": "\"cbbebi\"\n3", "expected_output": "5"},
            {"input_text": "\"aabbccddeeff\"\n2", "expected_output": "4"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "If k == 0 or the string is empty, the result is immediately 0.", "xp_cost": 2},
            {"level": 2, "text": "Expand the right boundary while maintaining character frequencies in the window.", "xp_cost": 5},
            {"level": 3, "text": "Use a Sliding Window with a Hash Map storing character counts, shrinking from left when distinct count > k.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Sliding Window Frequency Map\n\nExpand `right` and record character count in a map. When `len(map) > k`, increment `left` and decrement frequency until a character count hits 0 and is removed from the map. Update `max_len = max(max_len, right - left + 1)`.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ each character added and removed from window once.\n- **Space Complexity:** $O(k)$ for frequency map.\n\n#### Common Pitfalls\n- Not deleting key from map when count drops to 0.",
        "reference_solutions": {
            "brute_python": "def lengthOfLongestSubstringKDistinct(s, k):\n    if k == 0 or not s: return 0\n    max_len = 0\n    n = len(s)\n    for i in range(n):\n        seen = set()\n        for j in range(i, n):\n            seen.add(s[j])\n            if len(seen) <= k:\n                max_len = max(max_len, j - i + 1)\n            else:\n                break\n    return max_len",
            "optimal_python": "def lengthOfLongestSubstringKDistinct(s, k):\n    if k == 0 or not s:\n        return 0\n    counts = {}\n    left = 0\n    max_len = 0\n    for right, ch in enumerate(s):\n        counts[ch] = counts.get(ch, 0) + 1\n        while len(counts) > k:\n            counts[s[left]] -= 1\n            if counts[s[left]] == 0:\n                del counts[s[left]]\n            left += 1\n        max_len = max(max_len, right - left + 1)\n    return max_len",
            "optimal_java": "import java.util.*;\npublic class Solution {\n    public int lengthOfLongestSubstringKDistinct(String s, int k) {\n        if (k == 0 || s == null || s.length() == 0) return 0;\n        Map<Character, Integer> counts = new HashMap<>();\n        int left = 0, maxLen = 0;\n        for (int right = 0; right < s.length(); right++) {\n            char c = s.charAt(right);\n            counts.put(c, counts.getOrDefault(c, 0) + 1);\n            while (counts.size() > k) {\n                char lc = s.charAt(left);\n                counts.put(lc, counts.get(lc) - 1);\n                if (counts.get(lc) == 0) counts.remove(lc);\n                left++;\n            }\n            maxLen = Math.max(maxLen, right - left + 1);\n        }\n        return maxLen;\n    }\n}",
            "optimal_cpp": "#include <string>\n#include <unordered_map>\n#include <algorithm>\nusing namespace std;\nclass Solution {\npublic:\n    int lengthOfLongestSubstringKDistinct(string s, int k) {\n        if (k == 0 || s.empty()) return 0;\n        unordered_map<char, int> counts;\n        int left = 0, maxLen = 0;\n        for (int right = 0; right < (int)s.size(); right++) {\n            counts[s[right]]++;\n            while ((int)counts.size() > k) {\n                counts[s[left]]--;\n                if (counts[s[left]] == 0) counts.erase(s[left]);\n                left++;\n            }\n            maxLen = max(maxLen, right - left + 1);\n        }\n        return maxLen;\n    }\n};"
        }
    },

    # 16. Two Pointers - Medium
    {
        "slug": "minimum-consecutive-cards-for-match",
        "title": "Minimum Consecutive Cards for Duplicate Match",
        "difficulty": "medium",
        "topic": "Two Pointers and Sliding Window",
        "tags": ["Sliding Window", "Hash Table", "Array"],
        "company_tags": ["Amazon", "Google", "Microsoft"],
        "statement_md": "You are given an integer array `cards` where `cards[i]` represents the value of the `i-th` card. A pair of cards are matching if they have the same value.\n\nReturn the minimum number of consecutive cards you have to pick up to have at least one pair of matching cards among the picked cards. If it is impossible, return `-1`.\n\n### Input Format\n- A JSON-encoded list of integers `cards`\n\n### Output Format\n- An integer representing the minimum window size",
        "examples": [
            {
                "input": "[3, 4, 2, 3, 4, 7]",
                "output": "4",
                "explanation": "We can pick cards from index 0 to 3 ([3, 4, 2, 3]) which gives a pair of 3s, length 4."
            },
            {
                "input": "[1, 0, 5, 3]",
                "output": "-1",
                "explanation": "There are no matching cards in the entire array."
            }
        ],
        "sample_tests": [
            {"input_text": "[3, 4, 2, 3, 4, 7]", "expected_output": "4"},
            {"input_text": "[1, 0, 5, 3]", "expected_output": "-1"},
            {"input_text": "[1, 1]", "expected_output": "2"}
        ],
        "hidden_tests": [
            {"input_text": "[]", "expected_output": "-1"},
            {"input_text": "[10]", "expected_output": "-1"},
            {"input_text": "[1, 2, 3, 1, 2, 3]", "expected_output": "4"},
            {"input_text": "[7, 7, 7, 7]", "expected_output": "2"},
            {"input_text": "[5, 6, 7, 8, 9, 5]", "expected_output": "6"},
            {"input_text": "[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]", "expected_output": "-1"},
            {"input_text": "[9, 5, 3, 5, 9]", "expected_output": "3"},
            {"input_text": "[-1, -2, -1, -2]", "expected_output": "3"},
            {"input_text": "[100, 200, 300, 400, 200]", "expected_output": "4"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Notice that the minimum distance between matching cards is the minimum distance between any two adjacent occurrences of the same card.", "xp_cost": 2},
            {"level": 2, "text": "Track the last seen index for each card value.", "xp_cost": 5},
            {"level": 3, "text": "Use a Hash Map recording last_index[card] to find min(i - last_index[card] + 1).", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Last Seen Index Tracking\n\nStore the most recent index where each card was seen. When a duplicate `card` is encountered at index `i`, the window length is `i - last_seen[card] + 1`. Minimize this across all cards.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ single pass.\n- **Space Complexity:** $O(n)$ hash table storage.\n\n#### Common Pitfalls\n- Returning length - 1 instead of length (inclusive of both matching endpoints).",
        "reference_solutions": {
            "brute_python": "def minimumCardPickup(cards):\n    min_len = float('inf')\n    n = len(cards)\n    for i in range(n):\n        for j in range(i + 1, n):\n            if cards[i] == cards[j]:\n                min_len = min(min_len, j - i + 1)\n                break\n    return min_len if min_len != float('inf') else -1",
            "optimal_python": "def minimumCardPickup(cards):\n    last_seen = {}\n    min_dist = float('inf')\n    for i, card in enumerate(cards):\n        if card in last_seen:\n            min_dist = min(min_dist, i - last_seen[card] + 1)\n        last_seen[card] = i\n    return min_dist if min_dist != float('inf') else -1",
            "optimal_java": "import java.util.*;\npublic class Solution {\n    public int minimumCardPickup(int[] cards) {\n        Map<Integer, Integer> lastSeen = new HashMap<>();\n        int minDist = Integer.MAX_VALUE;\n        for (int i = 0; i < cards.length; i++) {\n            if (lastSeen.containsKey(cards[i])) {\n                minDist = Math.min(minDist, i - lastSeen.get(cards[i]) + 1);\n            }\n            lastSeen.put(cards[i], i);\n        }\n        return minDist == Integer.MAX_VALUE ? -1 : minDist;\n    }\n}",
            "optimal_cpp": "#include <vector>\n#include <unordered_map>\n#include <algorithm>\nusing namespace std;\nclass Solution {\npublic:\n    int minimumCardPickup(vector<int>& cards) {\n        unordered_map<int, int> lastSeen;\n        int minDist = 1e9;\n        for (int i = 0; i < (int)cards.size(); i++) {\n            if (lastSeen.count(cards[i])) {\n                minDist = min(minDist, i - lastSeen[cards[i]] + 1);\n            }\n            lastSeen[cards[i]] = i;\n        }\n        return minDist == 1e9 ? -1 : minDist;\n    }\n};"
        }
    },

    # 17. Two Pointers - Medium
    {
        "slug": "container-with-bounded-walls",
        "title": "Container with Most Water Between Bounded Walls",
        "difficulty": "medium",
        "topic": "Two Pointers and Sliding Window",
        "tags": ["Two Pointers", "Greedy", "Array"],
        "company_tags": ["Google", "Amazon", "Meta", "Adobe"],
        "statement_md": "You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `i-th` line are `(i, 0)` and `(i, height[i])`.\n\nFind two lines that together with the x-axis form a container, such that the container contains the most water.\n\nReturn the maximum amount of water a container can store.\n\n### Input Format\n- A JSON-encoded list of integers `height` (length >= 2)\n\n### Output Format\n- An integer representing maximum water capacity",
        "examples": [
            {
                "input": "[1, 8, 6, 2, 5, 4, 8, 3, 7]",
                "output": "49",
                "explanation": "The maximum area is obtained between index 1 (height 8) and index 8 (height 7): min(8, 7) * (8 - 1) = 7 * 7 = 49."
            },
            {
                "input": "[1, 1]",
                "output": "1",
                "explanation": "min(1, 1) * (1 - 0) = 1."
            }
        ],
        "sample_tests": [
            {"input_text": "[1, 8, 6, 2, 5, 4, 8, 3, 7]", "expected_output": "49"},
            {"input_text": "[1, 1]", "expected_output": "1"},
            {"input_text": "[4, 3, 2, 1, 4]", "expected_output": "16"}
        ],
        "hidden_tests": [
            {"input_text": "[1, 2, 1]", "expected_output": "2"},
            {"input_text": "[1, 2, 4, 3]", "expected_output": "4"},
            {"input_text": "[2, 3, 4, 5, 18, 17, 6]", "expected_output": "17"},
            {"input_text": "[10, 9, 8, 7, 6, 5, 4, 3, 2, 1]", "expected_output": "25"},
            {"input_text": "[1, 100, 100, 1]", "expected_output": "100"},
            {"input_text": "[5, 5, 5, 5, 5]", "expected_output": "20"},
            {"input_text": "[100, 100]", "expected_output": "100"},
            {"input_text": "[1, 3, 2, 5, 25, 24, 5]", "expected_output": "24"},
            {"input_text": "[0, 2]", "expected_output": "0"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "The width is maximized when taking the two furthest endpoints.", "xp_cost": 2},
            {"level": 2, "text": "The limiting factor is the shorter of the two walls. Moving the taller wall can never increase area with a smaller width.", "xp_cost": 5},
            {"level": 3, "text": "Use Two Pointers starting at the extremities and greedily advance the pointer with the smaller height.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Greedily Converging Two Pointers\n\nStart with `left = 0` and `right = n - 1`. The current area is `(right - left) * min(height[left], height[right])`. To potentially find a larger area, we must advance the pointer pointing to the shorter vertical bar.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ single pass.\n- **Space Complexity:** $O(1)$ constant memory.\n\n#### Common Pitfalls\n- Moving the larger height pointer instead of the shorter height pointer.",
        "reference_solutions": {
            "brute_python": "def maxArea(height):\n    max_water = 0\n    n = len(height)\n    for i in range(n):\n        for j in range(i + 1, n):\n            max_water = max(max_water, (j - i) * min(height[i], height[j]))\n    return max_water",
            "optimal_python": "def maxArea(height):\n    left, right = 0, len(height) - 1\n    max_water = 0\n    while left < right:\n        cur = (right - left) * min(height[left], height[right])\n        if cur > max_water:\n            max_water = cur\n        if height[left] < height[right]:\n            left += 1\n        else:\n            right -= 1\n    return max_water",
            "optimal_java": "public class Solution {\n    public int maxArea(int[] height) {\n        int left = 0, right = height.length - 1;\n        int maxWater = 0;\n        while (left < right) {\n            int cur = (right - left) * Math.min(height[left], height[right]);\n            if (cur > maxWater) maxWater = cur;\n            if (height[left] < height[right]) left++;\n            else right--;\n        }\n        return maxWater;\n    }\n}",
            "optimal_cpp": "#include <vector>\n#include <algorithm>\nusing namespace std;\nclass Solution {\npublic:\n    int maxArea(vector<int>& height) {\n        int left = 0, right = (int)height.size() - 1;\n        int maxWater = 0;\n        while (left < right) {\n            int cur = (right - left) * min(height[left], height[right]);\n            if (cur > maxWater) maxWater = cur;\n            if (height[left] < height[right]) left++;\n            else right--;\n        }\n        return maxWater;\n    }\n};"
        }
    },

    # 18. Two Pointers - Hard
    {
        "slug": "minimum-window-subsequence-match",
        "title": "Minimum Window Subsequence Match",
        "difficulty": "hard",
        "topic": "Two Pointers and Sliding Window",
        "tags": ["Two Pointers", "Dynamic Programming", "Sliding Window"],
        "company_tags": ["Google", "Meta", "Amazon", "Uber"],
        "statement_md": "Given strings `s1` and `s2`, return the minimum contiguous substring `W` of `s1`, so that `s2` is a subsequence of `W`.\n\nIf there is no such window in `s1` that covers all characters in `s2`, return the empty string `\"\"`. If there are multiple such minimum-length windows, return the one with the smallest starting index.\n\n### Input Format\n- Line 1: String `s1`\n- Line 2: String `s2`\n\n### Output Format\n- A string representing the minimal window substring",
        "examples": [
            {
                "input": "\"abcdebdde\"\n\"bde\"",
                "output": "\"bcde\"",
                "explanation": "\"bcde\" is the first substring containing \"bde\" as a subsequence (length 4). \"bdde\" also has length 4, but occurs later."
            },
            {
                "input": "\"jmeqforevndlit\"\n\"u\"",
                "output": "\"\"",
                "explanation": "\"u\" does not appear in s1, so no window exists."
            }
        ],
        "sample_tests": [
            {"input_text": "\"abcdebdde\"\n\"bde\"", "expected_output": "\"bcde\""},
            {"input_text": "\"jmeqforevndlit\"\n\"u\"", "expected_output": "\"\""},
            {"input_text": "\"fgrqsqsnodwmxzkzxwqegkndaa\"\n\"k\"", "expected_output": "\"k\""}
        ],
        "hidden_tests": [
            {"input_text": "\"\"\n\"a\"", "expected_output": "\"\""},
            {"input_text": "\"a\"\n\"a\"", "expected_output": "\"a\""},
            {"input_text": "\"abc\"\n\"abc\"", "expected_output": "\"abc\""},
            {"input_text": "\"bbbbdebdde\"\n\"bde\"", "expected_output": "\"bde\""},
            {"input_text": "\"cnhczmccqouqadqtmjjzl\"\n\"mm\"", "expected_output": "\"mccqouqadqtm\""},
            {"input_text": "\"abcdefg\"\n\"ace\"", "expected_output": "\"abcde\""},
            {"input_text": "\"hgh9xabxcdxef\"\n\"abcdef\"", "expected_output": "\"abxcdxef\""},
            {"input_text": "\"zxyxyz\"\n\"xyz\"", "expected_output": "\"xyz\""},
            {"input_text": "\"aaaaa\"\n\"aaa\"", "expected_output": "\"aaa\""}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Scan forward to find any match of s2 as a subsequence.", "xp_cost": 2},
            {"level": 2, "text": "Once the end of s2 is matched, scan backwards from that end to find the optimal start of this specific window.", "xp_cost": 5},
            {"level": 3, "text": "Use Two Pointers with forward greedy match and reverse pointer contraction.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Forward Scan with Reverse Contraction\n\n1. Iterate pointer `i` through `s1` and pointer `j` through `s2`. Advance `j` when `s1[i] == s2[j]`.\n2. When `j == len(s2)`, we have found an end of a valid window at index `end = i`.\n3. Contract backwards: decrement `j` while decrementing `i` until `j < 0`. The index `start = i + 1` gives the tightest starting point for this window.\n4. Update min window if `end - start + 1 < min_len`.\n5. Reset `i = start + 1` and `j = 0` to search for subsequent occurrences.\n\n#### Complexity\n- **Time Complexity:** $O(N \\cdot M)$ where $N = \\text{len}(s1)$ and $M = \\text{len}(s2)$.\n- **Space Complexity:** $O(1)$ auxiliary storage.\n\n#### Common Pitfalls\n- Restarting search at `end` instead of `start + 1`, potentially skipping overlapping shorter windows.",
        "reference_solutions": {
            "brute_python": "def minWindow(s1, s2):\n    def is_subseq(sub, pat):\n        it = iter(sub)\n        return all(c in it for c in pat)\n    n = len(s1)\n    min_str = \"\"\n    min_len = float('inf')\n    for i in range(n):\n        for j in range(i + 1, n + 1):\n            sub = s1[i:j]\n            if is_subseq(sub, s2):\n                if len(sub) < min_len:\n                    min_len = len(sub)\n                    min_str = sub\n                break\n    return min_str",
            "optimal_python": "def minWindow(s1, s2):\n    n, m = len(s1), len(s2)\n    i, j = 0, 0\n    min_len = float('inf')\n    res = \"\"\n    while i < n:\n        if s1[i] == s2[j]:\n            j += 1\n            if j == m:\n                end = i\n                j -= 1\n                while j >= 0:\n                    if s1[i] == s2[j]:\n                        j -= 1\n                    i -= 1\n                i += 1\n                start = i\n                if end - start + 1 < min_len:\n                    min_len = end - start + 1\n                    res = s1[start:end + 1]\n                j = 0\n        i += 1\n    return res",
            "optimal_java": "public class Solution {\n    public String minWindow(String s1, String s2) {\n        int n = s1.length(), m = s2.length();\n        int i = 0, j = 0;\n        int minLen = Integer.MAX_VALUE;\n        String res = \"\";\n        while (i < n) {\n            if (s1.charAt(i) == s2.charAt(j)) {\n                j++;\n                if (j == m) {\n                    int end = i;\n                    j--;\n                    while (j >= 0) {\n                        if (s1.charAt(i) == s2.charAt(j)) j--;\n                        i--;\n                    }\n                    i++;\n                    int start = i;\n                    if (end - start + 1 < minLen) {\n                        minLen = end - start + 1;\n                        res = s1.substring(start, end + 1);\n                    }\n                    j = 0;\n                }\n            }\n            i++;\n        }\n        return res;\n    }\n}",
            "optimal_cpp": "#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    string minWindow(string s1, string s2) {\n        int n = s1.size(), m = s2.size();\n        int i = 0, j = 0;\n        int minLen = 1e9;\n        string res = \"\";\n        while (i < n) {\n            if (s1[i] == s2[j]) {\n                j++;\n                if (j == m) {\n                    int end = i;\n                    j--;\n                    while (j >= 0) {\n                        if (s1[i] == s2[j]) j--;\n                        i--;\n                    }\n                    i++;\n                    int start = i;\n                    if (end - start + 1 < minLen) {\n                        minLen = end - start + 1;\n                        res = s1.substr(start, end - start + 1);\n                    }\n                    j = 0;\n                }\n            }\n            i++;\n        }\n        return res;\n    }\n};"
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
    print(f"Batch 2 generated {count} problems.")

if __name__ == "__main__":
    main()
