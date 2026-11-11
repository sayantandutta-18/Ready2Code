from collections import Counter, defaultdict, deque
import random

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

def add_problems_21_30(register):
    # 21. Online Stock Span
    def sol_stock_span(prices):
        stack = [] # (price, span)
        res = []
        for p in prices:
            span = 1
            while stack and stack[-1][0] <= p:
                span += stack.pop()[1]
            stack.append((p, span))
            res.append(span)
        return res

    def gen_stock_span(rng):
        n = rng.randint(3, 15)
        prices = [rng.randint(20, 150) for _ in range(n)]
        return [prices]

    register(
        slug="online-stock-span",
        title="Online Stock Span",
        topic_key="stack",
        diff="medium",
        statement="Given an array of daily stock prices `prices`, calculate the span of stock's price for each day. The span of the stock's price on a day is the maximum number of consecutive days (starting from today and going backward) for which the stock price was less than or equal to today's price. Return the array of spans.",
        fn="stockSpans",
        params=["prices"],
        examples=[
            [[[100, 80, 60, 70, 60, 75, 85]], [1, 1, 1, 2, 1, 4, 6]],
            [[[31, 41, 48, 59, 79]], [1, 2, 3, 4, 5]]
        ],
        sol=sol_stock_span,
        gen=gen_stock_span
    )

    # 22. Score of Parentheses
    def sol_score_parens(s):
        stack = [0]
        for ch in s:
            if ch == '(':
                stack.append(0)
            else:
                v = stack.pop()
                stack[-1] += max(2 * v, 1)
        return stack[0]

    def gen_score_parens(rng):
        # generate valid balanced parenthesis string
        def rand_parens(depth):
            if depth <= 0 or rng.random() < 0.4:
                return "()"
            choice = rng.randint(1, 3)
            if choice == 1:
                return "(" + rand_parens(depth - 1) + ")"
            else:
                return rand_parens(depth - 1) + rand_parens(depth - 1)
        s = rand_parens(3)
        return [s]

    register(
        slug="score-of-parentheses",
        title="Score of Parentheses",
        topic_key="stack",
        diff="medium",
        statement="Given a balanced parentheses string `s`, return the score of the string. `()` has score 1, `AB` has score `A + B`, and `(A)` has score `2 * A`.",
        fn="scoreOfParentheses",
        params=["s"],
        examples=[
            [["()"], 1],
            [["(())"], 2],
            [["()()"], 2]
        ],
        sol=sol_score_parens,
        gen=gen_score_parens
    )

    # 23. Add Two Numbers
    def sol_add_two_numbers(l1, l2):
        carry = 0
        i, j = 0, 0
        res = []
        while i < len(l1) or j < len(l2) or carry:
            val1 = l1[i] if i < len(l1) else 0
            val2 = l2[j] if j < len(l2) else 0
            total = val1 + val2 + carry
            res.append(total % 10)
            carry = total // 10
            i += 1
            j += 1
        return res

    def gen_add_two_numbers(rng):
        len1 = rng.randint(1, 8)
        len2 = rng.randint(1, 8)
        l1 = [rng.randint(0, 9) for _ in range(len1)]
        l2 = [rng.randint(0, 9) for _ in range(len2)]
        if len(l1) > 1 and l1[-1] == 0: l1[-1] = rng.randint(1, 9)
        if len(l2) > 1 and l2[-1] == 0: l2[-1] = rng.randint(1, 9)
        return [l1, l2]

    register(
        slug="add-two-numbers",
        title="Add Two Numbers",
        topic_key="linked_list",
        diff="medium",
        statement="You are given two non-empty arrays representing two non-negative integers stored in reverse order. Add the two numbers and return the sum as an array in reverse order.",
        fn="addTwoNumbers",
        params=["l1", "l2"],
        examples=[
            [[[2, 4, 3], [5, 6, 4]], [7, 0, 8]],
            [[[0], [0]], [0]],
            [[[9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9]], [8, 9, 9, 9, 0, 0, 0, 1]]
        ],
        sol=sol_add_two_numbers,
        gen=gen_add_two_numbers
    )

    # 24. Intersection of Two Linked Lists
    def sol_intersect_ll(listA, listB, skipA, skipB):
        # shared suffix starts at skipA in A and skipB in B
        if skipA < len(listA) and skipB < len(listB) and listA[skipA:] == listB[skipB:]:
            return listA[skipA]
        return None

    def gen_intersect_ll(rng):
        common_len = rng.randint(0, 4)
        common = [rng.randint(100, 200) for _ in range(common_len)]
        lenA = rng.randint(1, 5)
        lenB = rng.randint(1, 5)
        listA = [rng.randint(1, 50) for _ in range(lenA)] + common
        listB = [rng.randint(51, 99) for _ in range(lenB)] + common
        return [listA, listB, lenA if common_len > 0 else len(listA), lenB if common_len > 0 else len(listB)]

    register(
        slug="intersection-linked-lists",
        title="Intersection of Two Linked Lists",
        topic_key="linked_list",
        diff="easy",
        statement="Given two arrays `listA` and `listB` and the skip counts `skipA` and `skipB` where after `skipA` nodes in A and `skipB` nodes in B the lists merge to share the same suffix, return the value of the intersecting node, or `null` if they do not intersect.",
        fn="getIntersectionNode",
        params=["listA", "listB", "skipA", "skipB"],
        examples=[
            [[[4, 1, 8, 4, 5], [5, 6, 1, 8, 4, 5], 2, 3], 8],
            [[[1, 9, 1, 2, 4], [3, 2, 4], 3, 1], 2],
            [[[2, 6, 4], [1, 5], 3, 2], None]
        ],
        sol=sol_intersect_ll,
        gen=gen_intersect_ll
    )

    # 25. Odd Even Linked List
    def sol_odd_even_ll(values):
        if len(values) <= 2:
            return list(values)
        odds = values[0::2]
        evens = values[1::2]
        return odds + evens

    def gen_odd_even_ll(rng):
        n = rng.randint(1, 15)
        vals = [rng.randint(1, 50) for _ in range(n)]
        return [vals]

    register(
        slug="odd-even-linked-list",
        title="Odd Even Linked List",
        topic_key="linked_list",
        diff="medium",
        statement="Given an array of integers `values` representing a singly linked list, group all nodes with odd indices together followed by the nodes with even indices (1-indexed: 1st, 3rd, 5th... then 2nd, 4th, 6th...). Return the reordered array.",
        fn="oddEvenList",
        params=["values"],
        examples=[
            [[[1, 2, 3, 4, 5]], [1, 3, 5, 2, 4]],
            [[[2, 1, 3, 5, 6, 4, 7]], [2, 3, 6, 7, 1, 5, 4]]
        ],
        sol=sol_odd_even_ll,
        gen=gen_odd_even_ll
    )

    # 26. Balanced Binary Tree
    def sol_balanced_bt(root):
        tree = build(root)
        def height(node):
            if not node:
                return 0
            lh = height(node.left)
            if lh == -1: return -1
            rh = height(node.right)
            if rh == -1: return -1
            if abs(lh - rh) > 1:
                return -1
            return 1 + max(lh, rh)
        return height(tree) != -1

    def gen_balanced_bt(rng):
        if rng.random() < 0.5:
            # balanced tree
            n = rng.randint(1, 15)
            vals = [rng.randint(1, 20) for _ in range(n)]
            return [vals]
        else:
            # unbalanced tree (e.g. linked chain)
            vals = []
            cur = 0
            for i in range(rng.randint(4, 7)):
                vals.append(rng.randint(1, 20))
                vals.append(None)
            return [vals]

    register(
        slug="balanced-binary-tree",
        title="Balanced Binary Tree",
        topic_key="trees",
        diff="easy",
        statement="Given the root of a binary tree represented as a level-order serialized array, determine if it is height-balanced (the depth of the two subtrees of every node never differs by more than one).",
        fn="isBalanced",
        params=["root"],
        examples=[
            [[[3, 9, 20, None, None, 15, 7]], True],
            [[[1, 2, 2, 3, 3, None, None, 4, 4]], False],
            [[[]], True]
        ],
        sol=sol_balanced_bt,
        gen=gen_balanced_bt
    )

    # 27. Sum Root to Leaf Numbers
    def sol_sum_root_to_leaf(root):
        tree = build(root)
        def dfs(node, cur_val):
            if not node:
                return 0
            cur_val = cur_val * 10 + node.val
            if not node.left and not node.right:
                return cur_val
            return dfs(node.left, cur_val) + dfs(node.right, cur_val)
        return dfs(tree, 0)

    def gen_sum_root_to_leaf(rng):
        n = rng.randint(1, 10)
        vals = [rng.randint(0, 9) for _ in range(n)]
        if vals: vals[0] = rng.randint(1, 9) # non-zero root
        return [vals]

    register(
        slug="sum-root-to-leaf",
        title="Sum Root to Leaf Numbers",
        topic_key="trees",
        diff="medium",
        statement="You are given the root of a binary tree containing digits from 0 to 9 only (as a level-order array). Each root-to-leaf path represents a number. Return the total sum of all root-to-leaf numbers.",
        fn="sumNumbers",
        params=["root"],
        examples=[
            [[[1, 2, 3]], 25],
            [[[4, 9, 0, 5, 1]], 1026]
        ],
        sol=sol_sum_root_to_leaf,
        gen=gen_sum_root_to_leaf
    )

    # 28. Kth Smallest Element in a BST
    def sol_kth_smallest_bst(root, k):
        tree = build(root)
        inorder = []
        def dfs(node):
            if not node:
                return
            dfs(node.left)
            inorder.append(node.val)
            dfs(node.right)
        dfs(tree)
        return inorder[k - 1]

    def gen_kth_smallest_bst(rng):
        # generate valid BST
        n = rng.randint(3, 12)
        unique_vals = sorted(rng.sample(range(1, 50), n))
        def bst_from_sorted(arr):
            if not arr:
                return None
            mid = len(arr) // 2
            node = TN(arr[mid])
            node.left = bst_from_sorted(arr[:mid])
            node.right = bst_from_sorted(arr[mid+1:])
            return node
        t = bst_from_sorted(unique_vals)
        arr = ser(t)
        k = rng.randint(1, n)
        return [arr, k]

    register(
        slug="kth-smallest-bst",
        title="Kth Smallest Element in a BST",
        topic_key="trees",
        diff="medium",
        statement="Given the root of a binary search tree (as a level-order serialized array) and an integer `k`, return the `k`-th smallest value (1-indexed) of all the values of the nodes in the tree.",
        fn="kthSmallest",
        params=["root", "k"],
        examples=[
            [[[3, 1, 4, None, 2], 1], 1],
            [[[5, 3, 6, 2, 4, None, None, 1], 3], 3]
        ],
        sol=sol_kth_smallest_bst,
        gen=gen_kth_smallest_bst
    )

    # 29. Binary Tree Zigzag Level Order Traversal
    def sol_zigzag_level(root):
        tree = build(root)
        if not tree:
            return []
        res = []
        q = deque([tree])
        left_to_right = True
        while q:
            level_size = len(q)
            level = deque()
            for _ in range(level_size):
                node = q.popleft()
                if left_to_right:
                    level.append(node.val)
                else:
                    level.appendleft(node.val)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            res.append(list(level))
            left_to_right = not left_to_right
        return res

    def gen_zigzag_level(rng):
        n = rng.randint(1, 15)
        vals = [rng.randint(-20, 50) for _ in range(n)]
        return [vals]

    register(
        slug="zigzag-level-order",
        title="Binary Tree Zigzag Level Order Traversal",
        topic_key="trees",
        diff="medium",
        statement="Given the root of a binary tree (as a level-order array), return the zigzag level order traversal of its nodes' values (i.e., alternating from left to right, then right to left for the next level).",
        fn="zigzagLevelOrder",
        params=["root"],
        examples=[
            [[[3, 9, 20, None, None, 15, 7]], [[3], [20, 9], [15, 7]]],
            [[[1]], [[1]]],
            [[[]], []]
        ],
        sol=sol_zigzag_level,
        gen=gen_zigzag_level
    )

    # 30. Pacific Atlantic Water Flow
    def sol_pacific_atlantic(heights):
        if not heights or not heights[0]:
            return []
        m, n = len(heights), len(heights[0])
        pac = set()
        atl = set()

        def dfs(r, c, visit, prev):
            if (r, c) in visit or r < 0 or c < 0 or r >= m or c >= n or heights[r][c] < prev:
                return
            visit.add((r, c))
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                dfs(r + dr, c + dc, visit, heights[r][c])

        for c in range(n):
            dfs(0, c, pac, heights[0][c])
            dfs(m - 1, c, atl, heights[m - 1][c])
        for r in range(m):
            dfs(r, 0, pac, heights[r][0])
            dfs(r, n - 1, atl, heights[r][n - 1])

        common = sorted([[r, c] for (r, c) in (pac & atl)])
        return common

    def gen_pacific_atlantic(rng):
        m = rng.randint(2, 6)
        n = rng.randint(2, 6)
        grid = [[rng.randint(1, 10) for _ in range(n)] for _ in range(m)]
        return [grid]

    register(
        slug="pacific-atlantic",
        title="Pacific Atlantic Water Flow",
        topic_key="graphs",
        diff="medium",
        statement="Given an `m x n` integer matrix `heights` representing an island bordering the Pacific Ocean (top and left edges) and Atlantic Ocean (bottom and right edges), water flows to neighboring cells of equal or lesser height. Return a sorted 2D list of coordinates `[r, c]` from which rainwater can flow to both oceans.",
        fn="pacificAtlantic",
        params=["heights"],
        examples=[
            [[[[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]]], [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]],
            [[[[1]]], [[0, 0]]]
        ],
        sol=sol_pacific_atlantic,
        gen=gen_pacific_atlantic
    )
