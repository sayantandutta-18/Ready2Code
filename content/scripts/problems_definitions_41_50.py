from collections import Counter, defaultdict
import heapq
import random

def add_problems_41_50(register):
    # 41. Longest Valid Parentheses
    def sol_longest_valid_parens(s):
        stack = [-1]
        max_len = 0
        for i, ch in enumerate(s):
            if ch == '(':
                stack.append(i)
            else:
                stack.pop()
                if not stack:
                    stack.append(i)
                else:
                    max_len = max(max_len, i - stack[-1])
        return max_len

    def gen_longest_valid_parens(rng):
        n = rng.randint(2, 20)
        s = "".join(rng.choice("()") for _ in range(n))
        return [s]

    register(
        slug="longest-valid-parentheses",
        title="Longest Valid Parentheses",
        topic_key="dp",
        diff="hard",
        statement="Given a string containing just the characters `'('` and `')'`, return the length of the longest valid (well-formed) parentheses substring.",
        fn="longestValidParentheses",
        params=["s"],
        examples=[
            [["(()"], 2],
            [[")()())"], 4],
            [[""], 0]
        ],
        sol=sol_longest_valid_parens,
        gen=gen_longest_valid_parens
    )

    # 42. Interleaving String
    def sol_interleave(s1, s2, s3):
        if len(s1) + len(s2) != len(s3):
            return False
        dp = [True] + [False] * len(s2)
        for j in range(1, len(s2) + 1):
            dp[j] = dp[j - 1] and s2[j - 1] == s3[j - 1]
        for i in range(1, len(s1) + 1):
            dp[0] = dp[0] and s1[i - 1] == s3[i - 1]
            for j in range(1, len(s2) + 1):
                dp[j] = (dp[j] and s1[i - 1] == s3[i + j - 1]) or (dp[j - 1] and s2[j - 1] == s3[i + j - 1])
        return dp[-1]

    def gen_interleave(rng):
        l1 = rng.randint(0, 8)
        l2 = rng.randint(0, 8)
        s1 = "".join(rng.choice("abc") for _ in range(l1))
        s2 = "".join(rng.choice("abc") for _ in range(l2))
        if rng.random() < 0.5:
            # construct true interleaving
            i, j = 0, 0
            s3 = []
            while i < len(s1) or j < len(s2):
                if i < len(s1) and (j == len(s2) or rng.random() < 0.5):
                    s3.append(s1[i]); i += 1
                else:
                    s3.append(s2[j]); j += 1
            return [s1, s2, "".join(s3)]
        else:
            s3 = "".join(rng.choice("abc") for _ in range(l1 + l2))
            return [s1, s2, s3]

    register(
        slug="interleaving-string",
        title="Interleaving String",
        topic_key="dp",
        diff="hard",
        statement="Given strings `s1`, `s2`, and `s3`, find whether `s3` is formed by an interleaving of `s1` and `s2`.",
        fn="isInterleave",
        params=["s1", "s2", "s3"],
        examples=[
            [["aabcc", "dbbca", "aadbbcbcac"], True],
            [["aabcc", "dbbca", "aadbbbaccc"], False],
            [["", "", ""], True]
        ],
        sol=sol_interleave,
        gen=gen_interleave
    )

    # 43. Maximal Square
    def sol_maximal_square(matrix):
        if not matrix or not matrix[0]:
            return 0
        m, n = len(matrix), len(matrix[0])
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        max_side = 0
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if matrix[i - 1][j - 1] == "1" or matrix[i - 1][j - 1] == 1:
                    dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
                    max_side = max(max_side, dp[i][j])
        return max_side * max_side

    def gen_maximal_square(rng):
        m = rng.randint(2, 6)
        n = rng.randint(2, 6)
        matrix = [[rng.choice(["0", "1"]) for _ in range(n)] for _ in range(m)]
        return [matrix]

    register(
        slug="maximal-square",
        title="Maximal Square",
        topic_key="dp",
        diff="medium",
        statement="Given an `m x n` binary matrix filled with `'0'`s and `'1'`s, find the largest square containing only `'1'`s and return its area.",
        fn="maximalSquare",
        params=["matrix"],
        examples=[
            [[[["1", "0", "1", "0", "0"], ["1", "0", "1", "1", "1"], ["1", "1", "1", "1", "1"], ["1", "0", "0", "1", "0"]]], 4],
            [[[["0", "1"], ["1", "0"]]], 1],
            [[[["0"]]], 0]
        ],
        sol=sol_maximal_square,
        gen=gen_maximal_square
    )

    # 44. Burst Balloons
    def sol_burst_balloons(nums):
        vals = [1] + [x for x in nums if x > 0] + [1]
        n = len(vals)
        dp = [[0] * n for _ in range(n)]
        for length in range(1, n - 1):
            for left in range(0, n - length - 1):
                right = left + length + 1
                for i in range(left + 1, right):
                    dp[left][right] = max(
                        dp[left][right],
                        vals[left] * vals[i] * vals[right] + dp[left][i] + dp[i][right]
                    )
        return dp[0][n - 1]

    def gen_burst_balloons(rng):
        n = rng.randint(1, 6)
        nums = [rng.randint(1, 10) for _ in range(n)]
        return [nums]

    register(
        slug="burst-balloons",
        title="Burst Balloons",
        topic_key="dp",
        diff="hard",
        statement="You are given `n` balloons indexed from 0 to `n - 1`, each painted with a number `nums[i]`. Bursting balloon `i` earns `nums[i - 1] * nums[i] * nums[i + 1]` coins (out of bounds balloons are treated as painted with 1). Return the maximum coins you can collect by bursting all balloons wisely.",
        fn="maxCoins",
        params=["nums"],
        examples=[
            [[[3, 1, 5, 8]], 167],
            [[[1, 5]], 10]
        ],
        sol=sol_burst_balloons,
        gen=gen_burst_balloons
    )

    # 45. K Closest Points to Origin
    def sol_k_closest(points, k):
        # sorted by distance, tie break by x then y
        points_sorted = sorted(points, key=lambda p: (p[0]**2 + p[1]**2, p[0], p[1]))
        res = points_sorted[:k]
        # sort result deterministically by x then y
        return sorted(res, key=lambda p: (p[0], p[1]))

    def gen_k_closest(rng):
        n = rng.randint(3, 15)
        points = [[rng.randint(-20, 20), rng.randint(-20, 20)] for _ in range(n)]
        k = rng.randint(1, n)
        return [points, k]

    register(
        slug="k-closest-points",
        title="K Closest Points to Origin",
        topic_key="heap_greedy",
        diff="medium",
        statement="Given an array of `points` where `points[i] = [xi, yi]` and an integer `k`, return the `k` closest points to the origin `(0, 0)` in Euclidean distance. Return the answer sorted by x-coordinate, then y-coordinate.",
        fn="kClosest",
        params=["points", "k"],
        examples=[
            [[[[1, 3], [-2, 2]], 1], [[-2, 2]]],
            [[[[3, 3], [5, -1], [-2, 4]], 2], [[-2, 4], [3, 3]]]
        ],
        sol=sol_k_closest,
        gen=gen_k_closest
    )

    # 46. Reorganize String
    def sol_reorganize_string(s):
        counts = Counter(s)
        max_freq = max(counts.values())
        if max_freq > (len(s) + 1) // 2:
            return ""
        # Arrange characters so no adjacent are same
        max_heap = [(-cnt, char) for char, cnt in counts.items()]
        heapq.heapify(max_heap)
        res = []
        prev_cnt, prev_char = 0, ""
        while max_heap:
            cnt, char = heapq.heappop(max_heap)
            res.append(char)
            if prev_cnt < 0:
                heapq.heappush(max_heap, (prev_cnt, prev_char))
            prev_cnt = cnt + 1
            prev_char = char
        return "".join(res)

    def gen_reorganize_string(rng):
        alpha = "abcde"
        n = rng.randint(2, 15)
        s = "".join(rng.choice(alpha) for _ in range(n))
        return [s]

    register(
        slug="reorganize-string",
        title="Reorganize String",
        topic_key="heap_greedy",
        diff="medium",
        statement="Given a string `s`, rearrange the characters of `s` so that any two adjacent characters are not the same. Return the rearranged string (using highest frequency first), or return `\"\"` if not possible.",
        fn="reorganizeString",
        params=["s"],
        examples=[
            [["aab"], "aba"],
            [["aaab"], ""]
        ],
        sol=sol_reorganize_string,
        gen=gen_reorganize_string
    )

    # 47. Car Pooling
    def sol_car_pooling(trips, capacity):
        timeline = defaultdict(int)
        for num, start, end in trips:
            timeline[start] += num
            timeline[end] -= num
        used = 0
        for pos in sorted(timeline.keys()):
            used += timeline[pos]
            if used > capacity:
                return False
        return True

    def gen_car_pooling(rng):
        n = rng.randint(2, 6)
        trips = []
        for _ in range(n):
            num = rng.randint(1, 4)
            start = rng.randint(0, 10)
            end = start + rng.randint(1, 8)
            trips.append([num, start, end])
        cap = rng.randint(2, 10)
        return [trips, cap]

    register(
        slug="car-pooling",
        title="Car Pooling",
        topic_key="heap_greedy",
        diff="medium",
        statement="There is a car with `capacity` seats driving east. You are given an integer `capacity` and an array `trips` where `trips[i] = [numPassengers, from, to]`. Return `true` if it is possible to pick up and drop off all passengers for all the given trips without exceeding capacity, or `false` otherwise.",
        fn="carPooling",
        params=["trips", "capacity"],
        examples=[
            [[[[2, 1, 5], [3, 3, 7]], 4], False],
            [[[[2, 1, 5], [3, 3, 7]], 5], True]
        ],
        sol=sol_car_pooling,
        gen=gen_car_pooling
    )

    # 48. Partition Labels
    def sol_partition_labels(s):
        last = {ch: i for i, ch in enumerate(s)}
        j = anchor = 0
        ans = []
        for i, ch in enumerate(s):
            j = max(j, last[ch])
            if i == j:
                ans.append(i - anchor + 1)
                anchor = i + 1
        return ans

    def gen_partition_labels(rng):
        alpha = "abcdefg"
        n = rng.randint(3, 20)
        s = "".join(rng.choice(alpha) for _ in range(n))
        return [s]

    register(
        slug="partition-labels",
        title="Partition Labels",
        topic_key="heap_greedy",
        diff="medium",
        statement="You are given a string `s`. Partition the string into as many parts as possible so that each letter appears in at most one part. Return a list of integers representing the size of these parts.",
        fn="partitionLabels",
        params=["s"],
        examples=[
            [["ababcbacadefegdehijhklij"], [9, 7, 8]],
            [["eccbbbbdec"], [10]]
        ],
        sol=sol_partition_labels,
        gen=gen_partition_labels
    )

    # 49. Minimum Arrows to Burst Balloons
    def sol_min_arrows(points):
        if not points:
            return 0
        points_sorted = sorted(points, key=lambda x: x[1])
        arrows = 1
        end = points_sorted[0][1]
        for p in points_sorted[1:]:
            if p[0] > end:
                arrows += 1
                end = p[1]
        return arrows

    def gen_min_arrows(rng):
        n = rng.randint(2, 8)
        points = []
        for _ in range(n):
            a = rng.randint(-15, 15)
            points.append([a, a + rng.randint(1, 10)])
        return [points]

    register(
        slug="min-arrows-burst-balloons",
        title="Minimum Number of Arrows to Burst Balloons",
        topic_key="heap_greedy",
        diff="medium",
        statement="There are spherical balloons taped to a flat wall represented as intervals `points[i] = [xstart, xend]`. An arrow shot at `x` bursts all balloons where `xstart <= x <= xend`. Return the minimum number of arrows that must be shot to burst all balloons.",
        fn="findMinArrowShots",
        params=["points"],
        examples=[
            [[[[10, 16], [2, 8], [1, 6], [7, 12]]], 2],
            [[[[1, 2], [3, 4], [5, 6], [7, 8]]], 4],
            [[[[1, 2], [2, 3], [3, 4], [4, 5]]], 2]
        ],
        sol=sol_min_arrows,
        gen=gen_min_arrows
    )

    # 50. Hand of Straights
    def sol_hand_of_straights(hand, groupSize):
        if len(hand) % groupSize != 0:
            return False
        count = Counter(hand)
        for val in sorted(count):
            if count[val] > 0:
                needed = count[val]
                for i in range(val, val + groupSize):
                    if count[i] < needed:
                        return False
                    count[i] -= needed
        return True

    def gen_hand_of_straights(rng):
        groupSize = rng.randint(2, 4)
        num_groups = rng.randint(1, 4)
        hand = []
        for _ in range(num_groups):
            start = rng.randint(1, 10)
            hand.extend(range(start, start + groupSize))
        if rng.random() < 0.4:
            # mess up one card
            hand[rng.randint(0, len(hand) - 1)] += rng.choice([-1, 1]) * groupSize
        rng.shuffle(hand)
        return [hand, groupSize]

    register(
        slug="hand-of-straights",
        title="Hand of Straights",
        topic_key="heap_greedy",
        diff="medium",
        statement="Alice has an integer array `hand` of cards and an integer `groupSize`. She wants to rearrange the cards into groups so that each group has size `groupSize` and consists of `groupSize` consecutive cards. Return `true` if she can rearrange the cards, or `false` otherwise.",
        fn="isNStraightHand",
        params=["hand", "groupSize"],
        examples=[
            [[[1, 2, 3, 6, 2, 3, 4, 7, 8], 3], True],
            [[[1, 2, 3, 4, 5], 4], False]
        ],
        sol=sol_hand_of_straights,
        gen=gen_hand_of_straights
    )
