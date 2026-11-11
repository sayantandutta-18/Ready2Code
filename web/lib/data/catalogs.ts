import problemsData from "./problems.json";

export interface ProblemItem {
  id: string;
  slug: string;
  title: string;
  difficulty: "easy" | "medium" | "hard";
  topic: string;
  topic_key: string;
  tags: string[];
  acceptance_rate: number;
  best_runtime_ms: number;
  status: "todo" | "attempted" | "solved";
  function_name?: string;
  params?: string[];
  statement_md?: string;
  examples?: any[];
  sample_tests?: any[];
  hidden_tests?: any[];
  starter_code?: Record<string, string>;
  reference_python?: string;
  hints?: any[];
}

export const PROBLEMS: ProblemItem[] = problemsData as ProblemItem[];

export const TOPICS = [
  { id: "topic_arrays", slug: "arrays", name: "Arrays and Hashing", order_index: 1, problem_count: 22 },
  { id: "topic_two_pointers", slug: "two_pointers", name: "Two Pointers and Sliding Window", order_index: 2, problem_count: 16 },
  { id: "topic_strings", slug: "strings", name: "Strings", order_index: 3, problem_count: 18 },
  { id: "topic_stack", slug: "stack", name: "Stack and Queue", order_index: 4, problem_count: 12 },
  { id: "topic_linked_list", slug: "linked_list", name: "Linked List", order_index: 5, problem_count: 10 },
  { id: "topic_trees", slug: "trees", name: "Trees", order_index: 6, problem_count: 13 },
  { id: "topic_graphs", slug: "graphs", name: "Graphs", order_index: 7, problem_count: 12 },
  { id: "topic_binary_search", slug: "binary_search", name: "Binary Search", order_index: 8, problem_count: 10 },
  { id: "topic_dp", slug: "dp", name: "Dynamic Programming", order_index: 9, problem_count: 20 },
  { id: "topic_heap_greedy", slug: "heap_greedy", name: "Heap, Intervals and Greedy", order_index: 10, problem_count: 17 },
];

export const PATTERNS = [
  {
    slug: "two-pointers",
    name: "Two Pointers",
    order_index: 1,
    signals: "Sorted arrays, searching for pairs, palindromes, in-place partitions.",
    lesson_md: `### Pattern: Two Pointers
Two pointers iterate through the data structure from opposite ends or at different speeds.

#### Key Signals in Problem Statements:
- Array is sorted or order can be sorted in $O(n \\log n)$.
- Target involves pair sums, triplets, or subsegments.
- Requires $O(1)$ auxiliary space without extra allocations.`,
    template_code: `def two_pointers(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        # evaluate condition
        if condition(nums[left], nums[right]):
            left += 1
        else:
            right -= 1`,
    quiz_question: "You need to find two numbers in an already sorted ascending array that sum to K using O(1) extra space. Which technique is optimal?",
    options: ["Two Pointers (converging inward)", "Breadth-First Search", "Segment Tree", "Topological Sort"],
    correct_option_index: 0
  },
  {
    slug: "sliding-window",
    name: "Sliding Window",
    order_index: 2,
    signals: "Contiguous subarrays, longest/shortest substrings, max sum of size K.",
    lesson_md: `### Pattern: Sliding Window
Maintains a window \`[left, right]\` that expands to include valid elements and shrinks when constraints are violated.

#### Key Signals:
- Finding longest/shortest contiguous sequence matching criteria.
- Target constraint: at most K distinct elements or max sum.`,
    template_code: `def sliding_window(s):
    left = 0
    state = {}
    best = 0
    for right, c in enumerate(s):
        state[c] = state.get(c, 0) + 1
        while not valid(state):
            state[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best`,
    quiz_question: "Given a string s, find the length of the longest substring with at most two distinct characters. Which pattern directly applies?",
    options: ["Sliding Window with character frequency hash map", "Floyd-Warshall algorithm", "Binary Indexed Tree", "Morris Traversal"],
    correct_option_index: 0
  },
  {
    slug: "fast-and-slow-pointers",
    name: "Fast & Slow Pointers (Floyd's Cycle)",
    order_index: 3,
    signals: "Cycle detection in linked list, finding middle node, happy numbers.",
    lesson_md: `### Pattern: Fast and Slow Pointers
Move \`slow\` one step and \`fast\` two steps. If a cycle exists, they will inevitably collide.`,
    template_code: `def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False`,
    quiz_question: "How do you detect if a singly linked list contains a cycle using O(1) space?",
    options: ["Floyd's Tortoise and Hare (Slow/Fast pointers)", "Store nodes in an adjacency matrix", "Run Dijkstra's algorithm", "Recursively reverse each node"],
    correct_option_index: 0
  },
  {
    slug: "monotonic-stack",
    name: "Monotonic Stack",
    order_index: 4,
    signals: "Next greater element, largest rectangle in histogram, daily temperatures.",
    lesson_md: `### Pattern: Monotonic Stack
A stack maintaining strictly increasing or decreasing elements to resolve nearest larger/smaller queries in linear time.`,
    template_code: `def next_greater(nums):
    res = [-1] * len(nums)
    stack = []
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            idx = stack.pop()
            res[idx] = x
        stack.append(i)
    return res`,
    quiz_question: "Find the number of days until a warmer temperature for every day in an array. Optimal approach?",
    options: ["Monotonic Decreasing Stack storing indices", "Nested loops scanning O(n²)", "Prim's Minimum Spanning Tree", "Bit manipulation"],
    correct_option_index: 0
  },
  {
    slug: "bfs-breadth-first-search",
    name: "Breadth-First Search (BFS)",
    order_index: 5,
    signals: "Shortest path in unweighted graphs, level-order traversal, word ladder.",
    lesson_md: `### Pattern: BFS
Explores graph or tree layer by layer using a FIFO queue to guarantee minimum distance.`,
    template_code: `def bfs(start):
    q = deque([start])
    visited = {start}
    while q:
        curr = q.popleft()
        for nbr in neighbors(curr):
            if nbr not in visited:
                visited.add(nbr)
                q.append(nbr)`,
    quiz_question: "To find the minimum number of knight moves on a chessboard from start to destination, which search should you use?",
    options: ["BFS using a Queue", "DFS with unlimited recursion depth", "QuickSort", "Kruskal's algorithm"],
    correct_option_index: 0
  }
];

export const COMPANIES = [
  {
    slug: "google",
    name: "Google",
    tier: "Tier 1 Product",
    rounds: 5,
    ctc: "₹35 - ₹55 LPA",
    target_topics: ["Graphs", "Dynamic Programming", "Trie", "Binary Search"],
    problem_count: 84,
    description: "Heavy focus on optimal time/space complexity, edge case handling, and clean modular code.",
    schedule: [
      { day: 1, title: "Array Two-Pointers & Sliding Window", problems: ["two-sum", "container-with-most-water", "longest-substring-without-repeating-characters"] },
      { day: 2, title: "Stack & Monotonic Queue Patterns", problems: ["valid-parentheses", "min-stack", "daily-temperatures"] },
      { day: 3, title: "Linked List Reversals & Cycles", problems: ["reverse-linked-list", "merge-two-sorted-lists", "linked-list-cycle"] },
      { day: 4, title: "Binary Search Variations & Rotated Arrays", problems: ["binary-search", "search-in-rotated-sorted-array", "find-minimum-in-rotated-sorted-array"] },
      { day: 5, title: "Tree Traversals & Binary Search Trees", problems: ["maximum-depth-of-binary-tree", "validate-binary-search-tree", "invert-binary-tree"] },
      { day: 6, title: "Graph BFS / DFS & Grid Traversal", problems: ["number-of-islands", "rotting-oranges", "course-schedule"] },
      { day: 7, title: "Dynamic Programming 1D & 2D Foundations", problems: ["climbing-stairs", "coin-change", "longest-common-subsequence"] },
      { day: 8, title: "Intervals & Greedy Scheduling", problems: ["merge-intervals", "insert-interval", "non-overlapping-intervals"] }
    ]
  },
  {
    slug: "amazon",
    name: "Amazon",
    tier: "Tier 1 Product",
    rounds: 4,
    ctc: "₹28 - ₹45 LPA",
    target_topics: ["Arrays", "Trees", "BFS/DFS", "Sliding Window"],
    problem_count: 112,
    description: "Balanced DSA rounds combined with 16 Amazon Leadership Principles across every interview.",
    schedule: [
      { day: 1, title: "Array Hashing & Two Pointers", problems: ["two-sum", "product-of-array-except-self", "container-with-most-water"] },
      { day: 2, title: "Tree Inorder, Preorder & BFS", problems: ["binary-tree-inorder-traversal", "binary-tree-level-order-traversal"] },
      { day: 3, title: "Priority Queue & Top K Elements", problems: ["kth-largest-element-in-an-array", "top-k-frequent-elements"] },
      { day: 4, title: "Dynamic Programming & Knapsack", problems: ["coin-change", "house-robber", "word-break"] }
    ]
  },
  {
    slug: "microsoft",
    name: "Microsoft",
    tier: "Tier 1 Product",
    rounds: 4,
    ctc: "₹26 - ₹42 LPA",
    target_topics: ["Linked List", "Strings", "Trees", "Stack"],
    problem_count: 96,
    description: "Standard algorithmic problem solving with deep dive into code correctness and test writing.",
    schedule: [
      { day: 1, title: "String Parsing & Anagrams", problems: ["valid-anagram", "group-anagrams", "valid-parentheses"] },
      { day: 2, title: "Linked List Merge & Reverse", problems: ["reverse-linked-list", "merge-two-sorted-lists"] },
      { day: 3, title: "Tree LCA & Validations", problems: ["lowest-common-ancestor-of-a-bst", "validate-binary-search-tree"] }
    ]
  },
  {
    slug: "uber",
    name: "Uber",
    tier: "Tier 1 Product",
    rounds: 4,
    ctc: "₹34 - ₹58 LPA",
    target_topics: ["Graphs", "Shortest Path", "Heaps", "Intervals"],
    problem_count: 65,
    description: "High bar on graph algorithms, concurrency, and low-latency system design fundamentals.",
    schedule: [
      { day: 1, title: "Topological Sort & Dependencies", problems: ["course-schedule"] },
      { day: 2, title: "Rotting Oranges & Multi-source BFS", problems: ["rotting-oranges", "number-of-islands"] }
    ]
  },
  {
    slug: "flipkart",
    name: "Flipkart",
    tier: "Top E-Commerce",
    rounds: 4,
    ctc: "₹24 - ₹38 LPA",
    target_topics: ["Dynamic Programming", "Trees", "Machine Coding (LLD)"],
    problem_count: 78,
    description: "Famous for the 90-minute Machine Coding round requiring fully working, extensible OOP code.",
    schedule: [
      { day: 1, title: "Grid Traversal & Shortest Paths", problems: ["unique-paths", "number-of-islands"] }
    ]
  },
  {
    slug: "atlassian",
    name: "Atlassian",
    tier: "Tier 1 SaaS",
    rounds: 5,
    ctc: "₹38 - ₹65 LPA",
    target_topics: ["Data Structures", "OOP", "Concurrency"],
    problem_count: 52,
    description: "Collaborative pair programming rounds evaluating design choices, unit testing, and communication.",
    schedule: [
      { day: 1, title: "Interval Merging & Processing", problems: ["merge-intervals", "insert-interval"] }
    ]
  }
];

export const INTERVIEWS = [
  {
    id: "exp-1",
    author: "Rohan V.",
    company: "Google",
    role: "Software Engineer (L3)",
    date: "October 2026",
    verdict: "Offer",
    ctc: "₹45 LPA",
    difficulty: "Hard",
    rounds: [
      { name: "OA (Online Assessment)", desc: "2 graph questions involving Dijkstra and disjoint set union." },
      { name: "Technical Round 1", desc: "Sliding window maximum with monotonic deque + follow-up on 2D matrix." },
      { name: "Technical Round 2", desc: "Dynamic programming on trees with subtree memoization." },
      { name: "Googlyness", desc: "Hypothetical engineering conflict scenarios and cross-team communication." }
    ],
    advice: "Do not jump straight into coding. Talk out loud for the first 5 minutes to validate edge cases and explain time/space trade-offs."
  },
  {
    id: "exp-2",
    author: "Sneha M.",
    company: "Amazon",
    role: "SDE-1",
    date: "September 2026",
    verdict: "Offer",
    ctc: "₹34 LPA",
    difficulty: "Medium",
    rounds: [
      { name: "OA", desc: "Two Sum variant with stock profit optimization + debugging section." },
      { name: "Round 1 (DSA)", desc: "Lowest common ancestor in binary tree + Amazon LP Customer Obsession." },
      { name: "Round 2 (DSA)", desc: "Rotting Oranges multi-source BFS with edge cases." },
      { name: "Round 3 (Bar Raiser)", desc: "LRU Cache design and deep dive into 'Deliver Results' principle." }
    ],
    advice: "Prepare 2 real stories in STAR format (Situation, Task, Action, Result) for every Amazon Leadership Principle."
  },
  {
    id: "exp-3",
    author: "Arjun K.",
    company: "Microsoft",
    role: "Software Engineer",
    date: "August 2026",
    verdict: "Offer",
    ctc: "₹28 LPA",
    difficulty: "Medium",
    rounds: [
      { name: "Round 1", desc: "Reverse Linked List in K-groups + edge case discussion." },
      { name: "Round 2", desc: "Course Schedule topological sort (Kahn's algorithm)." },
      { name: "Round 3 (Director)", desc: "Project architecture deep dive and concurrency questions." }
    ],
    advice: "Focus on clean code, naming conventions, and handling null/empty pointer checks before the interviewer asks."
  },
  {
    id: "exp-4",
    author: "Pooja D.",
    company: "Uber",
    role: "Software Engineer 1",
    date: "November 2026",
    verdict: "Rejected",
    ctc: "₹42 LPA",
    difficulty: "Hard",
    rounds: [
      { name: "Round 1 (DSA)", desc: "Word Search II with Trie optimization. Got stuck on prefix pruning." },
      { name: "Round 2 (DSA)", desc: "Trapping Rain Water with two pointers. Passed all test cases." }
    ],
    advice: "Uber's algorithmic bar is high. Practice hard Trie and Backtracking problems under a strict 35-minute timer."
  }
];

export const LISTS = [
  {
    id: "blind-75",
    name: "Blind 75",
    description: "Core 75 high-frequency questions essential for tech interviews across all major patterns.",
    is_system: true,
    visibility: "public",
    problem_slugs: [
      "two-sum", "best-time-to-buy-and-sell-stock", "contains-duplicate", "product-of-array-except-self",
      "maximum-subarray", "container-with-most-water", "3sum", "linked-list-cycle",
      "reverse-linked-list", "merge-two-sorted-lists", "valid-parentheses", "valid-anagram",
      "binary-search", "search-in-rotated-sorted-array", "climbing-stairs", "coin-change",
      "longest-increasing-subsequence", "longest-common-subsequence", "word-break", "number-of-islands",
      "course-schedule", "rotting-oranges", "invert-binary-tree", "maximum-depth-of-binary-tree", "validate-binary-search-tree"
    ]
  },
  {
    id: "neetcode-150",
    name: "NeetCode 150",
    description: "Structured 150-problem mastery syllabus covering foundational to advanced algorithms.",
    is_system: true,
    visibility: "public",
    problem_slugs: [
      "two-sum", "valid-anagram", "group-anagrams", "top-k-frequent-elements", "longest-consecutive-sequence",
      "valid-palindrome", "3sum", "container-with-most-water", "trapping-rain-water",
      "best-time-to-buy-and-sell-stock", "longest-substring-without-repeating-characters", "valid-parentheses",
      "min-stack", "daily-temperatures", "binary-search", "search-a-2d-matrix", "koko-eating-bananas",
      "reverse-linked-list", "merge-two-sorted-lists", "linked-list-cycle", "reorder-list",
      "invert-binary-tree", "maximum-depth-of-binary-tree", "diameter-of-binary-tree", "balanced-binary-tree"
    ]
  },
  {
    id: "placement-classics",
    name: "Top 50 Placement Classics",
    description: "High-yield problems frequently tested in online assessments for Indian campus recruitment.",
    is_system: true,
    visibility: "public",
    problem_slugs: [
      "two-sum", "valid-parentheses", "merge-intervals", "climbing-stairs", "number-of-islands",
      "longest-substring-without-repeating-characters", "subsets", "combination-sum", "word-search",
      "course-schedule", "rotting-oranges", "kth-largest-element-in-an-array", "merge-k-sorted-lists"
    ]
  }
];

export const STUDY_PLANS = [
  {
    id: "plan-30-day",
    name: "30-Day Interview Preparation Bootcamp",
    description: "Comprehensive 30-day algorithmic study plan covering foundational data structures and advanced patterns.",
    duration_days: 30,
    total_problems: 30
  },
  {
    id: "plan-75-day",
    name: "75-Day Placement Sprint",
    description: "Extensive campus placement preparation covering coding OAs, technical interviews, and system design.",
    duration_days: 75,
    total_problems: 75
  }
];

export const CONTESTS = [
  {
    id: "contest-1",
    title: "Weekly Bi-Virtual Arena #1",
    starts_at: new Date(Date.now() - 20 * 60 * 1000).toISOString(),
    duration_min: 90,
    type: "Standard DSA",
    status: "live",
    problem_slugs: ["two-sum", "valid-parentheses", "coin-change", "number-of-islands"]
  },
  {
    id: "contest-2",
    title: "Weekend Placement Hackathon #42",
    starts_at: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000).toISOString(),
    duration_min: 120,
    type: "Speed Coding",
    status: "upcoming",
    problem_slugs: ["container-with-most-water", "reverse-linked-list", "word-break"]
  },
  {
    id: "contest-3",
    title: "Algorithmic Showdown - Tree & Graph Special",
    starts_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
    duration_min: 90,
    type: "Ranked",
    status: "past",
    problem_slugs: ["maximum-depth-of-binary-tree", "validate-binary-search-tree", "course-schedule"]
  }
];

export const JOBS = [
  {
    id: "job-1",
    company: "Razorpay",
    role: "Software Development Engineer (Backend)",
    location: "Bengaluru, India (Hybrid)",
    ctc: "₹24 - ₹32 LPA",
    min_elo: 1550,
    tags: ["Go", "Distributed Systems", "DSA", "Kafka"],
    description: "Scale India's premier financial payments infrastructure handling 10,000+ transactions per second."
  },
  {
    id: "job-2",
    company: "Zepto",
    role: "SDE-1 (Supply Chain & Routing)",
    location: "Mumbai / Bengaluru",
    ctc: "₹28 - ₹36 LPA",
    min_elo: 1600,
    tags: ["Python", "Algorithms", "Graph Theory", "Redis"],
    description: "Design hyper-optimized routing and dispatch algorithms for 10-minute grocery fulfillment."
  },
  {
    id: "job-3",
    company: "Cred",
    role: "Backend Engineer (Payments & Trust)",
    location: "Bengaluru, India",
    ctc: "₹30 - ₹45 LPA",
    min_elo: 1650,
    tags: ["Java", "High Concurrency", "System Design"],
    description: "Architect mission-critical payment workflows with four 9s reliability and microsecond latency."
  },
  {
    id: "job-4",
    company: "Swiggy",
    role: "Software Engineer (Delivery Logistics)",
    location: "Bengaluru / Remote",
    ctc: "₹22 - ₹30 LPA",
    min_elo: 1500,
    tags: ["Java", "Microservices", "Data Structures", "Spring Boot"],
    description: "Build robust spatial dispatch algorithms connecting millions of customers to local restaurants."
  }
];

export const PLACEMENT_QUESTIONS = [
  {
    id: "os-1",
    track: "cs_core",
    title: "Process vs Thread & Context Switching",
    question: "What is the fundamental difference between a Process and a Thread? How do context switching overheads differ?",
    answer_md: `### Process vs Thread
- **Process:** An independent program in execution with its own separate address space, file handles, and memory map.
- **Thread:** A lightweight unit of execution within a process that shares the code, data, and open files with sibling threads, but maintains its own program counter, registers, and stack.
- **Context Switch:** Thread context switching is orders of magnitude faster because the memory cache (TLB) does not need to be flushed, unlike process switching.`,
    hindi_summary: "Process ek poora program hota hai jiska apna alag memory space hota hai. Thread usi process ke andar chhota hissa hota hai jo shared memory use karta hai, isliye context switch bohot fast hota hai.",
    bengali_summary: "Process holo ekta purno program jar nijosho alada memory thake. Thread holo sei process-er ontorgoto ekta lightweight unit ja shared memory bebohar kore, tai context switch onek druto hoy."
  },
  {
    id: "os-2",
    track: "cs_core",
    title: "Virtual Memory & Paging Mechanics",
    question: "How does Virtual Memory work, and what causes a Page Fault?",
    answer_md: `### Virtual Memory & Paging
Virtual memory provides an illusion of a large, contiguous physical memory space to each process.
- **Page Table:** Maps virtual addresses to physical frames.
- **MMU (Memory Management Unit):** Translates virtual addresses to physical addresses at runtime.
- **Page Fault:** Triggered by hardware when a process accesses a page that is not currently mapped into physical RAM (valid bit is 0). The OS suspends the process, fetches the page from swap disk, updates the page table, and resumes execution.`,
    hindi_summary: "Virtual memory ek illusion hai jo process ko lagti hai ki uske paas bohot saari RAM hai. Jab koi page RAM mein nahi milta, tab Page Fault hota hai aur OS usse hard disk se le kar aata hai.",
    bengali_summary: "Virtual memory prottye ti process ke ekta bohu boro memory-r bhranti dey. Jokhon kono page physical RAM-e pawa jay na, tokhon Page Fault ghote ebong OS disk theke sei page tule ane."
  },
  {
    id: "dbms-1",
    track: "cs_core",
    title: "ACID Properties in Relational Databases",
    question: "Explain the four ACID properties in DBMS with real banking transaction examples.",
    answer_md: `### ACID Properties
1. **Atomicity:** All operations succeed or none do (e.g., deducting ₹500 from Account A and adding ₹500 to Account B must both commit or both rollback).
2. **Consistency:** Database transitions only from one valid state to another satisfying all schema constraints.
3. **Isolation:** Concurrent transactions execute without interfering with one another (preventing dirty reads and phantom reads).
4. **Durability:** Once committed, transaction data persists even if the database crashes immediately afterward.`,
    hindi_summary: "ACID transactions ki security guarantee karta hai. Atomicity (sab hoga ya kuch nahi), Consistency (hamesha sahi state), Isolation (transactions ek dusre se alag chalte hain), Durability (crash ke baad bhi data safe rehta hai).",
    bengali_summary: "ACID transaction-er shothikota nishchit kore. Atomicity (shob hobe ba kichui hobe na), Consistency (shob somoy nirdishto niom mene cholbe), Isolation (ekti transaction onno ti ke disturb korbe na), Durability (system crash holeo data safe thakbe)."
  },
  {
    id: "apt-1",
    track: "aptitude",
    title: "Work & Time - Efficiency Formula",
    question: "A can complete a piece of work in 12 days, and B can complete the same work in 16 days. If they work together with C, they finish in 4 days. In how many days can C alone finish the work?",
    answer_md: `### Solution:
- Total Work = LCM(12, 16, 4) = 48 units.
- Efficiency of A = 48 / 12 = 4 units/day.
- Efficiency of B = 48 / 16 = 3 units/day.
- Combined Efficiency of (A + B + C) = 48 / 4 = 12 units/day.
- Efficiency of C = 12 - (4 + 3) = 5 units/day.
- **Time taken by C alone** = 48 / 5 = **9.6 days** (or 9 days 14 hours 24 minutes).`,
    hindi_summary: "Total kaam 48 units maan lo. A ek din mein 4 units karta hai, B 3 units. Teeno mil kar 12 units karte hain. Toh C ka kaam 5 units/day hua. C akele 48/5 = 9.6 din lega.",
    bengali_summary: "Total kaaj 48 units dhore nin. A protidin 4 units kore, B 3 units kore. Tinjone mile 12 units kore. Tai C kore 5 units/day. C ekaki 48/5 = 9.6 dine kaaj sesh korbe."
  }
];
