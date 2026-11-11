from collections import Counter, defaultdict, deque
import heapq
import random

def add_problems_31_40(register):
    # 31. Surrounded Regions
    def sol_surrounded_regions(board):
        board = [row[:] for row in board]
        if not board or not board[0]:
            return board
        m, n = len(board), len(board[0])

        def dfs(r, c):
            if r < 0 or c < 0 or r >= m or c >= n or board[r][c] != "O":
                return
            board[r][c] = "E"
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                dfs(r + dr, c + dc)

        for r in range(m):
            dfs(r, 0)
            dfs(r, n - 1)
        for c in range(n):
            dfs(0, c)
            dfs(m - 1, c)

        for r in range(m):
            for c in range(n):
                if board[r][c] == "O":
                    board[r][c] = "X"
                elif board[r][c] == "E":
                    board[r][c] = "O"
        return board

    def gen_surrounded_regions(rng):
        m = rng.randint(2, 6)
        n = rng.randint(2, 6)
        board = [[rng.choice(["X", "O"]) for _ in range(n)] for _ in range(m)]
        return [board]

    register(
        slug="surrounded-regions",
        title="Surrounded Regions",
        topic_key="graphs",
        diff="medium",
        statement="Given an `m x n` matrix `board` containing `'X'` and `'O'`, capture all regions that are 4-directionally surrounded by `'X'`. A region is captured by flipping all `'O'`s into `'X'`s in that surrounded region (any `'O'` connected to the boundary is not flipped). Return the updated board.",
        fn="solve",
        params=["board"],
        examples=[
            [[[["X", "X", "X", "X"], ["X", "O", "O", "X"], ["X", "X", "O", "X"], ["X", "O", "X", "X"]]],
             [["X", "X", "X", "X"], ["X", "X", "X", "X"], ["X", "X", "X", "X"], ["X", "O", "X", "X"]]],
            [[[["X"]]], [["X"]]]
        ],
        sol=sol_surrounded_regions,
        gen=gen_surrounded_regions
    )

    # 32. Network Delay Time
    def sol_network_delay(times, n, k):
        adj = defaultdict(list)
        for u, v, w in times:
            adj[u].append((v, w))
        pq = [(0, k)]
        dist = {}
        while pq:
            d, u = heapq.heappop(pq)
            if u in dist:
                continue
            dist[u] = d
            for v, w in adj[u]:
                if v not in dist:
                    heapq.heappush(pq, (d + w, v))
        return max(dist.values()) if len(dist) == n else -1

    def gen_network_delay(rng):
        n = rng.randint(2, 6)
        edges = []
        for u in range(1, n + 1):
            for v in range(1, n + 1):
                if u != v and rng.random() < 0.4:
                    edges.append([u, v, rng.randint(1, 15)])
        k = rng.randint(1, n)
        return [edges, n, k]

    register(
        slug="network-delay-time",
        title="Network Delay Time",
        topic_key="graphs",
        diff="medium",
        statement="You are given a network of `n` nodes labeled `1` to `n`. You are given `times`, a list of directed edges `times[i] = [u, v, w]`, where `u` is the source, `v` is the target, and `w` is the travel time. Return the minimum time it takes for all `n` nodes to receive a signal sent from node `k`, or `-1` if not all nodes can receive it.",
        fn="networkDelayTime",
        params=["times", "n", "k"],
        examples=[
            [[[[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2], 2],
            [[[[1, 2, 1]], 2, 1], 1],
            [[[[1, 2, 1]], 2, 2], -1]
        ],
        sol=sol_network_delay,
        gen=gen_network_delay
    )

    # 33. Redundant Connection
    def sol_redundant_conn(edges):
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

    def gen_redundant_conn(rng):
        # generate tree of n nodes then add 1 edge
        n = rng.randint(3, 8)
        edges = []
        nodes = list(range(1, n + 1))
        rng.shuffle(nodes)
        for i in range(1, n):
            edges.append([nodes[i], nodes[rng.randint(0, i - 1)]])
        # add one extra cycle-creating edge
        u, v = rng.sample(nodes, 2)
        while [u, v] in edges or [v, u] in edges:
            u, v = rng.sample(nodes, 2)
        edges.append([u, v])
        return [edges]

    register(
        slug="redundant-connection",
        title="Redundant Connection",
        topic_key="graphs",
        diff="medium",
        statement="Given an undirected graph that started as a tree with `n` nodes labeled `1` to `n` with one additional edge added, return an edge that can be removed so that the resulting graph is a tree. If multiple answers exist, return the edge that occurs last in the input.",
        fn="findRedundantConnection",
        params=["edges"],
        examples=[
            [[[[1, 2], [1, 3], [2, 3]]], [2, 3]],
            [[[[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]], [1, 4]]
        ],
        sol=sol_redundant_conn,
        gen=gen_redundant_conn
    )

    # 34. Find Peak Element
    def sol_find_peak(nums):
        left, right = 0, len(nums) - 1
        while left < right:
            mid = (left + right) // 2
            if nums[mid] > nums[mid + 1]:
                right = mid
            else:
                left = mid + 1
        return left

    def gen_find_peak(rng):
        n = rng.randint(1, 15)
        # distinct adjacent numbers
        nums = []
        for _ in range(n):
            val = rng.randint(-50, 50)
            while nums and nums[-1] == val:
                val = rng.randint(-50, 50)
            nums.append(val)
        return [nums]

    register(
        slug="find-peak-element",
        title="Find Peak Element",
        topic_key="binary_search",
        diff="medium",
        statement="A peak element is an element that is strictly greater than its neighbors. Given a 0-indexed integer array `nums` where no two adjacent elements are equal, find a peak element and return its index using binary search.",
        fn="findPeakElement",
        params=["nums"],
        examples=[
            [[[1, 2, 3, 1]], 2],
            [[[1, 2, 1, 3, 5, 6, 4]], 5]
        ],
        sol=sol_find_peak,
        gen=gen_find_peak
    )

    # 35. Capacity to Ship Packages
    def sol_ship_within_days(weights, days):
        left, right = max(weights), sum(weights)
        while left < right:
            mid = (left + right) // 2
            needed = 1
            cur = 0
            for w in weights:
                if cur + w > mid:
                    needed += 1
                    cur = 0
                cur += w
            if needed <= days:
                right = mid
            else:
                left = mid + 1
        return left

    def gen_ship_within_days(rng):
        n = rng.randint(3, 15)
        weights = [rng.randint(1, 20) for _ in range(n)]
        days = rng.randint(1, n)
        return [weights, days]

    register(
        slug="capacity-ship-packages",
        title="Capacity to Ship Packages Within D Days",
        topic_key="binary_search",
        diff="medium",
        statement="A conveyor belt has packages that must be shipped within `days` days. Return the least weight capacity of the ship that will result in all the packages being shipped within `days` days.",
        fn="shipWithinDays",
        params=["weights", "days"],
        examples=[
            [[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5], 15],
            [[[3, 2, 2, 4, 1, 4], 3], 6],
            [[[1, 2, 3, 1, 1], 4], 3]
        ],
        sol=sol_ship_within_days,
        gen=gen_ship_within_days
    )

    # 36. Median of Two Sorted Arrays
    def sol_median_sorted(nums1, nums2):
        merged = sorted(nums1 + nums2)
        m = len(merged)
        if m % 2 == 1:
            return float(merged[m // 2])
        return (merged[m // 2 - 1] + merged[m // 2]) / 2.0

    def gen_median_sorted(rng):
        l1 = rng.randint(0, 10)
        l2 = rng.randint(1 if l1 == 0 else 0, 10)
        n1 = sorted(rng.randint(-50, 50) for _ in range(l1))
        n2 = sorted(rng.randint(-50, 50) for _ in range(l2))
        return [n1, n2]

    register(
        slug="median-two-sorted-arrays",
        title="Median of Two Sorted Arrays",
        topic_key="binary_search",
        diff="hard",
        statement="Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the median of the two sorted arrays as a float.",
        fn="findMedianSortedArrays",
        params=["nums1", "nums2"],
        examples=[
            [[[1, 3], [2]], 2.0],
            [[[1, 2], [3, 4]], 2.5]
        ],
        sol=sol_median_sorted,
        gen=gen_median_sorted
    )

    # 37. House Robber II
    def sol_rob_ii(nums):
        if len(nums) == 1:
            return nums[0]
        def rob_line(arr):
            p1 = p2 = 0
            for x in arr:
                p1, p2 = max(p1, p2 + x), p1
            return p1
        return max(rob_line(nums[:-1]), rob_line(nums[1:]))

    def gen_rob_ii(rng):
        n = rng.randint(1, 15)
        nums = [rng.randint(0, 50) for _ in range(n)]
        return [nums]

    register(
        slug="house-robber-ii",
        title="House Robber II",
        topic_key="dp",
        diff="medium",
        statement="You are planning to rob houses arranged in a circle (the first house and the last house are neighbors). Adjacent houses cannot be robbed on the same night. Return the maximum amount of money you can rob.",
        fn="rob",
        params=["nums"],
        examples=[
            [[[2, 3, 2]], 3],
            [[[1, 2, 3, 1]], 4],
            [[[1, 2, 3]], 3]
        ],
        sol=sol_rob_ii,
        gen=gen_rob_ii
    )

    # 38. Longest Palindromic Subsequence
    def sol_lps(s):
        n = len(s)
        dp = [0] * n
        for i in range(n - 1, -1, -1):
            new_dp = [0] * n
            new_dp[i] = 1
            for j in range(i + 1, n):
                if s[i] == s[j]:
                    new_dp[j] = dp[j - 1] + 2
                else:
                    new_dp[j] = max(dp[j], new_dp[j - 1])
            dp = new_dp
        return dp[n - 1] if n else 0

    def gen_lps(rng):
        n = rng.randint(1, 15)
        s = "".join(rng.choice("abcdef") for _ in range(n))
        return [s]

    register(
        slug="longest-palindromic-subsequence",
        title="Longest Palindromic Subsequence",
        topic_key="dp",
        diff="medium",
        statement="Given a string `s`, find the longest palindromic subsequence's length in `s`.",
        fn="longestPalindromeSubseq",
        params=["s"],
        examples=[
            [["bbbab"], 4],
            [["cbbd"], 2]
        ],
        sol=sol_lps,
        gen=gen_lps
    )

    # 39. Target Sum
    def sol_target_sum(nums, target):
        total = sum(nums)
        if abs(target) > total or (total + target) % 2 != 0:
            return 0
        s = (total + target) // 2
        dp = defaultdict(int)
        dp[0] = 1
        for x in nums:
            next_dp = defaultdict(int)
            for current_sum, count in dp.items():
                next_dp[current_sum] += count
                if current_sum + x <= s:
                    next_dp[current_sum + x] += count
            dp = next_dp
        return dp[s]

    def gen_target_sum(rng):
        n = rng.randint(1, 10)
        nums = [rng.randint(0, 10) for _ in range(n)]
        target = rng.randint(-sum(nums), sum(nums))
        return [nums, target]

    register(
        slug="target-sum",
        title="Target Sum",
        topic_key="dp",
        diff="medium",
        statement="You are given an integer array `nums` and an integer `target`. Build an expression out of `nums` by placing either `'+'` or `'-'` before each integer. Return the number of different expressions that evaluate to `target`.",
        fn="findTargetSumWays",
        params=["nums", "target"],
        examples=[
            [[[1, 1, 1, 1, 1], 3], 5],
            [[[1], 1], 1]
        ],
        sol=sol_target_sum,
        gen=gen_target_sum
    )

    # 40. Best Time to Buy and Sell Stock with Cooldown
    def sol_stock_cooldown(prices):
        if not prices:
            return 0
        sold, held, reset = 0, -float('inf'), 0
        for p in prices:
            pre_sold = sold
            sold = held + p
            held = max(held, reset - p)
            reset = max(reset, pre_sold)
        return max(sold, reset)

    def gen_stock_cooldown(rng):
        n = rng.randint(1, 15)
        prices = [rng.randint(1, 30) for _ in range(n)]
        return [prices]

    register(
        slug="stock-with-cooldown",
        title="Best Time to Buy and Sell Stock with Cooldown",
        topic_key="dp",
        diff="medium",
        statement="Given an array `prices` where `prices[i]` is the price of a given stock on the `i`-th day, find the maximum profit you can achieve. You may complete as many transactions as you like with the restriction: after you sell your stock, you cannot buy stock on the next day (i.e. cooldown 1 day).",
        fn="maxProfit",
        params=["prices"],
        examples=[
            [[[1, 2, 3, 0, 2]], 3],
            [[[1]], 0]
        ],
        sol=sol_stock_cooldown,
        gen=gen_stock_cooldown
    )
