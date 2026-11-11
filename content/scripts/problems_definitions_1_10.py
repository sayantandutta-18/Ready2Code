from collections import Counter, defaultdict
import random

def add_problems_1_10(register):
    # 1. Top K Frequent Elements
    def sol_topk(nums, k):
        c = Counter(nums)
        # return sorted in ascending order for deterministic output
        most = [item[0] for item in c.most_common(k)]
        return sorted(most)

    def gen_topk(rng):
        n = rng.randint(5, 30)
        vals = [rng.randint(-20, 20) for _ in range(rng.randint(2, 6))]
        nums = [rng.choice(vals) for _ in range(n)]
        unique_cnt = len(set(nums))
        k = rng.randint(1, unique_cnt)
        return [nums, k]

    register(
        slug="top-k-frequent-elements",
        title="Top K Frequent Elements",
        topic_key="arrays",
        diff="medium",
        statement="Given an integer array `nums` and an integer `k`, return the `k` most frequent elements in ascending order.",
        fn="topKFrequent",
        params=["nums", "k"],
        examples=[
            [[[1, 1, 1, 2, 2, 3], 2], [1, 2]],
            [[[1], 1], [1]]
        ],
        sol=sol_topk,
        gen=gen_topk
    )

    # 2. Find All Duplicates in an Array
    def sol_duplicates(nums):
        c = Counter(nums)
        return sorted([k for k, v in c.items() if v == 2])

    def gen_duplicates(rng):
        n = rng.randint(3, 20)
        nums = list(range(1, n + 1))
        # duplicate some
        num_dup = rng.randint(0, min(5, n // 2))
        dup_choices = rng.sample(nums, num_dup)
        result = list(nums)
        for d in dup_choices:
            # replace one other element so length stays bounded or standard
            pass
        # standard leetcode: array of length n where elements are 1..n and appear once or twice
        # let's construct exactly that
        arr = []
        doubles = rng.sample(range(1, n + 1), num_dup)
        singles = [x for x in range(1, n + 1) if x not in doubles]
        # to keep length <= n:
        singles_chosen = rng.sample(singles, n - 2 * num_dup) if (n - 2 * num_dup) >= 0 else []
        for d in doubles:
            arr.extend([d, d])
        arr.extend(singles_chosen)
        rng.shuffle(arr)
        return [arr]

    register(
        slug="find-all-duplicates",
        title="Find All Duplicates in an Array",
        topic_key="arrays",
        diff="medium",
        statement="Given an integer array `nums` where each integer appears once or twice, return an array of all integers that appear twice in ascending order.",
        fn="findDuplicates",
        params=["nums"],
        examples=[
            [[[4, 3, 2, 7, 8, 2, 3, 1]], [2, 3]],
            [[[1, 1, 2]], [1]],
            [[[1]], []]
        ],
        sol=sol_duplicates,
        gen=gen_duplicates
    )

    # 3. Count Pairs With Difference K
    def sol_count_k_diff(nums, k):
        cnt = 0
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if abs(nums[i] - nums[j]) == k:
                    cnt += 1
        return cnt

    def gen_count_k_diff(rng):
        n = rng.randint(3, 20)
        nums = [rng.randint(1, 20) for _ in range(n)]
        k = rng.randint(1, 5)
        return [nums, k]

    register(
        slug="count-pairs-difference-k",
        title="Count Pairs With Difference K",
        topic_key="arrays",
        diff="medium",
        statement="Given an integer array `nums` and an integer `k`, return the number of pairs `(i, j)` where `i < j` such that `|nums[i] - nums[j]| == k`.",
        fn="countKDifference",
        params=["nums", "k"],
        examples=[
            [[[1, 2, 2, 1], 1], 4],
            [[[1, 3], 3], 0],
            [[[3, 2, 1, 5, 4], 2], 3]
        ],
        sol=sol_count_k_diff,
        gen=gen_count_k_diff
    )

    # 4. Sort Array by Parity
    def sol_sort_parity(nums):
        evens = sorted([x for x in nums if x % 2 == 0])
        odds = sorted([x for x in nums if x % 2 != 0])
        return evens + odds

    def gen_sort_parity(rng):
        n = rng.randint(2, 20)
        nums = [rng.randint(0, 50) for _ in range(n)]
        return [nums]

    register(
        slug="sort-by-parity",
        title="Sort Array by Parity",
        topic_key="arrays",
        diff="easy",
        statement="Given an integer array `nums`, return an array with all even integers first (sorted ascending), followed by all odd integers (sorted ascending).",
        fn="sortArrayByParity",
        params=["nums"],
        examples=[
            [[[3, 1, 2, 4]], [2, 4, 1, 3]],
            [[[0]], [0]]
        ],
        sol=sol_sort_parity,
        gen=gen_sort_parity
    )

    # 5. Find Pivot Index
    def sol_pivot(nums):
        total = sum(nums)
        left = 0
        for i, x in enumerate(nums):
            if left == total - left - x:
                return i
            left += x
        return -1

    def gen_pivot(rng):
        n = rng.randint(3, 20)
        nums = [rng.randint(-10, 20) for _ in range(n)]
        return [nums]

    register(
        slug="find-pivot-index",
        title="Find Pivot Index",
        topic_key="arrays",
        diff="easy",
        statement="Given an array of integers `nums`, calculate the pivot index of this array. The pivot index is the index where the sum of all the numbers strictly to the left of the index is equal to the sum of all the numbers strictly to the index's right. Return the leftmost pivot index, or -1 if none exists.",
        fn="pivotIndex",
        params=["nums"],
        examples=[
            [[[1, 7, 3, 6, 5, 6]], 3],
            [[[1, 2, 3]], -1],
            [[[2, 1, -1]], 0]
        ],
        sol=sol_pivot,
        gen=gen_pivot
    )

    # 6. Relative Sort Array
    def sol_rel_sort(arr1, arr2):
        rank = {val: i for i, val in enumerate(arr2)}
        in_arr2 = [x for x in arr1 if x in rank]
        not_in_arr2 = [x for x in arr1 if x not in rank]
        in_arr2.sort(key=lambda x: rank[x])
        not_in_arr2.sort()
        return in_arr2 + not_in_arr2

    def gen_rel_sort(rng):
        arr2_len = rng.randint(2, 6)
        arr2 = sorted(rng.sample(range(1, 30), arr2_len))
        rng.shuffle(arr2)
        n = rng.randint(arr2_len, 25)
        arr1 = []
        # ensure arr2 elements are present
        arr1.extend(arr2)
        for _ in range(n - arr2_len):
            if rng.random() < 0.6:
                arr1.append(rng.choice(arr2))
            else:
                arr1.append(rng.randint(1, 40))
        rng.shuffle(arr1)
        return [arr1, arr2]

    register(
        slug="relative-sort-array",
        title="Relative Sort Array",
        topic_key="arrays",
        diff="easy",
        statement="Given two arrays `arr1` and `arr2`, the elements of `arr2` are distinct and appear in `arr1`. Sort the elements of `arr1` such that the relative ordering of items in `arr1` are the same as in `arr2`. Elements that do not appear in `arr2` should be placed at the end of `arr1` in ascending order.",
        fn="relativeSortArray",
        params=["arr1", "arr2"],
        examples=[
            [[[2, 3, 1, 3, 2, 4, 6, 7, 9, 2, 19], [2, 1, 4, 3, 9, 6]], [2, 2, 2, 1, 4, 3, 3, 9, 6, 7, 19]],
            [[[28, 6, 22, 8, 44, 17], [22, 28, 8, 6]], [22, 28, 8, 6, 17, 44]]
        ],
        sol=sol_rel_sort,
        gen=gen_rel_sort
    )

    # 7. Trapping Rain Water
    def sol_trap(height):
        if not height:
            return 0
        l, r = 0, len(height) - 1
        l_max, r_max = height[l], height[r]
        water = 0
        while l < r:
            if l_max < r_max:
                l += 1
                l_max = max(l_max, height[l])
                water += l_max - height[l]
            else:
                r -= 1
                r_max = max(r_max, height[r])
                water += r_max - height[r]
        return water

    def gen_trap(rng):
        n = rng.randint(3, 20)
        h = [rng.randint(0, 8) for _ in range(n)]
        return [h]

    register(
        slug="trapping-rain-water",
        title="Trapping Rain Water",
        topic_key="two_pointers",
        diff="hard",
        statement="Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
        fn="trap",
        params=["height"],
        examples=[
            [[[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]], 6],
            [[[4, 2, 0, 3, 2, 5]], 9]
        ],
        sol=sol_trap,
        gen=gen_trap
    )

    # 8. Sort Colors (Dutch National Flag)
    def sol_sort_colors(nums):
        nums = list(nums)
        low, mid, high = 0, 0, len(nums) - 1
        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1
        return nums

    def gen_sort_colors(rng):
        n = rng.randint(2, 20)
        nums = [rng.choice([0, 1, 2]) for _ in range(n)]
        return [nums]

    register(
        slug="sort-colors",
        title="Sort Colors (Dutch National Flag)",
        topic_key="two_pointers",
        diff="medium",
        statement="Given an array `nums` with `n` objects colored red, white, or blue (represented by 0, 1, and 2), sort them in-place so that objects of the same color are adjacent. Return the sorted array.",
        fn="sortColors",
        params=["nums"],
        examples=[
            [[[2, 0, 2, 1, 1, 0]], [0, 0, 1, 1, 2, 2]],
            [[[2, 0, 1]], [0, 1, 2]]
        ],
        sol=sol_sort_colors,
        gen=gen_sort_colors
    )

    # 9. Permutation in String
    def sol_perm_str(s1, s2):
        if len(s1) > len(s2):
            return False
        c1 = Counter(s1)
        window = Counter(s2[:len(s1)])
        if c1 == window:
            return True
        for i in range(len(s1), len(s2)):
            window[s2[i]] += 1
            window[s2[i - len(s1)]] -= 1
            if window[s2[i - len(s1)]] == 0:
                del window[s2[i - len(s1)]]
            if window == c1:
                return True
        return False

    def gen_perm_str(rng):
        alpha = "abcde"
        l1 = rng.randint(2, 5)
        l2 = rng.randint(l1, 15)
        s1 = "".join(rng.choice(alpha) for _ in range(l1))
        if rng.random() < 0.5:
            # embed permutation
            p = list(s1)
            rng.shuffle(p)
            pos = rng.randint(0, l2 - l1)
            s2_list = [rng.choice(alpha) for _ in range(l2)]
            s2_list[pos:pos+l1] = p
            s2 = "".join(s2_list)
        else:
            s2 = "".join(rng.choice(alpha) for _ in range(l2))
        return [s1, s2]

    register(
        slug="permutation-in-string",
        title="Permutation in String",
        topic_key="two_pointers",
        diff="medium",
        statement="Given two strings `s1` and `s2`, return `true` if `s2` contains a permutation of `s1`, or `false` otherwise.",
        fn="checkInclusion",
        params=["s1", "s2"],
        examples=[
            [["ab", "eidbaooo"], True],
            [["ab", "eidboaoo"], False]
        ],
        sol=sol_perm_str,
        gen=gen_perm_str
    )

    # 10. Find All Anagrams in a String
    def sol_anagrams(s, p):
        if len(p) > len(s):
            return []
        cp = Counter(p)
        window = Counter(s[:len(p)])
        res = []
        if window == cp:
            res.append(0)
        for i in range(len(p), len(s)):
            window[s[i]] += 1
            window[s[i - len(p)]] -= 1
            if window[s[i - len(p)]] == 0:
                del window[s[i - len(p)]]
            if window == cp:
                res.append(i - len(p) + 1)
        return res

    def gen_anagrams(rng):
        alpha = "abc"
        lp = rng.randint(2, 4)
        ls = rng.randint(lp, 15)
        p = "".join(rng.choice(alpha) for _ in range(lp))
        s = "".join(rng.choice(alpha) for _ in range(ls))
        return [s, p]

    register(
        slug="find-all-anagrams",
        title="Find All Anagrams in a String",
        topic_key="two_pointers",
        diff="medium",
        statement="Given two strings `s` and `p`, return an array of all the start indices of `p`'s anagrams in `s` in ascending order.",
        fn="findAnagrams",
        params=["s", "p"],
        examples=[
            [["cbaebabacd", "abc"], [0, 6]],
            [["abab", "ab"], [0, 1, 2]]
        ],
        sol=sol_anagrams,
        gen=gen_anagrams
    )
