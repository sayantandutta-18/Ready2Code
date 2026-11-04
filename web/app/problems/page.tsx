"use client";

import React, { useState, useEffect, useMemo, Suspense } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import DifficultyChip from "../../components/ui/DifficultyChip";
import {
  Search,
  Shuffle,
  CheckCircle2,
  Clock,
  Circle,
  Filter,
  Tag,
  BookOpen,
} from "lucide-react";

interface ProblemItem {
  id: string;
  slug: string;
  title: string;
  difficulty: "easy" | "medium" | "hard";
  topic: string;
  tags: string[];
  status: "todo" | "attempted" | "solved";
  acceptance_rate: number;
}

function ProblemsContent() {
  const router = useRouter();
  const searchParams = useSearchParams();

  // Read initial filter values from URL query string
  const initialTopic = searchParams.get("topic") || "all";
  const initialDifficulty = searchParams.get("difficulty") || "all";
  const initialStatus = searchParams.get("status") || "all";
  const initialCompany = searchParams.get("company") || "all";
  const initialSearch = searchParams.get("q") || "";

  const [topic, setTopic] = useState(initialTopic);
  const [difficulty, setDifficulty] = useState(initialDifficulty);
  const [status, setStatus] = useState(initialStatus);
  const [company, setCompany] = useState(initialCompany);
  const [search, setSearch] = useState(initialSearch);
  const [debouncedSearch, setDebouncedSearch] = useState(initialSearch);

  const [problems, setProblems] = useState<ProblemItem[]>([]);
  const [loading, setLoading] = useState(true);

  // 300ms search input debounce (C1.3 specification)
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(search);
    }, 300);
    return () => clearTimeout(timer);
  }, [search]);

  // Sync state to URL query string
  useEffect(() => {
    const params = new URLSearchParams();
    if (topic !== "all") params.set("topic", topic);
    if (difficulty !== "all") params.set("difficulty", difficulty);
    if (status !== "all") params.set("status", status);
    if (company !== "all") params.set("company", company);
    if (debouncedSearch) params.set("q", debouncedSearch);

    const queryString = params.toString();
    const targetUrl = queryString ? `/problems?${queryString}` : "/problems";
    router.replace(targetUrl, { scroll: false });
  }, [topic, difficulty, status, company, debouncedSearch, router]);

  // Fetch problems from API (with fallback starter data if backend is offline)
  useEffect(() => {
    setLoading(true);
    const query = new URLSearchParams({
      topic,
      difficulty,
      company: company === "all" ? "" : company,
      status,
      search: debouncedSearch,
    });

    fetch(`/api/problems?${query.toString()}`)
      .then((res) => {
        if (!res.ok) throw new Error("API request failed");
        return res.json();
      })
      .then((data) => {
        if (Array.isArray(data)) {
          setProblems(data);
        }
        setLoading(false);
      })
      .catch(() => {
        // Fallback starter problems if API is starting up
        setProblems([
          { id: "1", slug: "two-sum", title: "Two Sum", difficulty: "easy", topic: "Arrays", tags: ["Array", "Hash Map", "Google"], status: "todo", acceptance_rate: 68.5 },
          { id: "2", slug: "valid-parentheses", title: "Valid Parentheses", difficulty: "easy", topic: "Stack and Queue", tags: ["Stack", "String", "Amazon"], status: "todo", acceptance_rate: 61.2 },
          { id: "3", slug: "best-time-to-buy-and-sell-stock", title: "Best Time to Buy and Sell Stock", difficulty: "easy", topic: "Arrays", tags: ["Array", "Dynamic Programming", "Apple"], status: "todo", acceptance_rate: 54.8 },
          { id: "4", slug: "binary-search", title: "Binary Search", difficulty: "easy", topic: "Binary Search", tags: ["Binary Search", "Array", "Microsoft"], status: "todo", acceptance_rate: 65.1 },
          { id: "5", slug: "reverse-linked-list", title: "Reverse Linked List", difficulty: "easy", topic: "Linked List", tags: ["Linked List", "Meta"], status: "todo", acceptance_rate: 73.4 },
          { id: "6", slug: "maximum-subarray", title: "Maximum Subarray", difficulty: "medium", topic: "Arrays", tags: ["Array", "Dynamic Programming", "Kadane"], status: "todo", acceptance_rate: 50.2 },
          { id: "7", slug: "climbing-stairs", title: "Climbing Stairs", difficulty: "easy", topic: "DP", tags: ["Dynamic Programming", "Math"], status: "todo", acceptance_rate: 52.3 },
          { id: "8", slug: "number-of-islands", title: "Number of Islands", difficulty: "medium", topic: "Graphs", tags: ["Graph", "BFS", "DFS", "Bloomberg"], status: "todo", acceptance_rate: 57.8 },
          { id: "9", slug: "merge-intervals", title: "Merge Intervals", difficulty: "medium", topic: "Arrays", tags: ["Array", "Sorting", "Google"], status: "todo", acceptance_rate: 46.9 },
          { id: "10", slug: "longest-substring-without-repeating-characters", title: "Longest Substring Without Repeating Characters", difficulty: "medium", topic: "Strings", tags: ["Sliding Window", "Hash Table"], status: "todo", acceptance_rate: 34.6 },
          { id: "11", slug: "coin-change", title: "Coin Change", difficulty: "medium", topic: "DP", tags: ["Dynamic Programming", "BFS"], status: "todo", acceptance_rate: 42.1 },
          { id: "12", slug: "binary-tree-inorder-traversal", title: "Binary Tree Inorder Traversal", difficulty: "easy", topic: "Trees", tags: ["Tree", "DFS", "Stack"], status: "todo", acceptance_rate: 74.3 },
        ]);
        setLoading(false);
      });
  }, [topic, difficulty, status, company, debouncedSearch]);

  // Random unsolved problem picker (C1.3 specification)
  const handleRandomProblem = () => {
    const unsolved = problems.filter((p) => p.status !== "solved");
    const candidates = unsolved.length > 0 ? unsolved : problems;
    if (candidates.length > 0) {
      const chosen = candidates[Math.floor(Math.random() * candidates.length)];
      router.push(`/problems/${chosen.slug}`);
    }
  };

  const statusIcon = (s: string) => {
    if (s === "solved")
      return (
        <span title="Solved">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
        </span>
      );
    if (s === "attempted")
      return (
        <span title="Attempted">
          <Clock className="w-4 h-4 text-amber-400" />
        </span>
      );
    return (
      <span title="Todo">
        <Circle className="w-4 h-4 text-slate-600" />
      </span>
    );
  };

  return (
    <div className="max-w-7xl mx-auto px-4 lg:px-8 py-8 space-y-6">
      {/* Title & Actions Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-black text-white tracking-tight flex items-center gap-3">
            <BookOpen className="w-8 h-8 text-cyan-400" />
            <span>Problem Arena</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Browse and filter {problems.length} high-frequency algorithmic challenges.
          </p>
        </div>

        <button
          onClick={handleRandomProblem}
          className="px-4 py-2.5 rounded-xl bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white font-semibold text-sm shadow-lg shadow-violet-600/20 flex items-center gap-2 self-start sm:self-auto transition-all"
        >
          <Shuffle className="w-4 h-4" />
          <span>Pick Random Unsolved</span>
        </button>
      </div>

      {/* Filter Controls Bar */}
      <div className="bg-[#121C2F] rounded-2xl border border-slate-800 p-4 space-y-4 shadow-xl">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
          {/* Search Box */}
          <div className="lg:col-span-2 relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search problems by title, tag..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-[#0B1220] border border-slate-700 rounded-xl pl-9 pr-4 py-2 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-400 transition-colors"
            />
          </div>

          {/* Topic Select */}
          <div>
            <select
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              aria-label="Filter by Topic"
              className="w-full bg-[#0B1220] border border-slate-700 rounded-xl px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-cyan-400"
            >
              <option value="all">All Topics</option>
              <option value="arrays">Arrays</option>
              <option value="strings">Strings</option>
              <option value="linked-list">Linked List</option>
              <option value="stack-and-queue">Stack and Queue</option>
              <option value="trees">Trees</option>
              <option value="graphs">Graphs</option>
              <option value="dp">Dynamic Programming</option>
              <option value="binary-search">Binary Search</option>
            </select>
          </div>

          {/* Difficulty Select */}
          <div>
            <select
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
              aria-label="Filter by Difficulty"
              className="w-full bg-[#0B1220] border border-slate-700 rounded-xl px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-cyan-400"
            >
              <option value="all">All Difficulties</option>
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>

          {/* Status Select */}
          <div>
            <select
              value={status}
              onChange={(e) => setStatus(e.target.value)}
              aria-label="Filter by Status"
              className="w-full bg-[#0B1220] border border-slate-700 rounded-xl px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-cyan-400"
            >
              <option value="all">All Statuses</option>
              <option value="todo">Todo</option>
              <option value="attempted">Attempted</option>
              <option value="solved">Solved</option>
            </select>
          </div>
        </div>
      </div>

      {/* Problems Table */}
      <div className="bg-[#121C2F] rounded-2xl border border-slate-800 overflow-hidden shadow-2xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-800 text-[11px] uppercase tracking-wider text-slate-400 bg-[#0E1726]/60 font-semibold">
                <th className="py-3.5 px-4 w-12 text-center">Status</th>
                <th className="py-3.5 px-4">Title</th>
                <th className="py-3.5 px-4 w-32">Difficulty</th>
                <th className="py-3.5 px-4 w-36">Topic</th>
                <th className="py-3.5 px-4">Tags</th>
                <th className="py-3.5 px-4 w-28 text-right">Acceptance</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-sm">
              {loading ? (
                <tr>
                  <td colSpan={6} className="py-12 text-center text-slate-400 font-mono text-xs">
                    Loading problem catalogue...
                  </td>
                </tr>
              ) : problems.length === 0 ? (
                <tr>
                  <td colSpan={6} className="py-12 text-center text-slate-500">
                    No problems match the selected filters.
                  </td>
                </tr>
              ) : (
                problems.map((p, index) => (
                  <tr
                    key={p.slug}
                    className="hover:bg-slate-800/40 transition-colors group cursor-pointer"
                  >
                    <td className="py-3.5 px-4 text-center">
                      <div className="flex justify-center">{statusIcon(p.status)}</div>
                    </td>
                    <td className="py-3.5 px-4 font-semibold text-slate-100 group-hover:text-cyan-300 transition-colors">
                      <Link href={`/problems/${p.slug}`} className="block">
                        <span className="text-slate-500 mr-2 font-mono text-xs">
                          {index + 1}.
                        </span>
                        {p.title}
                      </Link>
                    </td>
                    <td className="py-3.5 px-4">
                      <DifficultyChip difficulty={p.difficulty} />
                    </td>
                    <td className="py-3.5 px-4 text-xs text-slate-300">{p.topic}</td>
                    <td className="py-3.5 px-4">
                      <div className="flex flex-wrap gap-1.5">
                        {p.tags.slice(0, 3).map((tag) => (
                          <span
                            key={tag}
                            className="px-2 py-0.5 rounded-md bg-[#0B1220] border border-slate-700/60 text-[11px] text-slate-400"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className="py-3.5 px-4 text-xs font-mono text-slate-400 text-right">
                      {p.acceptance_rate}%
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default function ProblemsPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center text-slate-500">Loading problem arena...</div>}>
      <ProblemsContent />
    </Suspense>
  );
}
