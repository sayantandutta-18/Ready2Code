"""
Ready2Code launch problem bank: 100 original problems.

Convention (the judge harness must follow this):
- Each problem is a function `fn(*params)`.
- stdin  : a JSON array with one value per parameter, e.g. [[2,7,11,15], 9]
- stdout : the JSON-encoded return value, e.g. [0,1]
Every problem has a reference solution (`sol`) and a random test generator (`gen`).
"""
import math
import bisect
import heapq
import os
from collections import Counter, defaultdict, deque
from itertools import groupby

PROBLEMS = []


def P(slug, title, topic, diff, stmt, fn, params, examples, sol, gen):
    PROBLEMS.append(dict(slug=slug, title=title, topic=topic, difficulty=diff, statement=stmt,
                         fn=fn, params=params, examples=examples, sol=sol, gen=gen))


# ---------- generator helpers ----------
def ints(r, n, lo, hi, mn=1):
    return [r.randint(lo, hi) for _ in range(r.randint(mn, n))]


def word(r, n, alpha="abc", mn=0):
    return "".join(r.choice(alpha) for _ in range(r.randint(mn, n)))


def sorted_distinct(r, n, lo, hi, mn=1):
    return sorted(r.sample(range(lo, hi + 1), r.randint(mn, n)))


def intervals(r, n=6, hi=20):
    out = []
    for _ in range(r.randint(1, n)):
        a = r.randint(0, hi)
        out.append([a, a + r.randint(1, 6)])
    return out


def grid01(r, R=5, C=5):
    rows, cols = r.randint(1, R), r.randint(1, C)
    return [[r.choice("01") for _ in range(cols)] for _ in range(rows)]


def rect(r, R, C, lo, hi):
    rr, cc = r.randint(1, R), r.randint(1, C)
    return [[r.randint(lo, hi) for _ in range(cc)] for _ in range(rr)]


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


def gtree(r, n=8):
    return [r.randint(0, 9)] + [None if r.random() < 0.35 else r.randint(0, 9) for _ in range(r.randint(0, n))]


def ins(root, v):
    if root is None:
        return TN(v)
    if v < root.val:
        root.left = ins(root.left, v)
    else:
        root.right = ins(root.right, v)
    return root


# =====================================================================
# ARRAYS AND HASHING (16)
# =====================================================================
def s_two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return sorted([seen[target - x], i])
        seen[x] = i
    return []


def g_two_sum(r):
    while True:
        nums = r.sample(range(-20, 21), r.randint(2, 8))
        a, b = r.sample(range(len(nums)), 2)
        t = nums[a] + nums[b]
        if sum(1 for i in range(len(nums)) for j in range(i + 1, len(nums)) if nums[i] + nums[j] == t) == 1:
            return [nums, t]


P("two-sum", "Two Sum", "arrays", "easy",
  "Given an array `nums` and an integer `target`, return the indices of the two numbers that add up to `target`. "
  "Exactly one solution exists. Return the two indices in ascending order.",
  "twoSum", ["nums", "target"], [[[2, 7, 11, 15], 9], [[3, 2, 4], 6]], s_two_sum, g_two_sum)


def s_contains_duplicate(nums):
    return len(set(nums)) != len(nums)


P("contains-duplicate", "Contains Duplicate", "arrays", "easy",
  "Return `true` if any value appears at least twice in the array, otherwise return `false`.",
  "containsDuplicate", ["nums"], [[[1, 2, 3, 1]], [[1, 2, 3, 4]]], s_contains_duplicate,
  lambda r: [ints(r, 8, -5, 5)])


def s_group_anagrams(strs):
    d = defaultdict(list)
    for w in strs:
        d["".join(sorted(w))].append(w)
    return sorted(sorted(g) for g in d.values())


P("group-anagrams", "Group Anagrams", "arrays", "medium",
  "Group strings that are anagrams of each other. Inside each group sort the words, then sort the groups. "
  "Return the list of groups.",
  "groupAnagrams", ["strs"], [[["eat", "tea", "tan", "ate", "nat", "bat"]]], s_group_anagrams,
  lambda r: [[word(r, 3, "abc", 1) for _ in range(r.randint(1, 6))]])


def s_majority_element(nums):
    return Counter(nums).most_common(1)[0][0]


def g_majority(r):
    k = r.randint(0, 4); m = r.randint(-5, 5)
    arr = [m] * (k + 1) + [r.randint(-5, 5) for _ in range(k)]
    r.shuffle(arr)
    return [arr]


P("majority-element", "Majority Element", "arrays", "easy",
  "Return the value that appears more than n/2 times in the array. Such a value always exists.",
  "majorityElement", ["nums"], [[[3, 2, 3]], [[2, 2, 1, 1, 1, 2, 2]]], s_majority_element, g_majority)


def s_product_except_self(nums):
    n = len(nums); out = [1] * n; p = 1
    for i in range(n):
        out[i] = p; p *= nums[i]
    p = 1
    for i in range(n - 1, -1, -1):
        out[i] *= p; p *= nums[i]
    return out


P("product-except-self", "Product of Array Except Self", "arrays", "medium",
  "For each index i, return the product of all elements except nums[i]. Do it without division.",
  "productExceptSelf", ["nums"], [[[1, 2, 3, 4]], [[-1, 1, 0, -3, 3]]], s_product_except_self,
  lambda r: [[r.randint(-3, 3) for _ in range(r.randint(2, 6))]])


def s_longest_consecutive(nums):
    s = set(nums); best = 0
    for x in s:
        if x - 1 not in s:
            y = x
            while y + 1 in s:
                y += 1
            best = max(best, y - x + 1)
    return best


P("longest-consecutive-sequence", "Longest Consecutive Sequence", "arrays", "medium",
  "Return the length of the longest run of consecutive integers that can be formed from the array. "
  "The order of elements does not matter.",
  "longestConsecutive", ["nums"], [[[100, 4, 200, 1, 3, 2]], [[0, 3, 7, 2, 5, 8, 4, 6, 0, 1]]],
  s_longest_consecutive, lambda r: [ints(r, 12, -10, 10)])


def s_missing_number(nums):
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)


def g_missing(r):
    n = r.randint(1, 10); m = r.randint(0, n)
    arr = [x for x in range(n + 1) if x != m]
    r.shuffle(arr)
    return [arr]


P("missing-number", "Missing Number", "arrays", "easy",
  "The array contains n distinct numbers taken from 0 to n. Return the one number that is missing.",
  "missingNumber", ["nums"], [[[3, 0, 1]], [[0, 1]]], s_missing_number, g_missing)


def s_intersection(a, b):
    return sorted(set(a) & set(b))


P("intersection-of-two-arrays", "Intersection of Two Arrays", "arrays", "easy",
  "Return the unique values that appear in both arrays, sorted in ascending order.",
  "intersection", ["nums1", "nums2"], [[[1, 2, 2, 1], [2, 2]], [[4, 9, 5], [9, 4, 9, 8, 4]]], s_intersection,
  lambda r: [ints(r, 8, 0, 9), ints(r, 8, 0, 9)])


def s_subarray_sum_k(nums, k):
    cnt = {0: 1}; s = 0; ans = 0
    for x in nums:
        s += x
        ans += cnt.get(s - k, 0)
        cnt[s] = cnt.get(s, 0) + 1
    return ans


P("subarray-sum-equals-k", "Subarray Sum Equals K", "arrays", "medium",
  "Count the number of contiguous subarrays whose elements sum to `k`.",
  "subarraySum", ["nums", "k"], [[[1, 1, 1], 2], [[1, 2, 3], 3]], s_subarray_sum_k,
  lambda r: [ints(r, 8, -3, 3), r.randint(-3, 3)])


def s_contiguous_array(nums):
    first = {0: -1}; bal = 0; best = 0
    for i, x in enumerate(nums):
        bal += 1 if x == 1 else -1
        if bal in first:
            best = max(best, i - first[bal])
        else:
            first[bal] = i
    return best


P("contiguous-array", "Contiguous Array", "arrays", "medium",
  "Given a binary array (only 0 and 1), return the length of the longest contiguous subarray with an equal "
  "number of 0s and 1s.",
  "findMaxLength", ["nums"], [[[0, 1]], [[0, 1, 0]]], s_contiguous_array,
  lambda r: [[r.randint(0, 1) for _ in range(r.randint(1, 10))]])


def s_single_number(nums):
    x = 0
    for v in nums:
        x ^= v
    return x


def g_single(r):
    vals = r.sample(range(-9, 10), r.randint(1, 4)); arr = [vals[0]]
    for v in vals[1:]:
        arr += [v, v]
    r.shuffle(arr)
    return [arr]


P("single-number", "Single Number", "arrays", "easy",
  "Every value appears twice except one value, which appears once. Return that value. "
  "Use O(1) extra space.",
  "singleNumber", ["nums"], [[[2, 2, 1]], [[4, 1, 2, 1, 2]]], s_single_number, g_single)


def s_rotate(nums, k):
    n = len(nums)
    if n == 0:
        return []
    k %= n
    return nums[n - k:] + nums[:n - k]


P("rotate-array", "Rotate Array", "arrays", "easy",
  "Rotate the array to the right by `k` steps and return the result.",
  "rotate", ["nums", "k"], [[[1, 2, 3, 4, 5, 6, 7], 3], [[-1, -100, 3, 99], 2]], s_rotate,
  lambda r: [ints(r, 8, -9, 9), r.randint(0, 12)])


def s_move_zeroes(nums):
    nz = [x for x in nums if x != 0]
    return nz + [0] * (len(nums) - len(nz))


P("move-zeroes", "Move Zeroes", "arrays", "easy",
  "Move all zeros to the end while keeping the order of the non-zero elements. Return the new array.",
  "moveZeroes", ["nums"], [[[0, 1, 0, 3, 12]], [[0]]], s_move_zeroes, lambda r: [ints(r, 8, -2, 2)])


def s_pascal(n):
    rows = [[1]]
    for _ in range(n - 1):
        p = rows[-1]
        rows.append([1] + [p[i] + p[i + 1] for i in range(len(p) - 1)] + [1])
    return rows


P("pascals-triangle", "Pascal's Triangle", "arrays", "easy",
  "Return the first `numRows` rows of Pascal's triangle.",
  "generate", ["numRows"], [[5], [1]], s_pascal, lambda r: [r.randint(1, 10)])


def s_dup_within_k(nums, k):
    last = {}
    for i, x in enumerate(nums):
        if x in last and i - last[x] <= k:
            return True
        last[x] = i
    return False


P("contains-nearby-duplicate", "Contains Nearby Duplicate", "arrays", "easy",
  "Return `true` if there are two different indices i and j with nums[i] == nums[j] and |i - j| <= k.",
  "containsNearbyDuplicate", ["nums", "k"], [[[1, 2, 3, 1], 3], [[1, 0, 1, 1], 1]], s_dup_within_k,
  lambda r: [ints(r, 8, -3, 3), r.randint(0, 5)])


def s_spiral(m):
    res = []
    top, bottom, left, right = 0, len(m) - 1, 0, len(m[0]) - 1
    while top <= bottom and left <= right:
        for j in range(left, right + 1):
            res.append(m[top][j])
        top += 1
        for i in range(top, bottom + 1):
            res.append(m[i][right])
        right -= 1
        if top <= bottom:
            for j in range(right, left - 1, -1):
                res.append(m[bottom][j])
            bottom -= 1
        if left <= right:
            for i in range(bottom, top - 1, -1):
                res.append(m[i][left])
            left += 1
    return res


P("spiral-matrix", "Spiral Matrix", "arrays", "medium",
  "Given an m x n matrix, return all its elements in spiral order (clockwise from the top-left).",
  "spiralOrder", ["matrix"], [[[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], [[[1, 2], [3, 4]]]], s_spiral,
  lambda r: [rect(r, 4, 4, 0, 9)])

# =====================================================================
# TWO POINTERS AND SLIDING WINDOW (10)
# =====================================================================


def s_is_palindrome(s):
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]


P("valid-palindrome", "Valid Palindrome", "two_pointers", "easy",
  "Return `true` if the string reads the same forwards and backwards after removing non-alphanumeric "
  "characters and ignoring case.",
  "isPalindrome", ["s"], [["A man, a plan, a canal: Panama"], ["race a car"]], s_is_palindrome,
  lambda r: [word(r, 8, "aA b,1", 0)])


def s_two_sum_sorted(numbers, target):
    i, j = 0, len(numbers) - 1
    while i < j:
        s = numbers[i] + numbers[j]
        if s == target:
            return [i + 1, j + 1]
        if s < target:
            i += 1
        else:
            j -= 1
    return []


def g_two_sum_sorted(r):
    while True:
        nums = sorted(r.sample(range(-15, 16), r.randint(2, 8)))
        a, b = r.sample(range(len(nums)), 2)
        if a > b:
            a, b = b, a
        t = nums[a] + nums[b]
        if sum(1 for i in range(len(nums)) for j in range(i + 1, len(nums)) if nums[i] + nums[j] == t) == 1:
            return [nums, t]


P("two-sum-sorted", "Two Sum II (Sorted Array)", "two_pointers", "easy",
  "Given a sorted array `numbers` and a `target`, return the 1-based indices of the two numbers that add up to "
  "`target`. Exactly one solution exists. Use O(1) extra space.",
  "twoSumSorted", ["numbers", "target"], [[[2, 7, 11, 15], 9], [[2, 3, 4], 6]], s_two_sum_sorted, g_two_sum_sorted)


def s_three_sum(nums):
    s = sorted(nums); res = set()
    for i in range(len(s)):
        l, r = i + 1, len(s) - 1
        while l < r:
            t = s[i] + s[l] + s[r]
            if t == 0:
                res.add((s[i], s[l], s[r])); l += 1; r -= 1
            elif t < 0:
                l += 1
            else:
                r -= 1
    return [list(x) for x in sorted(res)]


P("three-sum", "3Sum", "two_pointers", "medium",
  "Return all unique triplets [a, b, c] from the array with a + b + c = 0. Each triplet is sorted, and the "
  "result is sorted.",
  "threeSum", ["nums"], [[[-1, 0, 1, 2, -1, -4]], [[0, 1, 1]]], s_three_sum,
  lambda r: [ints(r, 8, -5, 5)])


def s_max_area(height):
    i, j = 0, len(height) - 1; best = 0
    while i < j:
        best = max(best, (j - i) * min(height[i], height[j]))
        if height[i] < height[j]:
            i += 1
        else:
            j -= 1
    return best


P("container-with-most-water", "Container With Most Water", "two_pointers", "medium",
  "Given heights of vertical lines, choose two lines that together with the x-axis form a container holding "
  "the most water. Return that maximum area.",
  "maxArea", ["height"], [[[1, 8, 6, 2, 5, 4, 8, 3, 7]], [[1, 1]]], s_max_area,
  lambda r: [[r.randint(0, 9) for _ in range(r.randint(2, 8))]])


def s_unique_sorted(nums):
    return sorted(set(nums))


P("remove-duplicates-sorted", "Remove Duplicates From Sorted Array", "two_pointers", "easy",
  "Given a sorted array, return the array with duplicates removed, keeping the first occurrence of each value.",
  "removeDuplicates", ["nums"], [[[1, 1, 2]], [[0, 0, 1, 1, 1, 2, 2, 3, 3, 4]]], s_unique_sorted,
  lambda r: [sorted(r.randint(0, 6) for _ in range(r.randint(1, 9)))])


def s_length_longest_substring(s):
    last = {}; left = best = 0
    for right, c in enumerate(s):
        if c in last and last[c] >= left:
            left = last[c] + 1
        last[c] = right
        best = max(best, right - left + 1)
    return best


P("longest-substring-without-repeat", "Longest Substring Without Repeating Characters", "two_pointers", "medium",
  "Return the length of the longest substring that has no repeated characters.",
  "lengthOfLongestSubstring", ["s"], [["abcabcbb"], ["bbbbb"]], s_length_longest_substring,
  lambda r: [word(r, 10, "abc")])


def s_character_replacement(s, k):
    cnt = Counter(); l = 0; best = 0; mx = 0
    for r_, c in enumerate(s):
        cnt[c] += 1
        mx = max(mx, cnt[c])
        while (r_ - l + 1) - mx > k:
            cnt[s[l]] -= 1; l += 1
        best = max(best, r_ - l + 1)
    return best


P("longest-repeating-character-replacement", "Longest Repeating Character Replacement", "two_pointers", "medium",
  "You may change at most `k` characters in the string. Return the length of the longest substring that can "
  "become a single repeated character.",
  "characterReplacement", ["s", "k"], [["ABAB", 2], ["AABABBA", 1]], s_character_replacement,
  lambda r: [word(r, 10, "ab", 1), r.randint(0, 3)])


def s_longest_ones(nums, k):
    l = 0; zeros = 0; best = 0
    for r_, x in enumerate(nums):
        if x == 0:
            zeros += 1
        while zeros > k:
            if nums[l] == 0:
                zeros -= 1
            l += 1
        best = max(best, r_ - l + 1)
    return best


P("max-consecutive-ones-flip", "Max Consecutive Ones After K Flips", "two_pointers", "medium",
  "Given a binary array and `k`, you may flip at most `k` zeros to ones. Return the length of the longest run "
  "of ones you can get.",
  "longestOnes", ["nums", "k"], [[[1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2], [[0, 0, 1, 1, 0, 0, 1], 0]],
  s_longest_ones, lambda r: [[r.randint(0, 1) for _ in range(r.randint(1, 10))], r.randint(0, 3)])


def s_max_sliding_window(nums, k):
    dq = deque(); res = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            res.append(nums[dq[0]])
    return res


P("sliding-window-maximum", "Sliding Window Maximum", "two_pointers", "hard",
  "Given an array and a window size `k`, return the maximum value of each window of size k as it slides "
  "from left to right.",
  "maxSlidingWindow", ["nums", "k"], [[[1, 3, -1, -3, 5, 3, 6, 7], 3], [[1], 1]], s_max_sliding_window,
  lambda r: (lambda a: [a, r.randint(1, len(a))])(ints(r, 9, -9, 9)))


def s_min_subarray_len(target, nums):
    l = 0; s = 0; best = math.inf
    for r_, x in enumerate(nums):
        s += x
        while s >= target:
            best = min(best, r_ - l + 1)
            s -= nums[l]; l += 1
    return 0 if best == math.inf else best


P("minimum-size-subarray-sum", "Minimum Size Subarray Sum", "two_pointers", "medium",
  "Given positive integers, return the minimal length of a contiguous subarray whose sum is at least `target`. "
  "Return 0 if no such subarray exists.",
  "minSubArrayLen", ["target", "nums"], [[7, [2, 3, 1, 2, 4, 3]], [11, [1, 1, 1, 1, 1]]], s_min_subarray_len,
  lambda r: [r.randint(1, 10), [r.randint(1, 9) for _ in range(r.randint(1, 10))]])

# =====================================================================
# STRINGS (12)
# =====================================================================


def s_is_anagram(s, t):
    return Counter(s) == Counter(t)


P("valid-anagram", "Valid Anagram", "strings", "easy",
  "Return `true` if `t` is an anagram of `s` (same letters with the same counts), otherwise `false`.",
  "isAnagram", ["s", "t"], [["anagram", "nagaram"], ["rat", "car"]], s_is_anagram,
  lambda r: [word(r, 5, "ab"), word(r, 5, "ab")])


def s_first_uniq(s):
    c = Counter(s)
    for i, ch in enumerate(s):
        if c[ch] == 1:
            return i
    return -1


P("first-unique-character", "First Unique Character", "strings", "easy",
  "Return the index of the first character that appears exactly once. Return -1 if there is none.",
  "firstUniqChar", ["s"], [["leetcode"], ["aabb"]], s_first_uniq, lambda r: [word(r, 8, "abc")])


P("reverse-words", "Reverse Words in a String", "strings", "easy",
  "Reverse the order of the words in the string. Return the words joined by a single space, with no leading or "
  "trailing spaces.",
  "reverseWords", ["s"], [["the sky is blue"], ["  hello world  "]],
  lambda s: " ".join(reversed(s.split())),
  lambda r: [" ".join(word(r, 4, "abc", 1) for _ in range(r.randint(1, 4)))])


def s_valid_parens(s):
    pairs = {")": "(", "]": "[", "}": "{"}; st = []
    for c in s:
        if c in pairs:
            if not st or st.pop() != pairs[c]:
                return False
        else:
            st.append(c)
    return not st


P("valid-parentheses", "Valid Parentheses", "strings", "easy",
  "Given a string containing only ()[]{} characters, return `true` if the brackets are valid: every opening bracket "
  "is closed by the same type in the correct order.",
  "isValid", ["s"], [["()[]{}"], ["(]"]], s_valid_parens, lambda r: [word(r, 8, "()[]")])


ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def s_roman(s):
    total = 0
    for i, ch in enumerate(s):
        v = ROMAN[ch]
        if i + 1 < len(s) and v < ROMAN[s[i + 1]]:
            total -= v
        else:
            total += v
    return total


def to_roman(n):
    vals = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
            (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    out = ""
    for v, sym in vals:
        while n >= v:
            out += sym; n -= v
    return out


P("roman-to-integer", "Roman to Integer", "strings", "easy",
  "Convert a valid Roman numeral (from 1 to 3999) to an integer.",
  "romanToInt", ["s"], [["III"], ["MCMXCIV"]], s_roman, lambda r: [to_roman(r.randint(1, 3999))])


P("longest-common-prefix", "Longest Common Prefix", "strings", "easy",
  "Return the longest common prefix of all strings in the array. Return an empty string if there is none.",
  "longestCommonPrefix", ["strs"], [[["flower", "flow", "flight"]], [["dog", "racecar", "car"]]],
  lambda strs: os.path.commonprefix(strs),
  lambda r: (lambda base: [[base + word(r, 3, "ab") for _ in range(r.randint(1, 4))]])(word(r, 4, "ab", 1)))


P("run-length-encoding", "Run-Length Encoding", "strings", "easy",
  "Encode the string by replacing each run of equal characters with the character followed by the run length. "
  "Example: `aaab` becomes `a3b1`.",
  "encode", ["s"], [["aaabcc"], ["z"]],
  lambda s: "".join(k + str(len(list(g))) for k, g in groupby(s)),
  lambda r: [word(r, 8, "ab", 1)])


def s_pal_len(s):
    n = len(s); best = 0
    for c in range(2 * n):
        l = c // 2; r_ = l + c % 2
        while l >= 0 and r_ < n and s[l] == s[r_]:
            l -= 1; r_ += 1
        best = max(best, r_ - l - 1)
    return best


P("longest-palindromic-substring-length", "Longest Palindromic Substring (Length)", "strings", "medium",
  "Return the length of the longest palindromic substring of `s`.",
  "longestPalindrome", ["s"], [["babad"], ["cbbd"]], s_pal_len, lambda r: [word(r, 8, "abc", 1)])


def s_count_pal(s):
    n = len(s); total = 0
    for c in range(2 * n):
        l = c // 2; r_ = l + c % 2
        while l >= 0 and r_ < n and s[l] == s[r_]:
            total += 1; l -= 1; r_ += 1
    return total


P("count-palindromic-substrings", "Palindromic Substrings", "strings", "medium",
  "Count how many substrings of `s` are palindromes. Count each occurrence separately.",
  "countSubstrings", ["s"], [["abc"], ["aaa"]], s_count_pal, lambda r: [word(r, 7, "ab", 1)])


def s_isomorphic(s, t):
    if len(s) != len(t):
        return False
    m1, m2 = {}, {}
    for a, b in zip(s, t):
        if m1.get(a, b) != b or m2.get(b, a) != a:
            return False
        m1[a] = b; m2[b] = a
    return True


def g_isomorphic(r):
    s = word(r, 5, "abc", 1)
    return [s, "".join(r.choice("xyz") for _ in s)]


P("isomorphic-strings", "Isomorphic Strings", "strings", "easy",
  "Two strings are isomorphic if the characters in s can be replaced one-to-one to get t. Return `true` if they are "
  "isomorphic.",
  "isIsomorphic", ["s", "t"], [["egg", "add"], ["foo", "bar"]], s_isomorphic, g_isomorphic)


def s_valid_pal_one(s):
    def ok(i, j):
        while i < j:
            if s[i] != s[j]:
                return False
            i += 1; j -= 1
        return True
    i, j = 0, len(s) - 1
    while i < j:
        if s[i] != s[j]:
            return ok(i + 1, j) or ok(i, j - 1)
        i += 1; j -= 1
    return True


P("valid-palindrome-one-deletion", "Valid Palindrome II", "strings", "easy",
  "Return `true` if the string can become a palindrome after deleting at most one character.",
  "validPalindrome", ["s"], [["aba"], ["abca"]], s_valid_pal_one, lambda r: [word(r, 7, "ab", 1)])


def s_is_subseq(s, t):
    it = iter(t)
    return all(c in it for c in s)


P("is-subsequence", "Is Subsequence", "strings", "easy",
  "Return `true` if `s` is a subsequence of `t` (characters appear in the same order, not necessarily next to each "
  "other).",
  "isSubsequence", ["s", "t"], [["abc", "ahbgdc"], ["axc", "ahbgdc"]], s_is_subseq,
  lambda r: [word(r, 3, "abc"), word(r, 8, "abc")])

# =====================================================================
# STACK AND QUEUE (8)
# =====================================================================


def s_next_greater(nums):
    res = [-1] * len(nums); st = []
    for i, x in enumerate(nums):
        while st and nums[st[-1]] < x:
            res[st.pop()] = x
        st.append(i)
    return res


P("next-greater-element", "Next Greater Element", "stack", "medium",
  "For each element, return the first greater value to its right in the array. Return -1 if there is none.",
  "nextGreater", ["nums"], [[[2, 1, 2, 4, 3]], [[1, 3, 2]]], s_next_greater, lambda r: [ints(r, 8, -5, 5)])


def s_daily_temps(temps):
    res = [0] * len(temps); st = []
    for i, t in enumerate(temps):
        while st and temps[st[-1]] < t:
            j = st.pop(); res[j] = i - j
        st.append(i)
    return res


P("daily-temperatures", "Daily Temperatures", "stack", "medium",
  "For each day, return how many days you must wait for a warmer temperature. Use 0 if there is none.",
  "dailyTemperatures", ["temperatures"], [[[73, 74, 75, 71, 69, 72, 76, 73]], [[30, 40, 50, 60]]],
  s_daily_temps, lambda r: [ints(r, 8, 30, 40)])


def s_largest_rect(heights):
    hs = heights + [0]; st = []; best = 0
    for i, h in enumerate(hs):
        while st and hs[st[-1]] >= h:
            top = st.pop()
            left = st[-1] if st else -1
            best = max(best, hs[top] * (i - left - 1))
        st.append(i)
    return best


P("largest-rectangle-histogram", "Largest Rectangle in Histogram", "stack", "hard",
  "Given bar heights, return the area of the largest rectangle that fits entirely inside the histogram.",
  "largestRectangleArea", ["heights"], [[[2, 1, 5, 6, 2, 3]], [[2, 4]]], s_largest_rect,
  lambda r: [ints(r, 8, 0, 6)])


def s_rpn(tokens):
    st = []
    for t in tokens:
        if t in "+-*" and len(t) == 1:
            b, a = st.pop(), st.pop()
            st.append(a + b if t == "+" else a - b if t == "-" else a * b)
        else:
            st.append(int(t))
    return st[-1]


def g_rpn(r):
    nums = [str(r.randint(-9, 9)) for _ in range(r.randint(1, 5))]
    ops = [r.choice("+-*") for _ in range(len(nums) - 1)]
    return [nums + ops]


P("evaluate-reverse-polish", "Evaluate Reverse Polish Notation", "stack", "medium",
  "Evaluate an expression written in Reverse Polish Notation. Tokens are integers or one of + - *.",
  "evalRPN", ["tokens"], [[["2", "1", "+", "3", "*"]], [["4", "13", "5", "*", "+"]]], s_rpn, g_rpn)


def s_backspace(s, t):
    def build_(x):
        out = []
        for c in x:
            if c == "#":
                if out:
                    out.pop()
            else:
                out.append(c)
        return out
    return build_(s) == build_(t)


P("backspace-string-compare", "Backspace String Compare", "stack", "easy",
  "Each `#` means a backspace. Return `true` if the two strings are equal after applying all backspaces.",
  "backspaceCompare", ["s", "t"], [["ab#c", "ad#c"], ["a#c", "b"]], s_backspace,
  lambda r: [word(r, 6, "ab#", 1), word(r, 6, "ab#", 1)])


def s_asteroids(asteroids):
    st = []
    for a in asteroids:
        alive = True
        while alive and a < 0 and st and st[-1] > 0:
            if st[-1] < -a:
                st.pop()
            elif st[-1] == -a:
                st.pop(); alive = False
            else:
                alive = False
        if alive:
            st.append(a)
    return st


P("asteroid-collision", "Asteroid Collision", "stack", "medium",
  "Asteroids move at the same speed. Positive values move right, negative values move left. When two meet, the "
  "smaller one explodes (equal sizes both explode). Return the asteroids that remain.",
  "asteroidCollision", ["asteroids"], [[[5, 10, -5]], [[8, -8]], [[10, 2, -5]]], s_asteroids,
  lambda r: [[r.choice([-4, -3, -2, -1, 1, 2, 3, 4]) for _ in range(r.randint(1, 7))]])


def s_decode(s):
    cur = ""; num = 0; st = []
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch == "[":
            st.append((cur, num)); cur = ""; num = 0
        elif ch == "]":
            prev, k = st.pop(); cur = prev + cur * k
        else:
            cur += ch
    return cur


def g_decode(r):
    return ["%d[%s]%s" % (r.randint(1, 3), word(r, 3, "abc", 1), word(r, 2, "xyz"))]


P("decode-string", "Decode String", "stack", "medium",
  "Decode an encoded string like `3[a]2[bc]`, which means repeat the bracketed content k times. Return the decoded "
  "string.",
  "decodeString", ["s"], [["3[a]2[bc]"], ["3[a2[c]]"]], s_decode, g_decode)


def s_simplify(path):
    st = []
    for p in path.split("/"):
        if p in ("", "."):
            continue
        if p == "..":
            if st:
                st.pop()
        else:
            st.append(p)
    return "/" + "/".join(st)


P("simplify-unix-path", "Simplify Path", "stack", "medium",
  "Given an absolute Unix path, return the canonical path. Treat `.` as the current folder and `..` as the parent "
  "folder.",
  "simplifyPath", ["path"], [["/home/"], ["/a/./b/../../c/"]], s_simplify,
  lambda r: ["/" + "/".join(r.choice(["a", "b", "..", ".", ""]) for _ in range(r.randint(1, 6)))])

# =====================================================================
# LINKED LIST (7)  -- input is the node values in order
# =====================================================================
P("reverse-linked-list", "Reverse Linked List", "linked_list", "easy",
  "The input gives the values of a singly linked list in order. Reverse the list and return the values in the new "
  "order.",
  "reverseList", ["values"], [[[1, 2, 3, 4, 5]], [[1, 2]]], lambda v: v[::-1],
  lambda r: [ints(r, 8, 0, 9)])

P("middle-of-linked-list", "Middle of the Linked List", "linked_list", "easy",
  "Return the values from the middle node to the end. If there are two middle nodes, start from the second one.",
  "middleNode", ["values"], [[[1, 2, 3, 4, 5]], [[1, 2, 3, 4, 5, 6]]], lambda v: v[len(v) // 2:],
  lambda r: [list(range(1, r.randint(1, 9) + 1))])


def s_remove_nth(v, n):
    idx = len(v) - n
    return v[:idx] + v[idx + 1:]


P("remove-nth-node-from-end", "Remove Nth Node From End", "linked_list", "medium",
  "Remove the n-th node from the end of the list. Return the remaining values in order.",
  "removeNthFromEnd", ["values", "n"], [[[1, 2, 3, 4, 5], 2], [[1], 1]], s_remove_nth,
  lambda r: (lambda v: [v, r.randint(1, len(v))])(list(range(1, r.randint(1, 8) + 1))))

P("merge-two-sorted-lists", "Merge Two Sorted Lists", "linked_list", "easy",
  "Two sorted lists are given as arrays of values. Merge them into one sorted list and return it.",
  "mergeTwoLists", ["list1", "list2"], [[[1, 2, 4], [1, 3, 4]], [[], [0]]], lambda a, b: sorted(a + b),
  lambda r: [sorted(ints(r, 5, 0, 9, 0)), sorted(ints(r, 5, 0, 9, 0))])

P("palindrome-linked-list", "Palindrome Linked List", "linked_list", "easy",
  "Return `true` if the values of the linked list read the same forwards and backwards.",
  "isPalindromeList", ["values"], [[[1, 2, 2, 1]], [[1, 2]]], lambda v: v == v[::-1],
  lambda r: [[r.randint(0, 2) for _ in range(r.randint(0, 6))]])

P("remove-linked-list-elements", "Remove Linked List Elements", "linked_list", "easy",
  "Remove every node whose value equals `val`. Return the remaining values in order.",
  "removeElements", ["values", "val"], [[[1, 2, 6, 3, 4, 5, 6], 6], [[7, 7], 7]],
  lambda v, val: [x for x in v if x != val], lambda r: [ints(r, 8, 0, 4), r.randint(0, 4)])


def s_reorder(v):
    out = []; i, j = 0, len(v) - 1
    while i <= j:
        out.append(v[i])
        if i != j:
            out.append(v[j])
        i += 1; j -= 1
    return out


P("reorder-linked-list", "Reorder List", "linked_list", "medium",
  "Reorder the list from L0 to Ln to L1 to Ln-1 to L2 to Ln-2 and so on. Return the new order of values.",
  "reorderList", ["values"], [[[1, 2, 3, 4]], [[1, 2, 3, 4, 5]]], s_reorder,
  lambda r: [list(range(1, r.randint(1, 8) + 1))])

# =====================================================================
# TREES (9)  -- input is level-order array, null = missing node
# =====================================================================


def s_max_depth(a):
    def d(n):
        return 0 if not n else 1 + max(d(n.left), d(n.right))
    return d(build(a))


P("maximum-depth-of-binary-tree", "Maximum Depth of Binary Tree", "trees", "easy",
  "Given a binary tree in level-order (null means no node), return its maximum depth.",
  "maxDepth", ["root"], [[[3, 9, 20, None, None, 15, 7]], [[1, None, 2]]], s_max_depth,
  lambda r: [gtree(r)])


def s_invert(a):
    def inv(n):
        if n is None:
            return None
        n.left, n.right = inv(n.right), inv(n.left)
        return n
    return ser(inv(build(a)))


P("invert-binary-tree", "Invert Binary Tree", "trees", "easy",
  "Mirror the binary tree by swapping every node's left and right children. Return the new tree in level-order "
  "(trailing nulls removed).",
  "invertTree", ["root"], [[[4, 2, 7, 1, 3, 6, 9]], [[2, 1, 3]]], s_invert, lambda r: [gtree(r)])


def s_inorder(a):
    def f(n):
        return f(n.left) + [n.val] + f(n.right) if n else []
    return f(build(a))


P("binary-tree-inorder", "Binary Tree Inorder Traversal", "trees", "easy",
  "Return the inorder traversal (left, root, right) of the binary tree given in level-order.",
  "inorderTraversal", ["root"], [[[1, None, 2, 3]], [[1, 2, 3, 4, 5]]], s_inorder, lambda r: [gtree(r)])


def s_level_order(a):
    root = build(a); res = []; q = deque([root] if root else [])
    while q:
        level = []
        for _ in range(len(q)):
            n = q.popleft(); level.append(n.val)
            if n.left: q.append(n.left)
            if n.right: q.append(n.right)
        res.append(level)
    return res


P("binary-tree-level-order", "Binary Tree Level Order Traversal", "trees", "medium",
  "Return the values of the tree grouped by level, from top to bottom and left to right.",
  "levelOrder", ["root"], [[[3, 9, 20, None, None, 15, 7]], [[1]]], s_level_order, lambda r: [gtree(r)])


def s_path_sum(a, target):
    def f(n, s):
        if not n:
            return False
        s += n.val
        if not n.left and not n.right:
            return s == target
        return f(n.left, s) or f(n.right, s)
    return f(build(a), 0)


P("path-sum", "Path Sum", "trees", "easy",
  "Return `true` if the tree has a root-to-leaf path whose values add up to `targetSum`.",
  "hasPathSum", ["root", "targetSum"], [[[5, 4, 8, 11, None, 13, 4], 22], [[1, 2], 1]], s_path_sum,
  lambda r: [gtree(r), r.randint(0, 20)])


def s_lca_bst(a, p, q):
    root = build(a)
    while root:
        if p < root.val and q < root.val:
            root = root.left
        elif p > root.val and q > root.val:
            root = root.right
        else:
            return root.val
    return None


def g_lca_bst(r):
    vals = r.sample(range(1, 20), r.randint(3, 7)); root = None
    for v in vals:
        root = ins(root, v)
    return [ser(root), r.choice(vals), r.choice(vals)]


P("lowest-common-ancestor-bst", "Lowest Common Ancestor of a BST", "trees", "medium",
  "Given a binary search tree (level-order) and two node values p and q that exist in it, return the lowest common "
  "ancestor value.",
  "lowestCommonAncestor", ["root", "p", "q"], [[[6, 2, 8, 0, 4, 7, 9], 2, 8], [[6, 2, 8, 0, 4, 7, 9], 2, 4]],
  s_lca_bst, g_lca_bst)


def s_diameter(a):
    best = [0]
    def h(n):
        if not n:
            return 0
        l, r_ = h(n.left), h(n.right)
        best[0] = max(best[0], l + r_)
        return 1 + max(l, r_)
    h(build(a))
    return best[0]


P("diameter-of-binary-tree", "Diameter of Binary Tree", "trees", "medium",
  "Return the length (number of edges) of the longest path between any two nodes in the tree.",
  "diameterOfBinaryTree", ["root"], [[[1, 2, 3, 4, 5]], [[1, 2]]], s_diameter, lambda r: [gtree(r)])


def s_right_view_real(a):
    root = build(a); res = []; q = deque([root] if root else [])
    while q:
        size = len(q)
        for i in range(size):
            n = q.popleft()
            if i == size - 1:
                res.append(n.val)
            if n.left: q.append(n.left)
            if n.right: q.append(n.right)
    return res


P("binary-tree-right-side-view", "Binary Tree Right Side View", "trees", "medium",
  "Return the values you would see when looking at the tree from the right side, from top to bottom.",
  "rightSideView", ["root"], [[[1, 2, 3, None, 5, None, 4]], [[1, None, 3]]], s_right_view_real,
  lambda r: [gtree(r)])

def s_symmetric(a):
    root = build(a)
    if root is None:
        return True
    def mirror(x, y):
        if x is None and y is None:
            return True
        if x is None or y is None:
            return False
        return x.val == y.val and mirror(x.left, y.right) and mirror(x.right, y.left)
    return mirror(root.left, root.right)


P("symmetric-tree", "Symmetric Tree", "trees", "easy",
  "Given a binary tree in level-order, return `true` if it is a mirror of itself around its center.",
  "isSymmetric", ["root"], [[[1, 2, 2, 3, 4, 4, 3]], [[1, 2, 2, None, 3, None, 3]]], s_symmetric,
  lambda r: [[r.randint(0, 2) for _ in range(r.randint(1, 7))]])


# =====================================================================
# GRAPHS (8)
# =====================================================================


def s_islands(grid):
    g = [list(row) for row in grid]; R = len(g); C = len(g[0]); cnt = 0
    for i in range(R):
        for j in range(C):
            if g[i][j] == "1":
                cnt += 1; st = [(i, j)]; g[i][j] = "0"
                while st:
                    x, y = st.pop()
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < R and 0 <= ny < C and g[nx][ny] == "1":
                            g[nx][ny] = "0"; st.append((nx, ny))
    return cnt


P("number-of-islands", "Number of Islands", "graphs", "medium",
  "Given a grid of '1' (land) and '0' (water), count the islands. An island is connected land horizontally or "
  "vertically.",
  "numIslands", ["grid"], [[[["1", "1", "0"], ["1", "0", "0"], ["0", "0", "1"]]]], s_islands,
  lambda r: [grid01(r)])


def s_flood(image, sr, sc, color):
    orig = image[sr][sc]
    if orig == color:
        return image
    img = [row[:] for row in image]; st = [(sr, sc)]; img[sr][sc] = color
    while st:
        x, y = st.pop()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(img) and 0 <= ny < len(img[0]) and img[nx][ny] == orig:
                img[nx][ny] = color; st.append((nx, ny))
    return img


def g_flood(r):
    img = rect(r, 4, 4, 0, 2)
    return [img, r.randint(0, len(img) - 1), r.randint(0, len(img[0]) - 1), r.randint(0, 3)]


P("flood-fill", "Flood Fill", "graphs", "easy",
  "Starting at pixel (sr, sc), change the color of every pixel connected to it (up, down, left, right) that has the "
  "same original color to `color`. Return the image.",
  "floodFill", ["image", "sr", "sc", "color"], [[[[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2]], s_flood, g_flood)


def adj_from_edges(n, edges):
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b); g[b].append(a)
    return g


def g_edges(r, n_max=6):
    n = r.randint(2, n_max)
    edges = []
    for _ in range(r.randint(0, n + 1)):
        a, b = r.sample(range(n), 2)
        edges.append([a, b])
    return n, edges


def s_components(n, edges):
    seen = [False] * n; cnt = 0; g = adj_from_edges(n, edges)
    for s in range(n):
        if not seen[s]:
            cnt += 1; st = [s]; seen[s] = True
            while st:
                x = st.pop()
                for y in g[x]:
                    if not seen[y]:
                        seen[y] = True; st.append(y)
    return cnt


P("number-of-connected-components", "Number of Connected Components", "graphs", "medium",
  "An undirected graph has n nodes (0 to n-1) and an edge list. Return the number of connected components.",
  "countComponents", ["n", "edges"], [[5, [[0, 1], [1, 2], [3, 4]]], [4, [[0, 1], [2, 3], [1, 2]]]], s_components,
  lambda r: list(g_edges(r)))


def s_valid_path(n, edges, src, dst):
    g = adj_from_edges(n, edges); seen = {src}; st = [src]
    while st:
        x = st.pop()
        for y in g[x]:
            if y not in seen:
                seen.add(y); st.append(y)
    return dst in seen


def g_valid_path(r):
    n, edges = g_edges(r)
    return [n, edges, r.randint(0, n - 1), r.randint(0, n - 1)]


P("valid-path-in-graph", "Find if Path Exists", "graphs", "easy",
  "Given an undirected graph with n nodes and edges, return `true` if there is a path from `source` to "
  "`destination`.",
  "validPath", ["n", "edges", "source", "destination"], [[3, [[0, 1], [1, 2], [2, 0]], 0, 2]], s_valid_path,
  g_valid_path)


def s_can_finish(n, prereqs):
    indeg = [0] * n; g = [[] for _ in range(n)]
    for a, b in prereqs:
        g[b].append(a); indeg[a] += 1
    q = deque([i for i in range(n) if indeg[i] == 0]); done = 0
    while q:
        x = q.popleft(); done += 1
        for y in g[x]:
            indeg[y] -= 1
            if indeg[y] == 0:
                q.append(y)
    return done == n


def g_can_finish(r):
    n = r.randint(1, 6)
    pre = []
    for _ in range(r.randint(0, 6)):
        if n >= 2:
            a, b = r.sample(range(n), 2); pre.append([a, b])
    return [n, pre]


P("course-schedule", "Course Schedule", "graphs", "medium",
  "There are n courses (0 to n-1). A pair [a, b] means you must take b before a. Return `true` if you can finish "
  "all courses.",
  "canFinish", ["numCourses", "prerequisites"], [[2, [[1, 0]]], [2, [[1, 0], [0, 1]]]], s_can_finish, g_can_finish)


def s_shortest(n, edges, src, dst):
    g = adj_from_edges(n, edges); dist = {src: 0}; q = deque([src])
    while q:
        x = q.popleft()
        for y in g[x]:
            if y not in dist:
                dist[y] = dist[x] + 1; q.append(y)
    return dist.get(dst, -1)


def g_shortest(r):
    n, edges = g_edges(r)
    return [n, edges, r.randint(0, n - 1), r.randint(0, n - 1)]


P("shortest-path-unweighted", "Shortest Path in Unweighted Graph", "graphs", "easy",
  "Return the minimum number of edges on a path from `source` to `destination` in an undirected graph, or -1 if "
  "no path exists.",
  "shortestPath", ["n", "edges", "source", "destination"], [[4, [[0, 1], [1, 2], [2, 3]], 0, 3]], s_shortest,
  g_shortest)


def s_rotting(grid):
    g = [row[:] for row in grid]; R, C = len(g), len(g[0]); q = deque(); fresh = 0
    for i in range(R):
        for j in range(C):
            if g[i][j] == 2: q.append((i, j, 0))
            elif g[i][j] == 1: fresh += 1
    t = 0
    while q:
        x, y, d = q.popleft(); t = max(t, d)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < R and 0 <= ny < C and g[nx][ny] == 1:
                g[nx][ny] = 2; fresh -= 1; q.append((nx, ny, d + 1))
    return -1 if fresh else t


P("rotting-oranges", "Rotting Oranges", "graphs", "medium",
  "Grid cells: 0 empty, 1 fresh orange, 2 rotten orange. Each minute rotten oranges rot their 4-directional fresh "
  "neighbours. Return the minimum minutes until no fresh orange remains, or -1 if impossible.",
  "orangesRotting", ["grid"], [[[[2, 1, 1], [1, 1, 0], [0, 1, 1]]], [[[2, 1, 1], [0, 1, 1], [1, 0, 1]]]],
  s_rotting, lambda r: [rect(r, 4, 4, 0, 2)])


def s_bipartite(graph):
    color = [-1] * len(graph)
    for s in range(len(graph)):
        if color[s] != -1:
            continue
        color[s] = 0; q = deque([s])
        while q:
            x = q.popleft()
            for y in graph[x]:
                if color[y] == -1:
                    color[y] = 1 - color[x]; q.append(y)
                elif color[y] == color[x]:
                    return False
    return True


def g_bipartite(r):
    n = r.randint(1, 6)
    edges = []
    for _ in range(r.randint(0, 7)):
        if n >= 2:
            a, b = r.sample(range(n), 2); edges.append([a, b])
    return [adj_from_edges(n, edges)]


P("is-graph-bipartite", "Is Graph Bipartite", "graphs", "medium",
  "Given an undirected graph as an adjacency list, return `true` if its nodes can be split into two groups so that "
  "every edge connects nodes from different groups.",
  "isBipartite", ["graph"], [[[[1, 3], [0, 2], [1, 3], [0, 2]]], [[[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]]],
  s_bipartite, g_bipartite)

# =====================================================================
# BINARY SEARCH (7)
# =====================================================================


def s_bsearch(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


P("binary-search", "Binary Search", "binary_search", "easy",
  "Given a sorted array of distinct integers and a target, return its index, or -1 if it is not present. Must run "
  "in O(log n).",
  "search", ["nums", "target"], [[[-1, 0, 3, 5, 9, 12], 9], [[-1, 0, 3, 5, 9, 12], 2]], s_bsearch,
  lambda r: (lambda a: [a, r.choice(a) if r.random() < 0.7 else r.randint(-20, 20)])(sorted_distinct(r, 8, -20, 20)))


def s_first_bad(n, bad):
    lo, hi = 1, n
    while lo < hi:
        mid = (lo + hi) // 2
        if mid >= bad:
            hi = mid
        else:
            lo = mid + 1
    return lo


P("first-bad-version", "First Bad Version", "binary_search", "easy",
  "Versions 1 to n exist. Every version from the first bad one onward is bad. Return the first bad version. Minimize "
  "calls, use binary search.",
  "firstBadVersion", ["n", "bad"], [[5, 4], [1, 1]], s_first_bad,
  lambda r: (lambda n: [n, r.randint(1, n)])(r.randint(1, 20)))


P("search-insert-position", "Search Insert Position", "binary_search", "easy",
  "Given a sorted array of distinct integers and a target, return the index where the target is or should be "
  "inserted to keep the array sorted.",
  "searchInsert", ["nums", "target"], [[[1, 3, 5, 6], 5], [[1, 3, 5, 6], 2]],
  lambda nums, t: bisect.bisect_left(nums, t),
  lambda r: [sorted_distinct(r, 8, 0, 40), r.randint(0, 40)])


P("integer-square-root", "Square Root (Floor)", "binary_search", "easy",
  "Return the integer part of the square root of a non-negative integer x, without using the power operator.",
  "mySqrt", ["x"], [[8], [16]], math.isqrt, lambda r: [r.randint(0, 10000)])


def s_find_min(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return nums[lo]


def g_find_min(r):
    arr = sorted_distinct(r, 8, -20, 20)
    k = r.randint(0, len(arr) - 1)
    return [arr[k:] + arr[:k]]


P("find-min-rotated-sorted", "Find Minimum in Rotated Sorted Array", "binary_search", "medium",
  "A sorted array of distinct integers was rotated between 1 and n times. Return the minimum element. Must run in "
  "O(log n).",
  "findMin", ["nums"], [[[3, 4, 5, 1, 2]], [[4, 5, 6, 7, 0, 1, 2]]], s_find_min, g_find_min)


def s_koko(piles, h):
    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if sum(-(-p // mid) for p in piles) <= h:
            hi = mid
        else:
            lo = mid + 1
    return lo


P("koko-eating-bananas", "Koko Eating Bananas", "binary_search", "medium",
  "Koko eats bananas at speed k per hour. Each pile is eaten in one go, taking ceil(pile / k) hours. Return the "
  "minimum integer speed k so that she finishes within h hours.",
  "minEatingSpeed", ["piles", "h"], [[[3, 6, 7, 11], 8], [[30, 11, 23, 4, 20], 5]], s_koko,
  lambda r: (lambda p: [p, r.randint(len(p), len(p) + 10)])([r.randint(1, 20) for _ in range(r.randint(1, 6))]))


def s_search_matrix(matrix, target):
    R = len(matrix); C = len(matrix[0]); lo, hi = 0, R * C - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        v = matrix[mid // C][mid % C]
        if v == target:
            return True
        if v < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


def g_search_matrix(r):
    R, C = r.randint(1, 4), r.randint(1, 4)
    vals = sorted(r.sample(range(0, 30), R * C))
    m = [vals[i * C:(i + 1) * C] for i in range(R)]
    return [m, r.choice(vals) if r.random() < 0.6 else r.randint(0, 30)]


P("search-2d-matrix", "Search a 2D Matrix", "binary_search", "medium",
  "Each row is sorted, and the first number of each row is greater than the last number of the previous row. "
  "Return `true` if the target exists in the matrix.",
  "searchMatrix", ["matrix", "target"], [[[[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3]],
  s_search_matrix, g_search_matrix)

# =====================================================================
# DYNAMIC PROGRAMMING (12)
# =====================================================================
def s_climb(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


P("climbing-stairs", "Climbing Stairs", "dp", "easy",
  "You can climb 1 or 2 steps at a time. Return the number of distinct ways to reach the top of an n-step staircase.",
  "climbStairs", ["n"], [[5], [2]], s_climb,
  lambda r: [r.randint(1, 30)])


def s_rob(nums):
    prev = cur = 0
    for x in nums:
        prev, cur = cur, max(cur, prev + x)
    return cur


P("house-robber", "House Robber", "dp", "medium",
  "You cannot rob two adjacent houses. Given the money in each house, return the maximum amount you can rob.",
  "rob", ["nums"], [[[1, 2, 3, 1]], [[2, 7, 9, 3, 1]]], s_rob, lambda r: [ints(r, 8, 0, 20)])


def s_min_cost(cost):
    p2, p1 = cost[0], cost[1]
    for i in range(2, len(cost)):
        p2, p1 = p1, cost[i] + min(p2, p1)
    return min(p2, p1)


P("min-cost-climbing-stairs", "Min Cost Climbing Stairs", "dp", "easy",
  "Each step has a cost. You may start at step 0 or step 1 and climb 1 or 2 steps at a time. Return the minimum cost "
  "to reach the top (one past the last step).",
  "minCostClimbingStairs", ["cost"], [[[10, 15, 20]], [[1, 100, 1, 1, 1, 100, 1, 1, 100, 1]]], s_min_cost,
  lambda r: [ints(r, 8, 0, 9, 2)])


def s_coin_change(coins, amount):
    INF = amount + 1; dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] < INF else -1


P("coin-change", "Coin Change", "dp", "medium",
  "Given coin denominations and an amount, return the fewest coins needed to make the amount, or -1 if impossible. "
  "Coins can be used unlimited times.",
  "coinChange", ["coins", "amount"], [[[1, 2, 5], 11], [[2], 3]], s_coin_change,
  lambda r: [r.sample(range(1, 8), r.randint(1, 3)), r.randint(0, 15)])


def s_lis(nums):
    tails = []
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)


P("longest-increasing-subsequence", "Longest Increasing Subsequence", "dp", "hard",
  "Return the length of the longest strictly increasing subsequence of the array. The subsequence need not be "
  "contiguous.",
  "lengthOfLIS", ["nums"], [[[10, 9, 2, 5, 3, 7, 101, 18]], [[0, 1, 0, 3, 2, 3]]], s_lis,
  lambda r: [ints(r, 8, -5, 9)])


def s_max_sub(nums):
    cur = best = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best


P("maximum-subarray", "Maximum Subarray", "dp", "medium",
  "Return the largest possible sum of a contiguous, non-empty subarray.",
  "maxSubArray", ["nums"], [[[-2, 1, -3, 4, -1, 2, 1, -5, 4]], [[1]]], s_max_sub, lambda r: [ints(r, 8, -9, 9)])


P("unique-paths", "Unique Paths", "dp", "medium",
  "A robot starts at the top-left of an m x n grid and can move only right or down. Return the number of paths to "
  "the bottom-right corner.",
  "uniquePaths", ["m", "n"], [[3, 7], [3, 2]], lambda m, n: math.comb(m + n - 2, m - 1),
  lambda r: [r.randint(1, 8), r.randint(1, 8)])


def s_lcs(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            dp[i][j] = dp[i - 1][j - 1] + 1 if a[i - 1] == b[j - 1] else max(dp[i - 1][j], dp[i][j - 1])
    return dp[-1][-1]


P("longest-common-subsequence", "Longest Common Subsequence", "dp", "hard",
  "Return the length of the longest subsequence common to both strings.",
  "longestCommonSubsequence", ["text1", "text2"], [["abcde", "ace"], ["abc", "def"]], s_lcs,
  lambda r: [word(r, 6, "abc"), word(r, 6, "abc")])


def s_edit(a, b):
    m, n = len(a), len(b); dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[0]; dp[0] = i
        for j in range(1, n + 1):
            tmp = dp[j]
            dp[j] = prev if a[i - 1] == b[j - 1] else 1 + min(prev, dp[j], dp[j - 1])
            prev = tmp
    return dp[n]


P("edit-distance", "Edit Distance", "dp", "hard",
  "Return the minimum number of insertions, deletions or replacements of single characters needed to turn word1 "
  "into word2.",
  "minDistance", ["word1", "word2"], [["horse", "ros"], ["intention", "execution"]], s_edit,
  lambda r: [word(r, 5, "abc"), word(r, 5, "abc")])


def s_word_break(s, words):
    ok = [False] * (len(s) + 1); ok[0] = True
    for i in range(1, len(s) + 1):
        ok[i] = any(ok[i - len(w)] and s[i - len(w):i] == w for w in words if len(w) <= i)
    return ok[len(s)]


P("word-break", "Word Break", "dp", "medium",
  "Return `true` if the string can be split into a sequence of one or more words from the dictionary `wordDict`. "
  "Words can be reused.",
  "wordBreak", ["s", "wordDict"], [["leetcode", ["leet", "code"]], ["catsandog", ["cats", "dog", "sand", "and", "cat"]]],
  s_word_break, lambda r: [word(r, 8, "ab"), [word(r, 3, "ab", 1) for _ in range(r.randint(1, 4))]])


def s_decode_ways(s):
    p2, p1 = 1, 0 if s[0] == "0" else 1
    for i in range(1, len(s)):
        cur = 0
        if s[i] != "0":
            cur += p1
        two = int(s[i - 1:i + 1])
        if 10 <= two <= 26:
            cur += p2
        p2, p1 = p1, cur
    return p1


P("decode-ways", "Decode Ways", "dp", "medium",
  "A message of digits maps to letters: 1 to A ... 26 to Z. Return the number of ways to decode the digit string.",
  "numDecodings", ["s"], [["12"], ["226"]], s_decode_ways,
  lambda r: ["".join(r.choice("0123456789") for _ in range(r.randint(1, 8)))])


def s_partition(nums):
    total = sum(nums)
    if total % 2:
        return False
    reach = {0}
    for x in nums:
        reach |= {v + x for v in reach}
    return total // 2 in reach


P("partition-equal-subset-sum", "Partition Equal Subset Sum", "dp", "hard",
  "Return `true` if the array can be split into two subsets with equal sums.",
  "canPartition", ["nums"], [[[1, 5, 11, 5]], [[1, 2, 3, 5]]], s_partition, lambda r: [ints(r, 6, 1, 9)])

# =====================================================================
# HEAP, INTERVALS AND GREEDY (11)
# =====================================================================


def s_kth_largest(nums, k):
    return sorted(nums, reverse=True)[k - 1]


P("kth-largest-element", "Kth Largest Element in an Array", "heap_greedy", "medium",
  "Return the k-th largest element in the array (counting duplicates as separate elements).",
  "findKthLargest", ["nums", "k"], [[[3, 2, 1, 5, 6, 4], 2], [[3, 2, 3, 1, 2, 4, 5, 5, 6], 4]],
  s_kth_largest, lambda r: (lambda a: [a, r.randint(1, len(a))])(ints(r, 8, -9, 9)))


def s_last_stone(stones):
    h = [-s for s in stones]; heapq.heapify(h)
    while len(h) > 1:
        x = -heapq.heappop(h); y = -heapq.heappop(h)
        if x != y:
            heapq.heappush(h, -(x - y))
    return -h[0] if h else 0


P("last-stone-weight", "Last Stone Weight", "heap_greedy", "easy",
  "Repeatedly smash the two heaviest stones. If they are equal both vanish, otherwise the lighter one is removed and "
  "the heavier one becomes their difference. Return the weight of the last stone, or 0.",
  "lastStoneWeight", ["stones"], [[[2, 7, 4, 1, 8, 1]], [[1]]], s_last_stone, lambda r: [ints(r, 6, 1, 9)])


def s_merge(intervals_):
    out = []
    for s, e in sorted(intervals_):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


P("merge-intervals", "Merge Intervals", "heap_greedy", "medium",
  "Given intervals [start, end], merge all overlapping intervals and return the merged list sorted by start.",
  "merge", ["intervals"], [[[[1, 3], [2, 6], [8, 10], [15, 18]]], [[[1, 4], [4, 5]]]], s_merge,
  lambda r: [intervals(r)])


def s_insert(intervals_, new):
    res = []; i = 0; n = len(intervals_)
    while i < n and intervals_[i][1] < new[0]:
        res.append(intervals_[i]); i += 1
    while i < n and intervals_[i][0] <= new[1]:
        new = [min(new[0], intervals_[i][0]), max(new[1], intervals_[i][1])]; i += 1
    res.append(new)
    res += intervals_[i:]
    return res


def g_insert(r):
    vals = sorted(r.sample(range(0, 40), 2 * r.randint(0, 4)))
    iv = [[vals[i], vals[i + 1]] for i in range(0, len(vals), 2)]
    a = r.randint(0, 40); return [iv, [a, a + r.randint(0, 6)]]


P("insert-interval", "Insert Interval", "heap_greedy", "medium",
  "You are given non-overlapping intervals sorted by start and one new interval. Insert it and merge if needed. "
  "Return the result.",
  "insert", ["intervals", "newInterval"], [[[[1, 3], [6, 9]], [2, 5]], [[[1, 2], [3, 5], [6, 7]], [4, 8]]],
  s_insert, g_insert)


def s_erase(intervals_):
    end = None; removed = 0
    for s, e in sorted(intervals_, key=lambda x: x[1]):
        if end is None or s >= end:
            end = e
        else:
            removed += 1
    return removed


def g_iv(r):
    out = []
    for _ in range(r.randint(1, 6)):
        a = r.randint(0, 15); out.append([a, a + r.randint(1, 6)])
    return [out]


P("non-overlapping-intervals", "Minimum Intervals to Remove", "heap_greedy", "medium",
  "Return the minimum number of intervals you must remove so that the rest do not overlap. Intervals touching at an "
  "endpoint do not overlap.",
  "eraseOverlapIntervals", ["intervals"], [[[[1, 2], [2, 3], [3, 4], [1, 3]]], [[[1, 2], [1, 2], [1, 2]]]],
  s_erase, g_iv)


def s_can_attend(intervals_):
    prev_end = None
    for s, e in sorted(intervals_):
        if prev_end is not None and s < prev_end:
            return False
        prev_end = e
    return True


P("meeting-rooms", "Meeting Rooms", "heap_greedy", "easy",
  "Given meeting intervals, return `true` if one person can attend all of them (no two overlap).",
  "canAttendMeetings", ["intervals"], [[[[0, 30], [5, 10], [15, 20]]], [[[7, 10], [2, 4]]]], s_can_attend, g_iv)


def s_min_rooms(intervals_):
    starts = sorted(s for s, _ in intervals_); ends = sorted(e for _, e in intervals_)
    i = j = rooms = best = 0
    while i < len(starts):
        if starts[i] < ends[j]:
            rooms += 1; i += 1
        else:
            rooms -= 1; j += 1
        best = max(best, rooms)
    return best


P("meeting-rooms-ii", "Meeting Rooms II", "heap_greedy", "medium",
  "Given meeting intervals, return the minimum number of rooms required so that no meeting overlaps in a room.",
  "minMeetingRooms", ["intervals"], [[[[0, 30], [5, 10], [15, 20]]], [[[7, 10], [2, 4]]]], s_min_rooms, g_iv)


def s_can_jump(nums):
    reach = 0
    for i, x in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + x)
    return True


P("jump-game", "Jump Game", "heap_greedy", "medium",
  "Each value is the maximum jump length from that index. Starting at index 0, return `true` if you can reach the "
  "last index.",
  "canJump", ["nums"], [[[2, 3, 1, 1, 4]], [[3, 2, 1, 0, 4]]], s_can_jump, lambda r: [ints(r, 6, 0, 3)])


def s_jump(nums):
    jumps = end = far = 0
    for i in range(len(nums) - 1):
        far = max(far, i + nums[i])
        if i == end:
            jumps += 1; end = far
    return jumps


P("jump-game-ii", "Jump Game II", "heap_greedy", "medium",
  "Each value is the maximum jump length from that index. Return the minimum number of jumps to reach the last "
  "index. The last index is always reachable.",
  "jump", ["nums"], [[[2, 3, 1, 1, 4]], [[2, 3, 0, 1, 4]]], s_jump, lambda r: [ints(r, 7, 1, 3)])


def s_gas(gas, cost):
    total = tank = start = 0
    for i in range(len(gas)):
        d = gas[i] - cost[i]
        total += d; tank += d
        if tank < 0:
            start = i + 1; tank = 0
    return start if total >= 0 else -1


def g_gas(r):
    n = r.randint(1, 6)
    return [[r.randint(0, 5) for _ in range(n)], [r.randint(0, 5) for _ in range(n)]]


P("gas-station", "Gas Station", "heap_greedy", "medium",
  "There are n gas stations on a circular route. gas[i] is the fuel at station i and cost[i] is the fuel needed to "
  "reach the next station. Return the index you can start at to complete the circle once, or -1 if impossible.",
  "canCompleteCircuit", ["gas", "cost"], [[[1, 2, 3, 4, 5], [3, 4, 5, 1, 2]], [[2, 3, 4], [3, 4, 3]]],
  s_gas, g_gas)


def s_least_interval(tasks, n):
    counts = Counter(tasks); maxf = max(counts.values())
    num_max = sum(1 for v in counts.values() if v == maxf)
    return max(len(tasks), (maxf - 1) * (n + 1) + num_max)


P("task-scheduler", "Task Scheduler", "heap_greedy", "medium",
  "Tasks are single letters. Identical tasks need at least n units of time between them. Idle time is allowed. "
  "Return the least number of time units needed to run all tasks.",
  "leastInterval", ["tasks", "n"], [[["A", "A", "A", "B", "B", "B"], 2], [["A", "A", "A", "B", "B", "B"], 0]],
  s_least_interval, lambda r: [[r.choice("ABC") for _ in range(r.randint(1, 8))], r.randint(0, 3)])


# =====================================================================
# Validation helper and count
# =====================================================================
assert len(PROBLEMS) == len({p["slug"] for p in PROBLEMS}), "duplicate slugs"

if __name__ == "__main__":
    from collections import Counter as C_
    print("total problems:", len(PROBLEMS))
    print("by topic:", dict(C_(p["topic"] for p in PROBLEMS)))
    print("by difficulty:", dict(C_(p["difficulty"] for p in PROBLEMS)))
