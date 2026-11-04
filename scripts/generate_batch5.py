"""
Problem Generator - Batch 5:
- Graphs (5 problems: 1 Easy, 3 Medium, 1 Hard)
- Binary Search (4 problems: 2 Easy, 1 Medium, 1 Hard)
- Dynamic Programming (5 problems: 1 Easy, 3 Medium, 1 Hard)
- Heap and Intervals (3 problems: 1 Easy, 1 Medium, 1 Hard)
Total: 17 problems -> Completing the 60 problem bank!
"""
import os
import json

PROBLEMS = [
    # 44. Graphs - Easy
    {
        "slug": "flood-fill-pixel-grid",
        "title": "Flood Fill Connected Pixel Matrix",
        "difficulty": "easy",
        "topic": "Graphs",
        "tags": ["Graph", "Breadth-First Search", "Depth-First Search", "Matrix"],
        "company_tags": ["Amazon", "Google", "Apple"],
        "statement_md": "An image is represented by an `m x n` integer grid `image` where `image[i][j]` represents the pixel value of the image. You are also given three integers `sr`, `sc`, and `color`.\n\nYou should perform a flood fill on the image starting from the pixel `image[sr][sc]`.\n\nTo perform a flood fill, consider the starting pixel, plus any pixels connected 4-directionally to the starting pixel of the same color, plus any pixels connected 4-directionally to those pixels, and so on. Replace the color of all of the aforementioned pixels with `color`.\n\nReturn the modified image.\n\n### Input Format\n- Line 1: A JSON-encoded 2D list `image`\n- Line 2: Integer `sr`\n- Line 3: Integer `sc`\n- Line 4: Integer `color`\n\n### Output Format\n- A JSON-encoded 2D list representing the modified image",
        "examples": [
            {
                "input": "[[1, 1, 1], [1, 1, 0], [1, 0, 1]]\n1\n1\n2",
                "output": "[[2, 2, 2], [2, 2, 0], [2, 0, 1]]",
                "explanation": "From the center (1, 1) all connected 1s are changed to 2. Bottom right 1 is not connected 4-directionally."
            },
            {
                "input": "[[0, 0, 0], [0, 0, 0]]\n0\n0\n0",
                "output": "[[0, 0, 0], [0, 0, 0]]",
                "explanation": "Starting pixel is already color 0, no changes."
            }
        ],
        "sample_tests": [
            {"input_text": "[[1, 1, 1], [1, 1, 0], [1, 0, 1]]\n1\n1\n2", "expected_output": "[[2, 2, 2], [2, 2, 0], [2, 0, 1]]"},
            {"input_text": "[[0, 0, 0], [0, 0, 0]]\n0\n0\n0", "expected_output": "[[0, 0, 0], [0, 0, 0]]"},
            {"input_text": "[[0, 0, 0], [0, 1, 1]]\n1\n1\n1", "expected_output": "[[0, 0, 0], [0, 1, 1]]"}
        ],
        "hidden_tests": [
            {"input_text": "[[1]]\n0\n0\n2", "expected_output": "[[2]]"},
            {"input_text": "[[0, 0, 0], [0, 1, 0]]\n1\n1\n2", "expected_output": "[[0, 0, 0], [0, 2, 0]]"},
            {"input_text": "[[1, 2], [3, 4]]\n0\n1\n5", "expected_output": "[[1, 5], [3, 4]]"},
            {"input_text": "[[1, 1, 1], [1, 1, 1], [1, 1, 1]]\n0\n0\n9", "expected_output": "[[9, 9, 9], [9, 9, 9], [9, 9, 9]]"},
            {"input_text": "[[2, 2, 2], [2, 2, 2]]\n0\n0\n3", "expected_output": "[[3, 3, 3], [3, 3, 3]]"},
            {"input_text": "[[1, 0, 1], [0, 1, 0], [1, 0, 1]]\n1\n1\n7", "expected_output": "[[1, 0, 1], [0, 7, 0], [1, 0, 1]]"},
            {"input_text": "[[5, 5], [5, 5]]\n1\n1\n5", "expected_output": "[[5, 5], [5, 5]]"},
            {"input_text": "[[1, 2, 3], [4, 5, 6]]\n0\n0\n8", "expected_output": "[[8, 2, 3], [4, 5, 6]]"},
            {"input_text": "[[0, 1, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0]]\n1\n1\n3", "expected_output": "[[0, 3, 0, 0], [3, 3, 3, 0], [0, 3, 0, 0]]"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "If the starting pixel already has the target color, return immediately.", "xp_cost": 2},
            {"level": 2, "text": "Explore neighbors in the 4 cardinal directions (up, down, left, right).", "xp_cost": 5},
            {"level": 3, "text": "Use Breadth-First Search (BFS) with a Queue or Depth-First Search (DFS) recursion.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Connected Component BFS/DFS\n\nRecord `orig = image[sr][sc]`. If `orig == color`, return early. Use BFS queue or DFS recursion from `(sr, sc)` replacing all connected cells of color `orig` with `color`.\n\n#### Complexity\n- **Time Complexity:** $O(m \\cdot n)$ each cell visited at most once.\n- **Space Complexity:** $O(m \\cdot n)$ worst case queue/call stack.\n\n#### Common Pitfalls\n- Infinite recursion when `orig == color` without an early return check.",
        "reference_solutions": {
            "brute_python": "def floodFill(image, sr, sc, color):\n    orig = image[sr][sc]\n    if orig == color: return image\n    m, n = len(image), len(image[0])\n    def dfs(r, c):\n        if 0 <= r < m and 0 <= c < n and image[r][c] == orig:\n            image[r][c] = color\n            dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)\n    dfs(sr, sc)\n    return image",
            "optimal_python": "def floodFill(image, sr, sc, color):\n    orig = image[sr][sc]\n    if orig == color: return image\n    m, n = len(image), len(image[0])\n    q = [(sr, sc)]\n    image[sr][sc] = color\n    while q:\n        r, c = q.pop(0)\n        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:\n            nr, nc = r + dr, c + dc\n            if 0 <= nr < m and 0 <= nc < n and image[nr][nc] == orig:\n                image[nr][nc] = color\n                q.append((nr, nc))\n    return image",
            "optimal_java": "public class Solution {\n    public int[][] floodFill(int[][] image, int sr, int sc, int color) {\n        return image;\n    }\n}",
            "optimal_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<vector<int>> floodFill(vector<vector<int>>& image, int sr, int sc, int color) {\n        return image;\n    }\n};"
        }
    },

    # 45. Graphs - Medium
    {
        "slug": "number-of-connected-islands",
        "title": "Number of Connected Island Landmasses",
        "difficulty": "medium",
        "topic": "Graphs",
        "tags": ["Graph", "Breadth-First Search", "Depth-First Search", "Matrix"],
        "company_tags": ["Amazon", "Microsoft", "Meta", "Google"],
        "statement_md": "Given an `m x n` 2D binary grid `grid` which represents a map of `'1'`s (land) and `'0'`s (water), return the number of islands.\n\nAn island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.\n\n### Input Format\n- A JSON-encoded 2D list of strings `grid`\n\n### Output Format\n- An integer representing island count",
        "examples": [
            {
                "input": "[[\"1\", \"1\", \"1\", \"1\", \"0\"], [\"1\", \"1\", \"0\", \"1\", \"0\"], [\"1\", \"1\", \"0\", \"0\", \"0\"], [\"0\", \"0\", \"0\", \"0\", \"0\"]]",
                "output": "1",
                "explanation": "All 1s connect into 1 single island."
            },
            {
                "input": "[[\"1\", \"1\", \"0\", \"0\", \"0\"], [\"1\", \"1\", \"0\", \"0\", \"0\"], [\"0\", \"0\", \"1\", \"0\", \"0\"], [\"0\", \"0\", \"0\", \"1\", \"1\"]]",
                "output": "3",
                "explanation": "There are 3 distinct islands."
            }
        ],
        "sample_tests": [
            {"input_text": "[[\"1\", \"1\", \"1\", \"1\", \"0\"], [\"1\", \"1\", \"0\", \"1\", \"0\"], [\"1\", \"1\", \"0\", \"0\", \"0\"], [\"0\", \"0\", \"0\", \"0\", \"0\"]]", "expected_output": "1"},
            {"input_text": "[[\"1\", \"1\", \"0\", \"0\", \"0\"], [\"1\", \"1\", \"0\", \"0\", \"0\"], [\"0\", \"0\", \"1\", \"0\", \"0\"], [\"0\", \"0\", \"0\", \"1\", \"1\"]]", "expected_output": "3"},
            {"input_text": "[[\"0\"]]", "expected_output": "0"}
        ],
        "hidden_tests": [
            {"input_text": "[]", "expected_output": "0"},
            {"input_text": "[[\"1\"]]", "expected_output": "1"},
            {"input_text": "[[\"1\", \"0\", \"1\"]]", "expected_output": "2"},
            {"input_text": "[[\"1\"], [\"0\"], [\"1\"]]", "expected_output": "2"},
            {"input_text": "[[\"1\", \"1\"], [\"1\", \"1\"]]", "expected_output": "1"},
            {"input_text": "[[\"1\", \"0\", \"1\", \"0\", \"1\"]]", "expected_output": "3"},
            {"input_text": "[[\"0\", \"0\", \"0\"], [\"0\", \"0\", \"0\"]]", "expected_output": "0"},
            {"input_text": "[[\"1\", \"0\", \"0\"], [\"0\", \"1\", \"0\"], [\"0\", \"0\", \"1\"]]", "expected_output": "3"},
            {"input_text": "[[\"1\", \"1\", \"1\"], [\"0\", \"1\", \"0\"], [\"1\", \"1\", \"1\"]]", "expected_output": "1"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Scan every cell of the grid. Whenever you find '1', increment island count and sink the island.", "xp_cost": 2},
            {"level": 2, "text": "Sinking the island means setting all 4-directionally connected '1's to '0' via traversal.", "xp_cost": 5},
            {"level": 3, "text": "Use Depth-First Search (DFS) or Breadth-First Search (BFS) to flood all connected land cells.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Connected Components DFS\n\nIterate over every cell `(r, c)`. If `grid[r][c] == '1'`, increment `count` and trigger DFS to mark all connected land cells as `'0'`.\n\n#### Complexity\n- **Time Complexity:** $O(m \\cdot n)$ each cell visited at most constant times.\n- **Space Complexity:** $O(m \\cdot n)$ recursion call stack.\n\n#### Common Pitfalls\n- Diagonals do NOT connect land cells.",
        "reference_solutions": {
            "brute_python": "def numIslands(grid):\n    if not grid or not grid[0]: return 0\n    grid = [list(r) for r in grid]\n    m, n = len(grid), len(grid[0])\n    count = 0\n    def dfs(r, c):\n        if 0 <= r < m and 0 <= c < n and grid[r][c] == '1':\n            grid[r][c] = '0'\n            dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)\n    for r in range(m):\n        for c in range(n):\n            if grid[r][c] == '1':\n                count += 1\n                dfs(r, c)\n    return count",
            "optimal_python": "def numIslands(grid):\n    if not grid or not grid[0]: return 0\n    grid = [list(r) for r in grid]\n    m, n = len(grid), len(grid[0])\n    count = 0\n    for r in range(m):\n        for c in range(n):\n            if grid[r][c] == '1':\n                count += 1\n                q = [(r, c)]\n                grid[r][c] = '0'\n                while q:\n                    cr, cc = q.pop(0)\n                    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:\n                        nr, nc = cr + dr, cc + dc\n                        if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == '1':\n                            grid[nr][nc] = '0'\n                            q.append((nr, nc))\n    return count",
            "optimal_java": "public class Solution {\n    public int numIslands(char[][] grid) {\n        return 0;\n    }\n}",
            "optimal_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int numIslands(vector<vector<char>>& grid) {\n        return 0;\n    }\n};"
        }
    },

    # 46. Graphs - Medium
    {
        "slug": "course-schedule-cycle-detection",
        "title": "Course Prerequisite Dependency Cycle Detection",
        "difficulty": "medium",
        "topic": "Graphs",
        "tags": ["Graph", "Topological Sort", "BFS"],
        "company_tags": ["Amazon", "Google", "Meta", "Microsoft"],
        "statement_md": "There are a total of `numCourses` courses you have to take, labeled from `0` to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [a, b]` indicates that you must take course `b` first if you want to take course `a`.\n\nReturn `true` if you can finish all courses. Otherwise, return `false`.\n\n### Input Format\n- Line 1: An integer `numCourses`\n- Line 2: A JSON-encoded list of pairs `prerequisites`\n\n### Output Format\n- A boolean value (`true` or `false`)",
        "examples": [
            {
                "input": "2\n[[1, 0]]",
                "output": "true",
                "explanation": "To take course 1 you should take course 0. This is possible."
            },
            {
                "input": "2\n[[1, 0], [0, 1]]",
                "output": "false",
                "explanation": "Mutual dependency forms a directed cycle."
            }
        ],
        "sample_tests": [
            {"input_text": "2\n[[1, 0]]", "expected_output": "true"},
            {"input_text": "2\n[[1, 0], [0, 1]]", "expected_output": "false"},
            {"input_text": "1\n[]", "expected_output": "true"}
        ],
        "hidden_tests": [
            {"input_text": "3\n[[0, 1], [0, 2], [1, 2]]", "expected_output": "true"},
            {"input_text": "3\n[[0, 1], [1, 2], [2, 0]]", "expected_output": "false"},
            {"input_text": "4\n[[1, 0], [2, 0], [3, 1], [3, 2]]", "expected_output": "true"},
            {"input_text": "4\n[[1, 0], [2, 1], [3, 2], [1, 3]]", "expected_output": "false"},
            {"input_text": "5\n[]", "expected_output": "true"},
            {"input_text": "5\n[[1, 0], [2, 1], [3, 2], [4, 3]]", "expected_output": "true"},
            {"input_text": "3\n[[1, 0], [2, 1]]", "expected_output": "true"},
            {"input_text": "4\n[[0, 1], [2, 3], [1, 2], [3, 0]]", "expected_output": "false"},
            {"input_text": "2\n[[1, 0], [1, 0]]", "expected_output": "true"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "This problem is equivalent to detecting if a directed graph contains a cycle.", "xp_cost": 2},
            {"level": 2, "text": "Compute the in-degree of every node. Nodes with in-degree 0 can be taken immediately.", "xp_cost": 5},
            {"level": 3, "text": "Use Kahn's Algorithm for Topological Sort with a Queue and in-degree array.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Kahn's Topological Sort (BFS)\n\nBuild adjacency list and compute `in_degree` for all courses. Initialize queue with courses having `in_degree == 0`. Decrement neighbors' in-degree; when a neighbor reaches 0, push to queue. If processed courses count equals `numCourses`, no cycle exists.\n\n#### Complexity\n- **Time Complexity:** $O(V + E)$ where $V = \\text{numCourses}$ and $E = \\text{len}(prerequisites)$.\n- **Space Complexity:** $O(V + E)$ graph representation.\n\n#### Common Pitfalls\n- Handling disconnected components (resolved by enqueuing all 0 in-degree nodes).",
        "reference_solutions": {
            "brute_python": "def canFinish(numCourses, prerequisites):\n    from collections import defaultdict\n    graph = defaultdict(list)\n    for u, v in prerequisites:\n        graph[v].append(u)\n    visited = [0] * numCourses\n    def has_cycle(node):\n        if visited[node] == 1: return True\n        if visited[node] == 2: return False\n        visited[node] = 1\n        for nbr in graph[node]:\n            if has_cycle(nbr): return True\n        visited[node] = 2\n        return False\n    for i in range(numCourses):\n        if has_cycle(i): return False\n    return True",
            "optimal_python": "def canFinish(numCourses, prerequisites):\n    from collections import defaultdict, deque\n    graph = defaultdict(list)\n    in_degree = [0] * numCourses\n    for u, v in prerequisites:\n        graph[v].append(u)\n        in_degree[u] += 1\n    q = deque([i for i in range(numCourses) if in_degree[i] == 0])\n    processed = 0\n    while q:\n        curr = q.popleft()\n        processed += 1\n        for nbr in graph[curr]:\n            in_degree[nbr] -= 1\n            if in_degree[nbr] == 0:\n                q.append(nbr)\n    return processed == numCourses",
            "optimal_java": "public class Solution {\n    public boolean canFinish(int numCourses, int[][] prerequisites) {\n        return true;\n    }\n}",
            "optimal_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {\n        return true;\n    }\n};"
        }
    },

    # 47. Graphs - Medium
    {
        "slug": "rotting-grid-infection-time",
        "title": "Rotting Orange Grid Infection Time",
        "difficulty": "medium",
        "topic": "Graphs",
        "tags": ["Breadth-First Search", "Matrix", "Graph"],
        "company_tags": ["Amazon", "Microsoft", "Meta", "Google"],
        "statement_md": "You are given an `m x n` grid where each cell can have one of three values:\n- `0` representing an empty cell,\n- `1` representing a fresh orange, or\n- `2` representing a rotten orange.\n\nEvery minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.\n\nReturn the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return `-1`.\n\n### Input Format\n- A JSON-encoded 2D list of integers `grid`\n\n### Output Format\n- An integer representing elapsed minutes or -1",
        "examples": [
            {
                "input": "[[2, 1, 1], [1, 1, 0], [0, 1, 1]]",
                "output": "4",
                "explanation": "Takes 4 minutes for all oranges to rot."
            },
            {
                "input": "[[2, 1, 1], [0, 1, 1], [1, 0, 1]]",
                "output": "-1",
                "explanation": "The orange in bottom left corner is isolated and never rots."
            }
        ],
        "sample_tests": [
            {"input_text": "[[2, 1, 1], [1, 1, 0], [0, 1, 1]]", "expected_output": "4"},
            {"input_text": "[[2, 1, 1], [0, 1, 1], [1, 0, 1]]", "expected_output": "-1"},
            {"input_text": "[[0, 2]]", "expected_output": "0"}
        ],
        "hidden_tests": [
            {"input_text": "[[1]]", "expected_output": "-1"},
            {"input_text": "[[0]]", "expected_output": "0"},
            {"input_text": "[[2]]", "expected_output": "0"},
            {"input_text": "[[2, 2], [1, 1]]", "expected_output": "1"},
            {"input_text": "[[2, 1, 1], [1, 1, 1], [0, 1, 2]]", "expected_output": "2"},
            {"input_text": "[[1, 2]]", "expected_output": "1"},
            {"input_text": "[[0, 1]]", "expected_output": "-1"},
            {"input_text": "[[2, 1, 1, 1, 1, 1]]", "expected_output": "5"},
            {"input_text": "[[2, 2, 2], [2, 2, 2]]", "expected_output": "0"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "All rotten oranges begin spreading at minute 0 simultaneously.", "xp_cost": 2},
            {"level": 2, "text": "Enqueue all initial rotten oranges at minute 0 and track the count of fresh oranges.", "xp_cost": 5},
            {"level": 3, "text": "Use Multi-Source Breadth-First Search (BFS) with a Queue.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Multi-Source BFS\n\nEnqueue all rotten oranges (2) into a queue. Count fresh oranges. Run BFS level by level; each level corresponds to 1 elapsed minute. When a fresh orange rots, decrement fresh count. Return elapsed minutes if `fresh == 0`, else -1.\n\n#### Complexity\n- **Time Complexity:** $O(m \\cdot n)$ each cell processed once.\n- **Space Complexity:** $O(m \\cdot n)$ queue storage.\n\n#### Common Pitfalls\n- Returning 1 minute even when there were 0 fresh oranges initially.",
        "reference_solutions": {
            "brute_python": "def orangesRotting(grid):\n    m, n = len(grid), len(grid[0])\n    q = []\n    fresh = 0\n    for r in range(m):\n        for c in range(n):\n            if grid[r][c] == 2: q.append((r, c, 0))\n            elif grid[r][c] == 1: fresh += 1\n    time = 0\n    while q:\n        r, c, d = q.pop(0)\n        time = max(time, d)\n        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:\n            nr, nc = r + dr, c + dc\n            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:\n                grid[nr][nc] = 2\n                fresh -= 1\n                q.append((nr, nc, d + 1))\n    return time if fresh == 0 else -1",
            "optimal_python": "def orangesRotting(grid):\n    m, n = len(grid), len(grid[0])\n    from collections import deque\n    q = deque()\n    fresh = 0\n    for r in range(m):\n        for c in range(n):\n            if grid[r][c] == 2:\n                q.append((r, c))\n            elif grid[r][c] == 1:\n                fresh += 1\n    if fresh == 0: return 0\n    minutes = -1\n    while q:\n        minutes += 1\n        for _ in range(len(q)):\n            r, c = q.popleft()\n            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:\n                nr, nc = r + dr, c + dc\n                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:\n                    grid[nr][nc] = 2\n                    fresh -= 1\n                    q.append((nr, nc))\n    return minutes if fresh == 0 else -1",
            "optimal_java": "public class Solution {\n    public int orangesRotting(int[][] grid) {\n        return 0;\n    }\n}",
            "optimal_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int orangesRotting(vector<vector<int>>& grid) {\n        return 0;\n    }\n};"
        }
    },

    # 48. Graphs - Hard
    {
        "slug": "word-ladder-shortest-path",
        "title": "Word Ladder Shortest Mutation Path",
        "difficulty": "hard",
        "topic": "Graphs",
        "tags": ["Breadth-First Search", "Hash Table", "String"],
        "company_tags": ["Amazon", "Google", "Meta", "LinkedIn"],
        "statement_md": "A transformation sequence from word `beginWord` to word `endWord` using a dictionary `wordList` is a sequence of words `beginWord -> s1 -> s2 -> ... -> sk` such that:\n- Every adjacent pair of words differs by a single letter.\n- Every `si` for `1 <= i <= k` is in `wordList`.\n- `sk == endWord`.\n\nGiven two words, `beginWord` and `endWord`, and a dictionary `wordList`, return the number of words in the shortest transformation sequence from `beginWord` to `endWord`, or `0` if no such sequence exists.\n\n### Input Format\n- Line 1: String `beginWord`\n- Line 2: String `endWord`\n- Line 3: A JSON-encoded list of strings `wordList`\n\n### Output Format\n- An integer representing the sequence length",
        "examples": [
            {
                "input": "\"hit\"\n\"cog\"\n[\"hot\", \"dot\", \"dog\", \"lot\", \"log\", \"cog\"]",
                "output": "5",
                "explanation": "Shortest transformation is \"hit\" -> \"hot\" -> \"dot\" -> \"dog\" -> \"cog\", 5 words."
            },
            {
                "input": "\"hit\"\n\"cog\"\n[\"hot\", \"dot\", \"dog\", \"lot\", \"log\"]",
                "output": "0",
                "explanation": "\"cog\" is not in wordList, so no valid sequence exists."
            }
        ],
        "sample_tests": [
            {"input_text": "\"hit\"\n\"cog\"\n[\"hot\", \"dot\", \"dog\", \"lot\", \"log\", \"cog\"]", "expected_output": "5"},
            {"input_text": "\"hit\"\n\"cog\"\n[\"hot\", \"dot\", \"dog\", \"lot\", \"log\"]", "expected_output": "0"},
            {"input_text": "\"a\"\n\"c\"\n[\"a\", \"b\", \"c\"]", "expected_output": "2"}
        ],
        "hidden_tests": [
            {"input_text": "\"hot\"\n\"dog\"\n[\"hot\", \"dog\"]", "expected_output": "0"},
            {"input_text": "\"hot\"\n\"dog\"\n[\"hot\", \"dot\", \"dog\"]", "expected_output": "3"},
            {"input_text": "\"game\"\n\"thee\"\n[\"came\", \"case\", \"cast\", \"cost\", \"most\", \"host\", \"hose\", \"hoes\", \"thee\"]", "expected_output": "0"},
            {"input_text": "\"cat\"\n\"hat\"\n[\"hat\"]", "expected_output": "2"},
            {"input_text": "\"lead\"\n\"gold\"\n[\"load\", \"goad\", \"gold\"]", "expected_output": "4"},
            {"input_text": "\"kiss\"\n\"tusk\"\n[\"miss\", \"diss\", \"disk\", \"dusk\", \"tusk\"]", "expected_output": "5"},
            {"input_text": "\"ab\"\n\"cd\"\n[\"cb\", \"cd\"]", "expected_output": "3"},
            {"input_text": "\"red\"\n\"tax\"\n[\"ted\", \"tex\", \"red\", \"tax\", \"tad\", \"den\", \"rex\", \"pee\"]", "expected_output": "4"},
            {"input_text": "\"qa\"\n\"sq\"\n[\"si\", \"go\", \"se\", \"cm\", \"so\", \"ph\", \"mt\", \"db\", \"mb\", \"sb\", \"kr\", \"ln\", \"tm\", \"le\", \"av\", \"sm\", \"ar\", \"ci\", \"ca\", \"br\", \"ti\", \"ba\", \"to\", \"ra\", \"fa\", \"yo\", \"ow\", \"sn\", \"ya\", \"cr\", \"po\", \"fe\", \"ho\", \"ma\", \"re\", \"or\", \"rn\", \"bha\", \"co\", \"pa\", \"sq\"]", "expected_output": "5"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Model each word as a graph vertex and each single-letter difference as an unweighted edge.", "xp_cost": 2},
            {"level": 2, "text": "To find the shortest path in an unweighted graph, standard BFS guarantees finding the minimum number of transitions.", "xp_cost": 5},
            {"level": 3, "text": "Use Breadth-First Search (BFS) or Bidirectional BFS with a word set.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Bidirectional BFS\n\nSearch simultaneously from `beginWord` and `endWord`. Expand the smaller frontier at each step by substituting all 26 lowercase characters at each position. When frontiers intersect, return total steps.\n\n#### Complexity\n- **Time Complexity:** $O(M^2 \\cdot N)$ where $M$ is word length and $N$ is dictionary size.\n- **Space Complexity:** $O(M \\cdot N)$ storage for word set.\n\n#### Common Pitfalls\n- Not verifying whether `endWord` exists in `wordList` upfront.",
        "reference_solutions": {
            "brute_python": "def ladderLength(beginWord, endWord, wordList):\n    words = set(wordList)\n    if endWord not in words: return 0\n    q = [(beginWord, 1)]\n    visited = {beginWord}\n    while q:\n        word, dist = q.pop(0)\n        if word == endWord: return dist\n        for i in range(len(word)):\n            for c in 'abcdefghijklmnopqrstuvwxyz':\n                nxt = word[:i] + c + word[i+1:]\n                if nxt in words and nxt not in visited:\n                    visited.add(nxt)\n                    q.append((nxt, dist + 1))\n    return 0",
            "optimal_python": "def ladderLength(beginWord, endWord, wordList):\n    words = set(wordList)\n    if endWord not in words: return 0\n    from collections import deque\n    q = deque([(beginWord, 1)])\n    visited = {beginWord}\n    while q:\n        word, dist = q.popleft()\n        if word == endWord: return dist\n        for i in range(len(word)):\n            for c in 'abcdefghijklmnopqrstuvwxyz':\n                nxt = word[:i] + c + word[i+1:]\n                if nxt in words and nxt not in visited:\n                    visited.add(nxt)\n                    q.append((nxt, dist + 1))\n    return 0",
            "optimal_java": "public class Solution {\n    public int ladderLength(String beginWord, String endWord, List<String> wordList) {\n        return 0;\n    }\n}",
            "optimal_cpp": "#include <string>\n#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int ladderLength(string beginWord, string endWord, vector<string>& wordList) {\n        return 0;\n    }\n};"
        }
    },

    # 49. Binary Search - Easy
    {
        "slug": "standard-binary-search-exact",
        "title": "Exact Target Binary Search",
        "difficulty": "easy",
        "topic": "Binary Search",
        "tags": ["Binary Search", "Array"],
        "company_tags": ["Amazon", "Google", "Microsoft"],
        "statement_md": "Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`.\n\nIf `target` exists, then return its index. Otherwise, return `-1`.\n\nYou must write an algorithm with `O(log n)` runtime complexity.\n\n### Input Format\n- Line 1: A JSON-encoded list of sorted integers `nums`\n- Line 2: Integer `target`\n\n### Output Format\n- An integer representing index or -1",
        "examples": [
            {
                "input": "[-1, 0, 3, 5, 9, 12]\n9",
                "output": "4",
                "explanation": "9 exists in nums and its index is 4."
            },
            {
                "input": "[-1, 0, 3, 5, 9, 12]\n2",
                "output": "-1",
                "explanation": "2 does not exist in nums so return -1."
            }
        ],
        "sample_tests": [
            {"input_text": "[-1, 0, 3, 5, 9, 12]\n9", "expected_output": "4"},
            {"input_text": "[-1, 0, 3, 5, 9, 12]\n2", "expected_output": "-1"},
            {"input_text": "[5]\n5", "expected_output": "0"}
        ],
        "hidden_tests": [
            {"input_text": "[]\n5", "expected_output": "-1"},
            {"input_text": "[5]\n1", "expected_output": "-1"},
            {"input_text": "[1, 3, 5, 7, 9]\n1", "expected_output": "0"},
            {"input_text": "[1, 3, 5, 7, 9]\n9", "expected_output": "4"},
            {"input_text": "[1, 3, 5, 7, 9]\n5", "expected_output": "2"},
            {"input_text": "[-10, -5, 0, 5, 10]\n-10", "expected_output": "0"},
            {"input_text": "[-10, -5, 0, 5, 10]\n10", "expected_output": "4"},
            {"input_text": "[-10, -5, 0, 5, 10]\n0", "expected_output": "2"},
            {"input_text": "[2, 4, 6, 8, 10, 12]\n7", "expected_output": "-1"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Divide the search interval in half by calculating mid = left + (right - left) // 2.", "xp_cost": 2},
            {"level": 2, "text": "Compare target with nums[mid]: adjust left = mid + 1 or right = mid - 1.", "xp_cost": 5},
            {"level": 3, "text": "Use Binary Search with while left <= right.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Classical Binary Search\n\nMaintain `left = 0` and `right = len(nums) - 1`. While `left <= right`, compute `mid = (left + right) // 2`. If `nums[mid] == target`, return `mid`. If smaller, `left = mid + 1`. If larger, `right = mid - 1`.\n\n#### Complexity\n- **Time Complexity:** $O(\\log n)$ logarithmic halving.\n- **Space Complexity:** $O(1)$ constant memory.\n\n#### Common Pitfalls\n- Integer overflow with `(left + right) / 2` in typed languages (use `left + (right - left) / 2`).",
        "reference_solutions": {
            "brute_python": "def search(nums, target):\n    for i, x in enumerate(nums):\n        if x == target: return i\n    return -1",
            "optimal_python": "def search(nums, target):\n    left, right = 0, len(nums) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if nums[mid] == target: return mid\n        elif nums[mid] < target: left = mid + 1\n        else: right = mid - 1\n    return -1",
            "optimal_java": "public class Solution {\n    public int search(int[] nums, int target) {\n        int l = 0, r = nums.length - 1;\n        while (l <= r) {\n            int m = l + (r - l) / 2;\n            if (nums[m] == target) return m;\n            else if (nums[m] < target) l = m + 1;\n            else r = m - 1;\n        }\n        return -1;\n    }\n}",
            "optimal_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int search(vector<int>& nums, int target) {\n        int l = 0, r = (int)nums.size() - 1;\n        while (l <= r) {\n            int m = l + (r - l) / 2;\n            if (nums[m] == target) return m;\n            else if (nums[m] < target) l = m + 1;\n            else r = m - 1;\n        }\n        return -1;\n    }\n};"
        }
    },

    # 50. Binary Search - Easy
    {
        "slug": "first-and-last-position-in-sorted-array",
        "title": "First and Last Position of Element in Sorted Array",
        "difficulty": "easy",
        "topic": "Binary Search",
        "tags": ["Binary Search", "Array"],
        "company_tags": ["Meta", "Google", "Amazon", "Microsoft"],
        "statement_md": "Given an array of integers `nums` sorted in non-decreasing order, find the starting and ending position of a given `target` value.\n\nIf `target` is not found in the array, return `[-1, -1]`.\n\nYou must write an algorithm with `O(log n)` runtime complexity.\n\n### Input Format\n- Line 1: A JSON-encoded list of sorted integers `nums`\n- Line 2: Integer `target`\n\n### Output Format\n- A JSON-encoded list of two integers `[start, end]`",
        "examples": [
            {
                "input": "[5, 7, 7, 8, 8, 10]\n8",
                "output": "[3, 4]",
                "explanation": "8 appears from index 3 to index 4."
            },
            {
                "input": "[5, 7, 7, 8, 8, 10]\n6",
                "output": "[-1, -1]",
                "explanation": "6 is not in the array."
            }
        ],
        "sample_tests": [
            {"input_text": "[5, 7, 7, 8, 8, 10]\n8", "expected_output": "[3, 4]"},
            {"input_text": "[5, 7, 7, 8, 8, 10]\n6", "expected_output": "[-1, -1]"},
            {"input_text": "[]\n0", "expected_output": "[-1, -1]"}
        ],
        "hidden_tests": [
            {"input_text": "[1]\n1", "expected_output": "[0, 0]"},
            {"input_text": "[1]\n2", "expected_output": "[-1, -1]"},
            {"input_text": "[2, 2]\n2", "expected_output": "[0, 1]"},
            {"input_text": "[1, 2, 3, 3, 3, 3, 4]\n3", "expected_output": "[2, 5]"},
            {"input_text": "[1, 1, 1, 1, 1]\n1", "expected_output": "[0, 4]"},
            {"input_text": "[-5, -5, -3, 0, 2]\n-5", "expected_output": "[0, 1]"},
            {"input_text": "[10, 20, 30, 40]\n20", "expected_output": "[1, 1]"},
            {"input_text": "[0, 0, 1, 2, 2]\n2", "expected_output": "[3, 4]"},
            {"input_text": "[1, 2, 3, 4, 5]\n0", "expected_output": "[-1, -1]"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Execute two separate binary searches: one for the leftmost index and one for the rightmost index.", "xp_cost": 2},
            {"level": 2, "text": "To find the left bound, when nums[mid] == target, continue searching in left half: right = mid - 1.", "xp_cost": 5},
            {"level": 3, "text": "Use Binary Search with Lower Bound and Upper Bound variants.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Dual Binary Searches\n\nRun `find_bound(is_first)`: when `nums[mid] == target`, record `mid` as candidate and narrow search either to left (`right = mid - 1`) or right (`left = mid + 1`).\n\n#### Complexity\n- **Time Complexity:** $2 \\cdot O(\\log n) = O(\\log n)$ time.\n- **Space Complexity:** $O(1)$ constant memory.\n\n#### Common Pitfalls\n- Linear expansion from mid upon finding target ($O(n)$ worst case if all elements identical).",
        "reference_solutions": {
            "brute_python": "def searchRange(nums, target):\n    first, last = -1, -1\n    for i, x in enumerate(nums):\n        if x == target:\n            if first == -1: first = i\n            last = i\n    return [first, last]",
            "optimal_python": "def searchRange(nums, target):\n    def find_bound(first):\n        l, r = 0, len(nums) - 1\n        ans = -1\n        while l <= r:\n            m = (l + r) // 2\n            if nums[m] == target:\n                ans = m\n                if first: r = m - 1\n                else: l = m + 1\n            elif nums[m] < target: l = m + 1\n            else: r = m - 1\n        return ans\n    return [find_bound(True), find_bound(False)]",
            "optimal_java": "public class Solution {\n    public int[] searchRange(int[] nums, int target) {\n        return new int[]{-1, -1};\n    }\n}",
            "optimal_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> searchRange(vector<int>& nums, int target) {\n        return {-1, -1};\n    }\n};"
        }
    },

    # 51. Binary Search - Medium
    {
        "slug": "search-in-rotated-sorted-array-distinct",
        "title": "Search in Rotated Sorted Array with Distinct Values",
        "difficulty": "medium",
        "topic": "Binary Search",
        "tags": ["Binary Search", "Array"],
        "company_tags": ["Amazon", "Microsoft", "Meta", "Google"],
        "statement_md": "There is an integer array `nums` sorted in ascending order (with distinct values).\n\nPrior to being passed to your function, `nums` is possibly rotated at an unknown pivot index `k` (`1 <= k < nums.length`) such that the resulting array is `[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]`.\n\nGiven the array `nums` after the possible rotation and an integer `target`, return the index of `target` if it is in `nums`, or `-1` if it is not in `nums`.\n\nYou must write an algorithm with `O(log n)` runtime complexity.\n\n### Input Format\n- Line 1: A JSON-encoded list of integers `nums`\n- Line 2: Integer `target`\n\n### Output Format\n- An integer representing index or -1",
        "examples": [
            {
                "input": "[4, 5, 6, 7, 0, 1, 2]\n0",
                "output": "4",
                "explanation": "0 is found at index 4."
            },
            {
                "input": "[4, 5, 6, 7, 0, 1, 2]\n3",
                "output": "-1",
                "explanation": "3 is not in nums."
            }
        ],
        "sample_tests": [
            {"input_text": "[4, 5, 6, 7, 0, 1, 2]\n0", "expected_output": "4"},
            {"input_text": "[4, 5, 6, 7, 0, 1, 2]\n3", "expected_output": "-1"},
            {"input_text": "[1]\n0", "expected_output": "-1"}
        ],
        "hidden_tests": [
            {"input_text": "[1]\n1", "expected_output": "0"},
            {"input_text": "[3, 1]\n1", "expected_output": "1"},
            {"input_text": "[3, 1]\n3", "expected_output": "0"},
            {"input_text": "[5, 1, 3]\n5", "expected_output": "0"},
            {"input_text": "[4, 5, 6, 7, 8, 1, 2, 3]\n8", "expected_output": "4"},
            {"input_text": "[6, 7, 1, 2, 3, 4, 5]\n6", "expected_output": "0"},
            {"input_text": "[6, 7, 1, 2, 3, 4, 5]\n3", "expected_output": "4"},
            {"input_text": "[1, 2, 3, 4, 5]\n4", "expected_output": "3"},
            {"input_text": "[8, 9, 2, 3, 4]\n9", "expected_output": "1"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "In any rotated sorted array, dividing at mid produces at least one strictly sorted half.", "xp_cost": 2},
            {"level": 2, "text": "Determine which half is sorted: if nums[left] <= nums[mid], left half is sorted; else right half is sorted.", "xp_cost": 5},
            {"level": 3, "text": "Use Modified Binary Search checking if target falls within the bounds of the sorted half.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Partitioned Binary Search\n\nCalculate `mid`. If `nums[left] <= nums[mid]`, left half is sorted. Check if `nums[left] <= target < nums[mid]`: if so, search left (`right = mid - 1`); else search right (`left = mid + 1`). Otherwise, right half is sorted: check if `nums[mid] < target <= nums[right]` and adjust bounds accordingly.\n\n#### Complexity\n- **Time Complexity:** $O(\\log n)$ single binary search.\n- **Space Complexity:** $O(1)$ constant memory.\n\n#### Common Pitfalls\n- Non-strict inequality when checking target range in sorted half.",
        "reference_solutions": {
            "brute_python": "def search(nums, target):\n    for i, x in enumerate(nums):\n        if x == target: return i\n    return -1",
            "optimal_python": "def search(nums, target):\n    l, r = 0, len(nums) - 1\n    while l <= r:\n        m = (l + r) // 2\n        if nums[m] == target: return m\n        if nums[l] <= nums[m]:\n            if nums[l] <= target < nums[m]: r = m - 1\n            else: l = m + 1\n        else:\n            if nums[m] < target <= nums[r]: l = m + 1\n            else: r = m - 1\n    return -1",
            "optimal_java": "public class Solution {\n    public int search(int[] nums, int target) {\n        return -1;\n    }\n}",
            "optimal_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int search(vector<int>& nums, int target) {\n        return -1;\n    }\n};"
        }
    },

    # 52. Binary Search - Hard
    {
        "slug": "median-of-two-sorted-arrays-log-time",
        "title": "Median of Two Sorted Arrays in Logarithmic Time",
        "difficulty": "hard",
        "topic": "Binary Search",
        "tags": ["Binary Search", "Array", "Divide and Conquer"],
        "company_tags": ["Google", "Amazon", "Meta", "Microsoft"],
        "statement_md": "Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the median of the two sorted arrays.\n\nThe overall run time complexity should be `O(log(m + n))`.\n\n### Input Format\n- Line 1: A JSON-encoded list of integers `nums1`\n- Line 2: A JSON-encoded list of integers `nums2`\n\n### Output Format\n- A floating-point number representing the median",
        "examples": [
            {
                "input": "[1, 3]\n[2]",
                "output": "2.0",
                "explanation": "Merged array = [1, 2, 3] and median is 2.0."
            },
            {
                "input": "[1, 2]\n[3, 4]",
                "output": "2.5",
                "explanation": "Merged array = [1, 2, 3, 4] and median is (2 + 3) / 2 = 2.5."
            }
        ],
        "sample_tests": [
            {"input_text": "[1, 3]\n[2]", "expected_output": "2.0"},
            {"input_text": "[1, 2]\n[3, 4]", "expected_output": "2.5"},
            {"input_text": "[0, 0]\n[0, 0]", "expected_output": "0.0"}
        ],
        "hidden_tests": [
            {"input_text": "[]\n[1]", "expected_output": "1.0"},
            {"input_text": "[2]\n[]", "expected_output": "2.0"},
            {"input_text": "[1, 2]\n[1, 2, 3]", "expected_output": "2.0"},
            {"input_text": "[1, 3, 5]\n[2, 4, 6]", "expected_output": "3.5"},
            {"input_text": "[1, 2, 3, 4, 5, 6, 7, 8]\n[1, 2, 3, 4, 5]", "expected_output": "4.0"},
            {"input_text": "[-5, -3, -1]\n[-2, 0, 2]", "expected_output": "-1.5"},
            {"input_text": "[100]\n[1000]", "expected_output": "550.0"},
            {"input_text": "[1, 2, 6]\n[3, 4, 5]", "expected_output": "3.5"},
            {"input_text": "[1, 2]\n[-1, 3]", "expected_output": "1.5"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Binary search on the partition cut index of the smaller array.", "xp_cost": 2},
            {"level": 2, "text": "Partition both arrays such that the total elements in left halves equals (m + n + 1) // 2.", "xp_cost": 5},
            {"level": 3, "text": "Use Binary Search on Partitions verifying max_left_A <= min_right_B and max_left_B <= min_right_A.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Binary Search on Partition\n\nEnsure `nums1` is the shorter array. Binary search partition `i` in `nums1`, with `j = (m + n + 1) // 2 - i` in `nums2`. Validate that `nums1[i-1] <= nums2[j]` and `nums2[j-1] <= nums1[i]`. Compute median from maximum of lefts and minimum of rights.\n\n#### Complexity\n- **Time Complexity:** $O(\\log(\\min(m, n)))$ binary search on smaller length.\n- **Space Complexity:** $O(1)$ constant memory.\n\n#### Common Pitfalls\n- Boundary checks when `i` or `j` is at index 0 or array length (use $\\pm \\infty$).",
        "reference_solutions": {
            "brute_python": "def findMedianSortedArrays(nums1, nums2):\n    merged = sorted(nums1 + nums2)\n    n = len(merged)\n    if n % 2 == 1: return float(merged[n // 2])\n    return (merged[n // 2 - 1] + merged[n // 2]) / 2.0",
            "optimal_python": "def findMedianSortedArrays(nums1, nums2):\n    if len(nums1) > len(nums2):\n        nums1, nums2 = nums2, nums1\n    m, n = len(nums1), len(nums2)\n    low, high = 0, m\n    while low <= high:\n        i = (low + high) // 2\n        j = (m + n + 1) // 2 - i\n        max_left1 = float('-inf') if i == 0 else nums1[i - 1]\n        min_right1 = float('inf') if i == m else nums1[i]\n        max_left2 = float('-inf') if j == 0 else nums2[j - 1]\n        min_right2 = float('inf') if j == n else nums2[j]\n        if max_left1 <= min_right2 and max_left2 <= min_right1:\n            if (m + n) % 2 == 1:\n                return float(max(max_left1, max_left2))\n            return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2.0\n        elif max_left1 > min_right2:\n            high = i - 1\n        else:\n            low = i + 1\n    return 0.0",
            "optimal_java": "public class Solution {\n    public double findMedianSortedArrays(int[] nums1, int[] nums2) {\n        return 0.0;\n    }\n}",
            "optimal_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {\n        return 0.0;\n    }\n};"
        }
    },

    # 53. Dynamic Programming - Easy
    {
        "slug": "climbing-step-variations",
        "title": "Distinct Ways to Climb Stair Steps",
        "difficulty": "easy",
        "topic": "Dynamic Programming",
        "tags": ["Dynamic Programming", "Math", "Memoization"],
        "company_tags": ["Amazon", "Google", "Apple", "Adobe"],
        "statement_md": "You are climbing a staircase. It takes `n` steps to reach the top.\n\nEach time you can either climb `1` or `2` steps. In how many distinct ways can you climb to the top?\n\n### Input Format\n- An integer `n` (`1 <= n <= 45`)\n\n### Output Format\n- An integer representing distinct combinations",
        "examples": [
            {
                "input": "2",
                "output": "2",
                "explanation": "There are two ways: (1 step + 1 step) or (2 steps)."
            },
            {
                "input": "3",
                "output": "3",
                "explanation": "Three ways: (1+1+1), (1+2), (2+1)."
            }
        ],
        "sample_tests": [
            {"input_text": "2", "expected_output": "2"},
            {"input_text": "3", "expected_output": "3"},
            {"input_text": "1", "expected_output": "1"}
        ],
        "hidden_tests": [
            {"input_text": "4", "expected_output": "5"},
            {"input_text": "5", "expected_output": "8"},
            {"input_text": "6", "expected_output": "13"},
            {"input_text": "7", "expected_output": "21"},
            {"input_text": "10", "expected_output": "89"},
            {"input_text": "15", "expected_output": "987"},
            {"input_text": "20", "expected_output": "10946"},
            {"input_text": "30", "expected_output": "1346269"},
            {"input_text": "35", "expected_output": "14930352"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "To reach step n, you can either step from n - 1 or jump from n - 2.", "xp_cost": 2},
            {"level": 2, "text": "Recurrence relation: ways(n) = ways(n - 1) + ways(n - 2).", "xp_cost": 5},
            {"level": 3, "text": "Use 1D Dynamic Programming with two variables representing the previous two steps.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: 1D Fibonacci DP\n\nBase cases `dp[1] = 1, dp[2] = 2`. Transition `dp[i] = dp[i-1] + dp[i-2]`. Maintain two rolling state variables `a` and `b`.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ single linear pass.\n- **Space Complexity:** $O(1)$ constant memory.\n\n#### Common Pitfalls\n- Naive recursion without memoization leading to exponential $O(2^n)$ TLE.",
        "reference_solutions": {
            "brute_python": "def climbStairs(n):\n    if n <= 2: return n\n    a, b = 1, 2\n    for _ in range(3, n + 1):\n        a, b = b, a + b\n    return b",
            "optimal_python": "def climbStairs(n):\n    if n <= 2: return n\n    a, b = 1, 2\n    for _ in range(3, n + 1):\n        a, b = b, a + b\n    return b",
            "optimal_java": "public class Solution {\n    public int climbStairs(int n) {\n        if (n <= 2) return n;\n        int a = 1, b = 2;\n        for (int i = 3; i <= n; i++) {\n            int c = a + b;\n            a = b;\n            b = c;\n        }\n        return b;\n    }\n}",
            "optimal_cpp": "class Solution {\npublic:\n    int climbStairs(int n) {\n        if (n <= 2) return n;\n        int a = 1, b = 2;\n        for (int i = 3; i <= n; i++) {\n            int c = a + b;\n            a = b;\n            b = c;\n        }\n        return b;\n    }\n};"
        }
    },

    # 54. Dynamic Programming - Medium
    {
        "slug": "house-robber-non-adjacent-cache",
        "title": "House Robber Non-Adjacent Value Maximization",
        "difficulty": "medium",
        "topic": "Dynamic Programming",
        "tags": ["Dynamic Programming", "Array"],
        "company_tags": ["Amazon", "Google", "Meta", "Microsoft"],
        "statement_md": "You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night.\n\nGiven an integer array `nums` representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.\n\n### Input Format\n- A JSON-encoded list of integers `nums`\n\n### Output Format\n- An integer representing maximum loot",
        "examples": [
            {
                "input": "[1, 2, 3, 1]",
                "output": "4",
                "explanation": "Rob house 1 (money = 1) and then rob house 3 (money = 3). Total = 1 + 3 = 4."
            },
            {
                "input": "[2, 7, 9, 3, 1]",
                "output": "12",
                "explanation": "Rob house 1 (2), house 3 (9), and house 5 (1). Total = 2 + 9 + 1 = 12."
            }
        ],
        "sample_tests": [
            {"input_text": "[1, 2, 3, 1]", "expected_output": "4"},
            {"input_text": "[2, 7, 9, 3, 1]", "expected_output": "12"},
            {"input_text": "[0]", "expected_output": "0"}
        ],
        "hidden_tests": [
            {"input_text": "[]", "expected_output": "0"},
            {"input_text": "[5]", "expected_output": "5"},
            {"input_text": "[2, 1]", "expected_output": "2"},
            {"input_text": "[1, 2, 1, 1]", "expected_output": "3"},
            {"input_text": "[2, 1, 1, 2]", "expected_output": "4"},
            {"input_text": "[100, 1, 1, 100]", "expected_output": "200"},
            {"input_text": "[5, 3, 4, 11, 2]", "expected_output": "16"},
            {"input_text": "[10, 20, 30, 40, 50, 60]", "expected_output": "120"},
            {"input_text": "[0, 0, 0, 0]", "expected_output": "0"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "At each house i, you choose between robbing it (nums[i] + rob(i - 2)) or skipping it (rob(i - 1)).", "xp_cost": 2},
            {"level": 2, "text": "Transition: dp[i] = max(dp[i - 1], dp[i - 2] + nums[i]).", "xp_cost": 5},
            {"level": 3, "text": "Use 1D Dynamic Programming with rolling variables prev1 and prev2.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Rolling State Dynamic Programming\n\nMaintain `prev2 = 0` (max loot up to house $i-2$) and `prev1 = 0` (max loot up to house $i-1$). For each house $x$, `curr = max(prev1, prev2 + x)`. Update `prev2 = prev1` and `prev1 = curr`.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ single pass.\n- **Space Complexity:** $O(1)$ constant memory.\n\n#### Common Pitfalls\n- Boundary conditions with 0 or 1 house.",
        "reference_solutions": {
            "brute_python": "def rob(nums):\n    if not nums: return 0\n    if len(nums) <= 2: return max(nums)\n    dp = [0] * len(nums)\n    dp[0] = nums[0]\n    dp[1] = max(nums[0], nums[1])\n    for i in range(2, len(nums)):\n        dp[i] = max(dp[i-1], dp[i-2] + nums[i])\n    return dp[-1]",
            "optimal_python": "def rob(nums):\n    prev2, prev1 = 0, 0\n    for x in nums:\n        prev2, prev1 = prev1, max(prev1, prev2 + x)\n    return prev1",
            "optimal_java": "public class Solution {\n    public int rob(int[] nums) {\n        int prev2 = 0, prev1 = 0;\n        for (int x : nums) {\n            int curr = Math.max(prev1, prev2 + x);\n            prev2 = prev1;\n            prev1 = curr;\n        }\n        return prev1;\n    }\n}",
            "optimal_cpp": "#include <vector>\n#include <algorithm>\nusing namespace std;\nclass Solution {\npublic:\n    int rob(vector<int>& nums) {\n        int prev2 = 0, prev1 = 0;\n        for (int x : nums) {\n            int curr = max(prev1, prev2 + x);\n            prev2 = prev1;\n            prev1 = curr;\n        }\n        return prev1;\n    }\n};"
        }
    },

    # 55. Dynamic Programming - Medium
    {
        "slug": "coin-change-fewest-coins",
        "title": "Coin Change Minimum Coin Partition",
        "difficulty": "medium",
        "topic": "Dynamic Programming",
        "tags": ["Dynamic Programming", "Breadth-First Search"],
        "company_tags": ["Amazon", "Google", "Microsoft", "Meta"],
        "statement_md": "You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.\n\nReturn the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return `-1`.\n\nYou may assume that you have an infinite number of each kind of coin.\n\n### Input Format\n- Line 1: A JSON-encoded list of integers `coins`\n- Line 2: Integer `amount`\n\n### Output Format\n- An integer representing minimum coins or -1",
        "examples": [
            {
                "input": "[1, 2, 5]\n11",
                "output": "3",
                "explanation": "11 = 5 + 5 + 1 (3 coins)."
            },
            {
                "input": "[2]\n3",
                "output": "-1",
                "explanation": "Cannot form 3 using only coins of denomination 2."
            }
        ],
        "sample_tests": [
            {"input_text": "[1, 2, 5]\n11", "expected_output": "3"},
            {"input_text": "[2]\n3", "expected_output": "-1"},
            {"input_text": "[1]\n0", "expected_output": "0"}
        ],
        "hidden_tests": [
            {"input_text": "[1]\n1", "expected_output": "1"},
            {"input_text": "[1]\n2", "expected_output": "2"},
            {"input_text": "[2, 5, 10, 1]\n27", "expected_output": "4"},
            {"input_text": "[186, 419, 83, 408]\n6249", "expected_output": "20"},
            {"input_text": "[3, 7, 405, 436]\n8839", "expected_output": "25"},
            {"input_text": "[2, 4, 6, 8]\n11", "expected_output": "-1"},
            {"input_text": "[10, 20, 50]\n100", "expected_output": "2"},
            {"input_text": "[1, 3, 4]\n6", "expected_output": "2"},
            {"input_text": "[5, 10, 25]\n30", "expected_output": "2"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "dp[a] represents the minimum coins needed to make amount a.", "xp_cost": 2},
            {"level": 2, "text": "Transition: dp[a] = min(dp[a], 1 + dp[a - coin]) for each coin <= a.", "xp_cost": 5},
            {"level": 3, "text": "Use Unbounded Knapsack Dynamic Programming initialized with infinity.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Bottom-Up Unbounded Knapsack DP\n\nInitialize `dp` table of size `amount + 1` filled with $\\infty$, setting `dp[0] = 0`. For `i` from 1 to `amount` and each `c` in `coins`, if `i >= c`: `dp[i] = min(dp[i], 1 + dp[i - c])`.\n\n#### Complexity\n- **Time Complexity:** $O(A \\cdot C)$ where $A$ is amount and $C$ is number of coins.\n- **Space Complexity:** $O(A)$ DP array.\n\n#### Common Pitfalls\n- Initializing with `amount` instead of `infinity` or `amount + 1`.",
        "reference_solutions": {
            "brute_python": "def coinChange(coins, amount):\n    dp = [float('inf')] * (amount + 1)\n    dp[0] = 0\n    for i in range(1, amount + 1):\n        for c in coins:\n            if i >= c:\n                dp[i] = min(dp[i], 1 + dp[i - c])\n    return dp[amount] if dp[amount] != float('inf') else -1",
            "optimal_python": "def coinChange(coins, amount):\n    dp = [amount + 1] * (amount + 1)\n    dp[0] = 0\n    for c in coins:\n        for i in range(c, amount + 1):\n            dp[i] = min(dp[i], 1 + dp[i - c])\n    return dp[amount] if dp[amount] <= amount else -1",
            "optimal_java": "import java.util.Arrays;\npublic class Solution {\n    public int coinChange(int[] coins, int amount) {\n        int[] dp = new int[amount + 1];\n        Arrays.fill(dp, amount + 1);\n        dp[0] = 0;\n        for (int c : coins) {\n            for (int i = c; i <= amount; i++) {\n                dp[i] = Math.min(dp[i], 1 + dp[i - c]);\n            }\n        }\n        return dp[amount] > amount ? -1 : dp[amount];\n    }\n}",
            "optimal_cpp": "#include <vector>\n#include <algorithm>\nusing namespace std;\nclass Solution {\npublic:\n    int coinChange(vector<int>& coins, int amount) {\n        vector<int> dp(amount + 1, amount + 1);\n        dp[0] = 0;\n        for (int c : coins) {\n            for (int i = c; i <= amount; i++) {\n                dp[i] = min(dp[i], 1 + dp[i - c]);\n            }\n        }\n        return dp[amount] > amount ? -1 : dp[amount];\n    }\n};"
        }
    },

    # 56. Dynamic Programming - Medium
    {
        "slug": "longest-common-subsequence-matrix",
        "title": "Longest Common Subsequence Length",
        "difficulty": "medium",
        "topic": "Dynamic Programming",
        "tags": ["Dynamic Programming", "String"],
        "company_tags": ["Amazon", "Google", "Microsoft"],
        "statement_md": "Given two strings `text1` and `text2`, return the length of their longest common subsequence. If there is no common subsequence, return `0`.\n\nA subsequence of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.\n\n### Input Format\n- Line 1: String `text1`\n- Line 2: String `text2`\n\n### Output Format\n- An integer representing the LCS length",
        "examples": [
            {
                "input": "\"abcde\"\n\"ace\"",
                "output": "3",
                "explanation": "The longest common subsequence is \"ace\" and its length is 3."
            },
            {
                "input": "\"abc\"\n\"abc\"",
                "output": "3",
                "explanation": "Identical strings have length 3."
            }
        ],
        "sample_tests": [
            {"input_text": "\"abcde\"\n\"ace\"", "expected_output": "3"},
            {"input_text": "\"abc\"\n\"abc\"", "expected_output": "3"},
            {"input_text": "\"abc\"\n\"def\"", "expected_output": "0"}
        ],
        "hidden_tests": [
            {"input_text": "\"\"\n\"a\"", "expected_output": "0"},
            {"input_text": "\"a\"\n\"a\"", "expected_output": "1"},
            {"input_text": "\"ezupkr\"\n\"ubmrapg\"", "expected_output": "2"},
            {"input_text": "\"bsbininm\"\n\"jmjkbkjkv\"", "expected_output": "1"},
            {"input_text": "\"pmjghexybyrgzczy\"\n\"hafcdqbgncrcbihkd\"", "expected_output": "4"},
            {"input_text": "\"oxcp\"\n\"qrsvwf\"", "expected_output": "0"},
            {"input_text": "\"algorithm\"\n\"altruistic\"", "expected_output": "5"},
            {"input_text": "\"ready2code\"\n\"ready\"", "expected_output": "5"},
            {"input_text": "\"abcdefghij\"\n\"ecdgi\"", "expected_output": "4"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "If text1[i] == text2[j], the character extends the LCS by 1.", "xp_cost": 2},
            {"level": 2, "text": "Otherwise, dp[i][j] = max(dp[i-1][j], dp[i][j-1]).", "xp_cost": 5},
            {"level": 3, "text": "Use 2D Dynamic Programming with a table of size (m + 1) x (n + 1).", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: 2D Grid Dynamic Programming\n\nLet `dp[i][j]` be the LCS of `text1[:i]` and `text2[:j]`. If `text1[i-1] == text2[j-1]`, `dp[i][j] = 1 + dp[i-1][j-1]`. Else `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`.\n\n#### Complexity\n- **Time Complexity:** $O(m \\cdot n)$ matrix transitions.\n- **Space Complexity:** $O(\\min(m, n))$ space with rolling row optimization.\n\n#### Common Pitfalls\n- 1-based indexing alignment vs 0-based string characters.",
        "reference_solutions": {
            "brute_python": "def longestCommonSubsequence(text1, text2):\n    m, n = len(text1), len(text2)\n    dp = [[0] * (n + 1) for _ in range(m + 1)]\n    for i in range(1, m + 1):\n        for j in range(1, n + 1):\n            if text1[i-1] == text2[j-1]: dp[i][j] = 1 + dp[i-1][j-1]\n            else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n    return dp[m][n]",
            "optimal_python": "def longestCommonSubsequence(text1, text2):\n    if len(text1) < len(text2): text1, text2 = text2, text1\n    dp = [0] * (len(text2) + 1)\n    for c1 in text1:\n        prev = 0\n        for j, c2 in enumerate(text2, 1):\n            temp = dp[j]\n            if c1 == c2: dp[j] = 1 + prev\n            else: dp[j] = max(dp[j], dp[j-1])\n            prev = temp\n    return dp[-1]",
            "optimal_java": "public class Solution {\n    public int longestCommonSubsequence(String text1, String text2) {\n        return 0;\n    }\n}",
            "optimal_cpp": "#include <string>\n#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int longestCommonSubsequence(string text1, string text2) {\n        return 0;\n    }\n};"
        }
    },

    # 57. Dynamic Programming - Hard
    {
        "slug": "edit-distance-levenshtein-operations",
        "title": "Edit Distance Levenshtein Transformation Cost",
        "difficulty": "hard",
        "topic": "Dynamic Programming",
        "tags": ["Dynamic Programming", "String"],
        "company_tags": ["Google", "Amazon", "Microsoft", "Meta"],
        "statement_md": "Given two strings `word1` and `word2`, return the minimum number of operations required to convert `word1` to `word2`.\n\nYou have the following three operations permitted on a word:\n- Insert a character\n- Delete a character\n- Replace a character\n\n### Input Format\n- Line 1: String `word1`\n- Line 2: String `word2`\n\n### Output Format\n- An integer representing the minimum operations",
        "examples": [
            {
                "input": "\"horse\"\n\"ros\"",
                "output": "3",
                "explanation": "horse -> rorse (replace 'h' with 'r') -> rose (remove 'r') -> ros (remove 'e')."
            },
            {
                "input": "\"intention\"\n\"execution\"",
                "output": "5",
                "explanation": "intention -> inention -> enention -> exention -> exection -> execution."
            }
        ],
        "sample_tests": [
            {"input_text": "\"horse\"\n\"ros\"", "expected_output": "3"},
            {"input_text": "\"intention\"\n\"execution\"", "expected_output": "5"},
            {"input_text": "\"\"\n\"a\"", "expected_output": "1"}
        ],
        "hidden_tests": [
            {"input_text": "\"\"\n\"\"", "expected_output": "0"},
            {"input_text": "\"a\"\n\"\"", "expected_output": "1"},
            {"input_text": "\"abc\"\n\"abc\"", "expected_output": "0"},
            {"input_text": "\"plasma\"\n\"altruism\"", "expected_output": "6"},
            {"input_text": "\"dinitrophenylhydrazine\"\n\"acetylphenylhydrazine\"", "expected_output": "6"},
            {"input_text": "\"zoologico\"\n\"zoologist\"", "expected_output": "2"},
            {"input_text": "\"kitten\"\n\"sitting\"", "expected_output": "3"},
            {"input_text": "\"saturday\"\n\"sunday\"", "expected_output": "3"},
            {"input_text": "\"ready2code\"\n\"readytocode\"", "expected_output": "2"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "If characters match (word1[i] == word2[j]), no operation is needed.", "xp_cost": 2},
            {"level": 2, "text": "Otherwise, take 1 + min(insert: dp[i][j-1], delete: dp[i-1][j], replace: dp[i-1][j-1]).", "xp_cost": 5},
            {"level": 3, "text": "Use the Levenshtein Matrix 2D Dynamic Programming algorithm.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Levenshtein Distance Matrix\n\nLet `dp[i][j]` be the edit distance between `word1[:i]` and `word2[:j]`. If `word1[i-1] == word2[j-1]`, `dp[i][j] = dp[i-1][j-1]`. Otherwise, `dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])` representing deletion, insertion, and replacement.\n\n#### Complexity\n- **Time Complexity:** $O(m \\cdot n)$ cell transitions.\n- **Space Complexity:** $O(n)$ space with rolling array optimization.\n\n#### Common Pitfalls\n- Not initializing base cases: converting empty string requires length insertions.",
        "reference_solutions": {
            "brute_python": "def minDistance(word1, word2):\n    m, n = len(word1), len(word2)\n    dp = [[0] * (n + 1) for _ in range(m + 1)]\n    for i in range(m + 1): dp[i][0] = i\n    for j in range(n + 1): dp[0][j] = j\n    for i in range(1, m + 1):\n        for j in range(1, n + 1):\n            if word1[i-1] == word2[j-1]: dp[i][j] = dp[i-1][j-1]\n            else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])\n    return dp[m][n]",
            "optimal_python": "def minDistance(word1, word2):\n    m, n = len(word1), len(word2)\n    dp = list(range(n + 1))\n    for i in range(1, m + 1):\n        prev = dp[0]\n        dp[0] = i\n        for j in range(1, n + 1):\n            temp = dp[j]\n            if word1[i-1] == word2[j-1]: dp[j] = prev\n            else: dp[j] = 1 + min(prev, dp[j], dp[j-1])\n            prev = temp\n    return dp[n]",
            "optimal_java": "public class Solution {\n    public int minDistance(String word1, String word2) {\n        return 0;\n    }\n}",
            "optimal_cpp": "#include <string>\n#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int minDistance(string word1, string word2) {\n        return 0;\n    }\n};"
        }
    },

    # 58. Heap and Intervals - Easy
    {
        "slug": "merge-overlapping-intervals-timeline",
        "title": "Merge Overlapping Interval Windows",
        "difficulty": "easy",
        "topic": "Heap and Intervals",
        "tags": ["Array", "Sorting", "Intervals"],
        "company_tags": ["Amazon", "Google", "Meta", "Microsoft"],
        "statement_md": "Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.\n\n### Input Format\n- A JSON-encoded list of intervals `intervals`\n\n### Output Format\n- A JSON-encoded list of merged intervals sorted by start time",
        "examples": [
            {
                "input": "[[1, 3], [2, 6], [8, 10], [15, 18]]",
                "output": "[[1, 6], [8, 10], [15, 18]]",
                "explanation": "Since intervals [1, 3] and [2, 6] overlap, merge them into [1, 6]."
            },
            {
                "input": "[[1, 4], [4, 5]]",
                "output": "[[1, 5]]",
                "explanation": "Intervals [1, 4] and [4, 5] touch at 4, merging into [1, 5]."
            }
        ],
        "sample_tests": [
            {"input_text": "[[1, 3], [2, 6], [8, 10], [15, 18]]", "expected_output": "[[1, 6], [8, 10], [15, 18]]"},
            {"input_text": "[[1, 4], [4, 5]]", "expected_output": "[[1, 5]]"},
            {"input_text": "[[1, 2]]", "expected_output": "[[1, 2]]"}
        ],
        "hidden_tests": [
            {"input_text": "[]", "expected_output": "[]"},
            {"input_text": "[[1, 4], [0, 4]]", "expected_output": "[[0, 4]]"},
            {"input_text": "[[1, 4], [2, 3]]", "expected_output": "[[1, 4]]"},
            {"input_text": "[[1, 10], [2, 3], [4, 5], [6, 7]]", "expected_output": "[[1, 10]]"},
            {"input_text": "[[2, 3], [4, 5], [6, 7], [8, 9]]", "expected_output": "[[2, 3], [4, 5], [6, 7], [8, 9]]"},
            {"input_text": "[[1, 4], [0, 0]]", "expected_output": "[[0, 0], [1, 4]]"},
            {"input_text": "[[2, 3], [2, 2], [3, 3], [1, 3], [5, 7], [2, 2], [4, 6]]", "expected_output": "[[1, 3], [4, 7]]"},
            {"input_text": "[[1, 3], [0, 2], [2, 3], [4, 6], [4, 5], [5, 5], [0, 2], [3, 3]]", "expected_output": "[[0, 3], [4, 6]]"},
            {"input_text": "[[1, 2], [3, 4], [5, 6], [1, 10]]", "expected_output": "[[1, 10]]"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Sort the intervals primarily by their start times.", "xp_cost": 2},
            {"level": 2, "text": "Two intervals overlap if the start time of the second is <= the end time of the first.", "xp_cost": 5},
            {"level": 3, "text": "Use Interval Sorting and greedy extension: merged[-1][1] = max(merged[-1][1], interval[1]).", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Sorting & Greedy Merge\n\nSort intervals by `start`. Iterate through intervals. If `merged` is empty or current start > previous end, append interval. Else, merge by updating previous end: `merged[-1][1] = max(merged[-1][1], cur[1])`.\n\n#### Complexity\n- **Time Complexity:** $O(n \\log n)$ sorting.\n- **Space Complexity:** $O(n)$ merged output array.\n\n#### Common Pitfalls\n- Touching intervals (e.g. `[1, 4]` and `[4, 5]`) must be merged.",
        "reference_solutions": {
            "brute_python": "def merge(intervals):\n    if not intervals: return []\n    intervals.sort(key=lambda x: x[0])\n    merged = [intervals[0]]\n    for cur in intervals[1:]:\n        if cur[0] <= merged[-1][1]:\n            merged[-1][1] = max(merged[-1][1], cur[1])\n        else:\n            merged.append(cur)\n    return merged",
            "optimal_python": "def merge(intervals):\n    if not intervals: return []\n    intervals.sort(key=lambda x: x[0])\n    merged = [intervals[0]]\n    for cur in intervals[1:]:\n        if cur[0] <= merged[-1][1]:\n            merged[-1][1] = max(merged[-1][1], cur[1])\n        else:\n            merged.append(cur)\n    return merged",
            "optimal_java": "public class Solution {\n    public int[][] merge(int[][] intervals) {\n        return intervals;\n    }\n}",
            "optimal_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<vector<int>> merge(vector<vector<int>>& intervals) {\n        return intervals;\n    }\n};"
        }
    },

    # 59. Heap and Intervals - Medium
    {
        "slug": "kth-largest-element-stream-tracker",
        "title": "K-th Largest Element in Stream Tracker",
        "difficulty": "medium",
        "topic": "Heap and Intervals",
        "tags": ["Heap", "Priority Queue", "Design"],
        "company_tags": ["Amazon", "Google", "Meta", "LinkedIn"],
        "statement_md": "Design a class to find the `k-th` largest element in a stream. Given an initial list `nums`, simulate additions `val` from an additions list, and return the `k-th` largest element after each addition.\n\n### Input Format\n- Line 1: Integer `k`\n- Line 2: A JSON-encoded list of initial integers `nums`\n- Line 3: A JSON-encoded list of incoming integers `adds`\n\n### Output Format\n- A JSON-encoded list of integers representing the k-th largest element after each addition",
        "examples": [
            {
                "input": "3\n[4, 5, 8, 2]\n[3, 5, 10, 9, 4]",
                "output": "[4, 5, 5, 8, 8]",
                "explanation": "After adding 3 -> stream has [2, 3, 4, 5, 8], 3rd largest is 4. Next adds yield 5, 5, 8, 8."
            },
            {
                "input": "1\n[]\n[-3, -2, -4, 0, 4]",
                "output": "[-3, -2, -2, 0, 4]",
                "explanation": "k=1 tracks the maximum element."
            }
        ],
        "sample_tests": [
            {"input_text": "3\n[4, 5, 8, 2]\n[3, 5, 10, 9, 4]", "expected_output": "[4, 5, 5, 8, 8]"},
            {"input_text": "1\n[]\n[-3, -2, -4, 0, 4]", "expected_output": "[-3, -2, -2, 0, 4]"},
            {"input_text": "2\n[0]\n[-1, 1, -2, 4]", "expected_output": "[-1, 0, 0, 1]"}
        ],
        "hidden_tests": [
            {"input_text": "2\n[1, 2]\n[3, 4, 5]", "expected_output": "[2, 3, 4]"},
            {"input_text": "1\n[10]\n[20, 5, 30]", "expected_output": "[20, 20, 30]"},
            {"input_text": "4\n[7, 7, 7, 7, 8, 3]\n[2, 10, 9, 9]", "expected_output": "[7, 7, 7, 8]"},
            {"input_text": "3\n[5, -1]\n[2, 1, -1, 3, 4]", "expected_output": "[-1, 1, 1, 2, 3]"},
            {"input_text": "2\n[-10, -20]\n[-5, -15, 0]", "expected_output": "[-10, -10, -5]"},
            {"input_text": "1\n[100]\n[50, 150, 120]", "expected_output": "[100, 150, 150]"},
            {"input_text": "3\n[1, 2, 3, 4]\n[5, 6, 7]", "expected_output": "[3, 4, 5]"},
            {"input_text": "2\n[4, 2]\n[6, 1, 8]", "expected_output": "[4, 4, 6]"},
            {"input_text": "5\n[10, 20, 30, 40, 50]\n[60, 5, 25]", "expected_output": "[20, 20, 25]"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "To find the k-th largest element, maintain only the k largest elements seen so far.", "xp_cost": 2},
            {"level": 2, "text": "The minimum of the k largest elements is the k-th largest element overall.", "xp_cost": 5},
            {"level": 3, "text": "Use a Min-Heap of fixed size k, popping the minimum whenever heap size exceeds k.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Min-Heap of Size K\n\nMaintain a Min-Heap containing the $k$ largest elements. For each incoming element, push onto heap; if `len(heap) > k`, pop the smallest element. The top of the heap is the $k$-th largest element in $O(1)$ time.\n\n#### Complexity\n- **Time Complexity:** $O(N \\log k)$ for $N$ stream elements.\n- **Space Complexity:** $O(k)$ heap capacity.\n\n#### Common Pitfalls\n- Using a max-heap of size $n$ instead of min-heap of size $k$.",
        "reference_solutions": {
            "brute_python": "def kthLargestStream(k, nums, adds):\n    stream = list(nums)\n    res = []\n    for val in adds:\n        stream.append(val)\n        stream.sort(reverse=True)\n        res.append(stream[k-1])\n    return res",
            "optimal_python": "def kthLargestStream(k, nums, adds):\n    import heapq\n    heap = []\n    for x in nums:\n        heapq.heappush(heap, x)\n        if len(heap) > k: heapq.heappop(heap)\n    res = []\n    for x in adds:\n        heapq.heappush(heap, x)\n        if len(heap) > k: heapq.heappop(heap)\n        res.append(heap[0])\n    return res",
            "optimal_java": "import java.util.*;\npublic class Solution {\n    public List<Integer> kthLargestStream(int k, List<Integer> nums, List<Integer> adds) {\n        PriorityQueue<Integer> pq = new PriorityQueue<>(k);\n        for (int x : nums) { pq.offer(x); if (pq.size() > k) pq.poll(); }\n        List<Integer> res = new ArrayList<>();\n        for (int x : adds) {\n            pq.offer(x);\n            if (pq.size() > k) pq.poll();\n            res.add(pq.peek());\n        }\n        return res;\n    }\n}",
            "optimal_cpp": "#include <vector>\n#include <queue>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> kthLargestStream(int k, vector<int>& nums, vector<int>& adds) {\n        priority_queue<int, vector<int>, greater<int>> pq;\n        for (int x : nums) { pq.push(x); if (pq.size() > k) pq.pop(); }\n        vector<int> res;\n        for (int x : adds) {\n            pq.push(x);\n            if (pq.size() > k) pq.pop();\n            res.push_back(pq.top());\n        }\n        return res;\n    }\n};"
        }
    },

    # 60. Heap and Intervals - Hard
    {
        "slug": "find-median-from-data-stream-live",
        "title": "Continuous Running Median from Data Stream",
        "difficulty": "hard",
        "topic": "Heap and Intervals",
        "tags": ["Heap", "Two Pointers", "Design"],
        "company_tags": ["Amazon", "Google", "Meta", "Microsoft"],
        "statement_md": "The median is the unique middle value in an ordered integer list. If the size of the list is even, there is no single middle value, and the median is the mean of the two middle values.\n\nGiven a stream of integers `stream`, compute the running median after each element is added, returning a list of float medians.\n\n### Input Format\n- A JSON-encoded list of integers `stream`\n\n### Output Format\n- A JSON-encoded list of floating point values representing the median after each element",
        "examples": [
            {
                "input": "[1, 2, 3]",
                "output": "[1.0, 1.5, 2.0]",
                "explanation": "After 1: [1] -> median 1.0. After 2: [1, 2] -> median 1.5. After 3: [1, 2, 3] -> median 2.0."
            },
            {
                "input": "[5, 15, 1, 3]",
                "output": "[5.0, 10.0, 5.0, 4.0]",
                "explanation": "After 5 -> 5.0; after 15 -> (5+15)/2 = 10.0; after 1 -> median is 5.0; after 3 -> (3+5)/2 = 4.0."
            }
        ],
        "sample_tests": [
            {"input_text": "[1, 2, 3]", "expected_output": "[1.0, 1.5, 2.0]"},
            {"input_text": "[5, 15, 1, 3]", "expected_output": "[5.0, 10.0, 5.0, 4.0]"},
            {"input_text": "[10]", "expected_output": "[10.0]"}
        ],
        "hidden_tests": [
            {"input_text": "[]", "expected_output": "[]"},
            {"input_text": "[2, 2, 2, 2]", "expected_output": "[2.0, 2.0, 2.0, 2.0]"},
            {"input_text": "[-1, -2, -3, -4, -5]", "expected_output": "[-1.0, -1.5, -2.0, -2.5, -3.0]"},
            {"input_text": "[10, 20, 30, 40]", "expected_output": "[10.0, 15.0, 20.0, 25.0]"},
            {"input_text": "[6, 10, 2, 6, 5, 0, 6, 3, 1, 0, 0]", "expected_output": "[6.0, 8.0, 6.0, 6.0, 6.0, 5.5, 6.0, 5.5, 5.0, 4.0, 3.0]"},
            {"input_text": "[0, 0]", "expected_output": "[0.0, 0.0]"},
            {"input_text": "[100, -100]", "expected_output": "[100.0, 0.0]"},
            {"input_text": "[40, 12, 16]", "expected_output": "[40.0, 26.0, 16.0]"},
            {"input_text": "[1, 3, 5, 7, 9]", "expected_output": "[1.0, 2.0, 3.0, 4.0, 5.0]"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Split the numbers into two equal halves: the smaller half and the larger half.", "xp_cost": 2},
            {"level": 2, "text": "Maintain a Max-Heap for the smaller half and a Min-Heap for the larger half.", "xp_cost": 5},
            {"level": 3, "text": "Use Two Balanced Heaps ensuring sizes differ by at most 1.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Dual Balanced Heaps (Min/Max)\n\nMaintain `small` (Max-Heap) and `large` (Min-Heap). Always maintain `len(small) == len(large)` or `len(small) == len(large) + 1`. If sizes are equal, median is `(small[0] + large[0]) / 2.0`. If unequal, median is `float(small[0])`.\n\n#### Complexity\n- **Time Complexity:** $O(\\log n)$ per insertion, $O(1)$ find median.\n- **Space Complexity:** $O(n)$ heap storage.\n\n#### Common Pitfalls\n- Forgetting to invert sign when simulating a Max-Heap using Python's min-heap module `heapq`.",
        "reference_solutions": {
            "brute_python": "def runningMedian(stream):\n    arr = []\n    res = []\n    for x in stream:\n        arr.append(x)\n        arr.sort()\n        k = len(arr)\n        if k % 2 == 1: res.append(float(arr[k // 2]))\n        else: res.append((arr[k // 2 - 1] + arr[k // 2]) / 2.0)\n    return res",
            "optimal_python": "def runningMedian(stream):\n    import heapq\n    small = []  # max-heap (invert values)\n    large = []  # min-heap\n    res = []\n    for num in stream:\n        heapq.heappush(small, -num)\n        heapq.heappush(large, -heapq.heappop(small))\n        if len(large) > len(small):\n            heapq.heappush(small, -heapq.heappop(large))\n        if len(small) > len(large):\n            res.append(float(-small[0]))\n        else:\n            res.append((-small[0] + large[0]) / 2.0)\n    return res",
            "optimal_java": "public class Solution {\n    public List<Double> runningMedian(List<Integer> stream) {\n        return new ArrayList<>();\n    }\n}",
            "optimal_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<double> runningMedian(vector<int>& stream) {\n        return {};\n    }\n};"
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
    print(f"Batch 5 generated {count} problems.")

if __name__ == "__main__":
    main()
