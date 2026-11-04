const { describe, it } = require("node:test");
const assert = require("node:assert");

// Pure filter & sorting functions matching web/app/problems/page.tsx
function filterProblems(problems, { topic = "all", difficulty = "all", status = "all", tag = "all", search = "" }) {
  return problems.filter((item) => {
    if (topic !== "all") {
      const tNorm = topic.toLowerCase().split(" ")[0];
      if (!item.topic.toLowerCase().includes(tNorm)) return false;
    }
    if (difficulty !== "all" && item.difficulty.toLowerCase() !== difficulty.toLowerCase()) {
      return false;
    }
    if (status !== "all" && item.status !== status) {
      return false;
    }
    if (tag !== "all" && !item.tags.some((t) => t.toLowerCase() === tag.toLowerCase())) {
      return false;
    }
    if (search.trim()) {
      const q = search.toLowerCase().trim();
      const inTitle = item.title.toLowerCase().includes(q);
      const inSlug = item.slug.toLowerCase().includes(q);
      const inTags = item.tags.some((t) => t.toLowerCase().includes(q));
      if (!inTitle && !inSlug && !inTags) return false;
    }
    return true;
  });
}

function sortProblems(problems, sortBy, sortOrder = "asc") {
  const sorted = [...problems];
  const orderMul = sortOrder === "desc" ? -1 : 1;
  const diffOrder = { easy: 1, medium: 2, hard: 3 };

  return sorted.sort((a, b) => {
    if (sortBy === "title") {
      return a.title.localeCompare(b.title) * orderMul;
    }
    if (sortBy === "difficulty") {
      return ((diffOrder[a.difficulty] || 0) - (diffOrder[b.difficulty] || 0)) * orderMul;
    }
    if (sortBy === "acceptance") {
      return (a.acceptance_rate - b.acceptance_rate) * orderMul;
    }
    if (sortBy === "runtime") {
      const rA = a.best_runtime_ms ?? 999999;
      const rB = b.best_runtime_ms ?? 999999;
      return (rA - rB) * orderMul;
    }
    return 0;
  });
}

function paginate(items, page = 1, pageSize = 25) {
  const total = items.length;
  const totalPages = Math.max(1, Math.ceil(total / pageSize));
  const currentPage = Math.min(Math.max(1, page), totalPages);
  const start = (currentPage - 1) * pageSize;
  const pagedItems = items.slice(start, start + pageSize);

  return {
    items: pagedItems,
    total,
    page: currentPage,
    limit: pageSize,
    total_pages: totalPages,
  };
}

describe("Problem List Filters & Sorting Suite", () => {
  const sampleProblems = [
    { id: "1", slug: "two-sum", title: "Two Sum", difficulty: "easy", topic: "Arrays and Hashing", tags: ["hash-map", "array"], status: "solved", acceptance_rate: 49.5, best_runtime_ms: 18 },
    { id: "2", slug: "three-sum", title: "Three Sum", difficulty: "medium", topic: "Two Pointers", tags: ["two-pointers", "array"], status: "attempted", acceptance_rate: 34.2, best_runtime_ms: 65 },
    { id: "3", slug: "trapping-rain-water", title: "Trapping Rain Water", difficulty: "hard", topic: "Two Pointers", tags: ["two-pointers", "stack"], status: "todo", acceptance_rate: 59.8, best_runtime_ms: null },
    { id: "4", slug: "valid-anagram", title: "Valid Anagram", difficulty: "easy", topic: "Arrays and Hashing", tags: ["hash-map", "string"], status: "solved", acceptance_rate: 63.1, best_runtime_ms: 24 },
    { id: "5", slug: "coin-change", title: "Coin Change", difficulty: "medium", topic: "Dynamic Programming", tags: ["dp", "knapsack"], status: "todo", acceptance_rate: 42.0, best_runtime_ms: null },
  ];

  it("filters problems by difficulty", () => {
    const easyOnly = filterProblems(sampleProblems, { difficulty: "easy" });
    assert.strictEqual(easyOnly.length, 2);
    assert.ok(easyOnly.every((p) => p.difficulty === "easy"));

    const hardOnly = filterProblems(sampleProblems, { difficulty: "hard" });
    assert.strictEqual(hardOnly.length, 1);
    assert.strictEqual(hardOnly[0].slug, "trapping-rain-water");
  });

  it("filters problems by topic", () => {
    const dpOnly = filterProblems(sampleProblems, { topic: "Dynamic Programming" });
    assert.strictEqual(dpOnly.length, 1);
    assert.strictEqual(dpOnly[0].slug, "coin-change");
  });

  it("filters problems by user solve status", () => {
    const solved = filterProblems(sampleProblems, { status: "solved" });
    assert.strictEqual(solved.length, 2);
    assert.ok(solved.every((p) => p.status === "solved"));

    const todo = filterProblems(sampleProblems, { status: "todo" });
    assert.strictEqual(todo.length, 2);
  });

  it("filters problems by tag and search query", () => {
    const hashMapped = filterProblems(sampleProblems, { tag: "hash-map" });
    assert.strictEqual(hashMapped.length, 2);

    const searched = filterProblems(sampleProblems, { search: "anagram" });
    assert.strictEqual(searched.length, 1);
    assert.strictEqual(searched[0].slug, "valid-anagram");
  });

  it("sorts problems by difficulty, acceptance rate, and runtime", () => {
    const byDiffAsc = sortProblems(sampleProblems, "difficulty", "asc");
    assert.strictEqual(byDiffAsc[0].difficulty, "easy");
    assert.strictEqual(byDiffAsc[byDiffAsc.length - 1].difficulty, "hard");

    const byAcceptanceDesc = sortProblems(sampleProblems, "acceptance", "desc");
    assert.strictEqual(byAcceptanceDesc[0].slug, "valid-anagram"); // 63.1%

    const byRuntimeAsc = sortProblems(sampleProblems, "runtime", "asc");
    assert.strictEqual(byRuntimeAsc[0].slug, "two-sum"); // 18ms
    assert.strictEqual(byRuntimeAsc[1].slug, "valid-anagram"); // 24ms
  });

  it("correctly paginates results at 25 items per page", () => {
    const mock60 = Array.from({ length: 60 }, (_, i) => ({
      id: String(i + 1),
      slug: `problem-${i + 1}`,
      title: `Problem ${i + 1}`,
      difficulty: i % 3 === 0 ? "easy" : i % 3 === 1 ? "medium" : "hard",
      topic: "Arrays",
      tags: ["array"],
      status: "todo",
      acceptance_rate: 50.0,
    }));

    const page1 = paginate(mock60, 1, 25);
    assert.strictEqual(page1.items.length, 25);
    assert.strictEqual(page1.total, 60);
    assert.strictEqual(page1.total_pages, 3);
    assert.strictEqual(page1.items[0].id, "1");

    const page3 = paginate(mock60, 3, 25);
    assert.strictEqual(page3.items.length, 10);
    assert.strictEqual(page3.items[9].id, "60");
  });
});
