"use client";

import React, { useState, useEffect, Suspense } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import DifficultyChip from "../../components/ui/DifficultyChip";
import LoadingSkeleton from "../../components/ui/LoadingSkeleton";
import EmptyState from "../../components/ui/EmptyState";
import QueryErrorState from "../../components/ui/QueryErrorState";
import { fetchApi } from "../../lib/api";
import {
  Search,
  Shuffle,
  CheckCircle2,
  Clock,
  Circle,
  Filter,
  Tag,
  BookOpen,
  RotateCcw,
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

  // TanStack Query for real server-side data fetching
  const {
    data: problems = [],
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<ProblemItem[]>({
    queryKey: ["problems", { topic, difficulty, company, status, search: debouncedSearch }],
    queryFn: () => {
      const query = new URLSearchParams({
        topic,
        difficulty,
        company: company === "all" ? "" : company,
        status,
        search: debouncedSearch,
      });
      return fetchApi<ProblemItem[]>(`/problems?${query.toString()}`);
    },
  });

  const handleClearFilters = () => {
    setTopic("all");
    setDifficulty("all");
    setStatus("all");
    setCompany("all");
    setSearch("");
    setDebouncedSearch("");
  };

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
      <span title="To Do">
        <Circle className="w-4 h-4 text-slate-600" />
      </span>
    );
  };

  return (
    <div className="max-w-7xl mx-auto px-4 lg:px-8 py-8 space-y-6">
      {/* Header & Controls */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-black text-white tracking-tight flex items-center gap-3">
            <BookOpen className="w-8 h-8 text-cyan-400" />
            <span>Problem Arena</span>
            <span className="text-xs px-2.5 py-1 rounded-full bg-cyan-950 border border-cyan-800 text-cyan-300 font-mono font-medium">
              {isLoading ? "..." : `${problems.length} Available`}
            </span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Curated algorithmic challenges categorized by pattern, topic, and difficulty.
          </p>
        </div>

        {/* Random Unsolved Picker */}
        <button
          onClick={handleRandomProblem}
          disabled={isLoading || problems.length === 0}
          className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-500 hover:from-cyan-600 hover:to-indigo-600 text-slate-950 font-bold text-xs uppercase tracking-wider shadow-lg shadow-cyan-500/20 active:scale-95 transition-all self-start md:self-auto disabled:opacity-50"
        >
          <Shuffle className="w-4 h-4" />
          <span>Pick Random Unsolved</span>
        </button>
      </div>

      {/* Filter and Search Bar */}
      <div className="p-4 rounded-2xl bg-[#121C2F] border border-slate-800 space-y-3 shadow-xl">
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search problems by name or tag (e.g. 'Two Sum', 'Sliding Window', 'Google')..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full bg-[#0B1220] border border-slate-700 rounded-xl pl-10 pr-4 py-2.5 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-400 transition-colors"
          />
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 pt-1">
          {/* Topic Filter */}
          <div>
            <label className="text-[10px] font-mono uppercase text-slate-400 block mb-1">Topic</label>
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
              <option value="stack-and-queue">Stack & Queue</option>
              <option value="trees">Trees</option>
              <option value="graphs">Graphs</option>
              <option value="dp">Dynamic Programming</option>
              <option value="binary-search">Binary Search</option>
            </select>
          </div>

          {/* Difficulty Filter */}
          <div>
            <label className="text-[10px] font-mono uppercase text-slate-400 block mb-1">Difficulty</label>
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

          {/* Company Filter */}
          <div>
            <label className="text-[10px] font-mono uppercase text-slate-400 block mb-1">Company</label>
            <select
              value={company}
              onChange={(e) => setCompany(e.target.value)}
              aria-label="Filter by Company"
              className="w-full bg-[#0B1220] border border-slate-700 rounded-xl px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-cyan-400"
            >
              <option value="all">All Companies</option>
              <option value="Google">Google</option>
              <option value="Amazon">Amazon</option>
              <option value="Meta">Meta</option>
              <option value="Microsoft">Microsoft</option>
              <option value="Apple">Apple</option>
              <option value="Uber">Uber</option>
            </select>
          </div>

          {/* Status Filter */}
          <div>
            <label className="text-[10px] font-mono uppercase text-slate-400 block mb-1">Status</label>
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

      {/* Error State */}
      {isError && (
        <QueryErrorState
          title="Could not load problems"
          message={error instanceof Error ? error.message : "Unable to reach the backend service."}
          onRetry={() => refetch()}
        />
      )}

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
              {isLoading ? (
                <tr>
                  <td colSpan={6} className="py-8 px-4">
                    <LoadingSkeleton rows={8} />
                  </td>
                </tr>
              ) : problems.length === 0 ? (
                <tr>
                  <td colSpan={6} className="p-8">
                    <EmptyState
                      title="No problems match these filters"
                      description="Try clearing your search query or broadening the selected topic, difficulty, or company filters."
                      actionText="Clear all filters"
                      onAction={handleClearFilters}
                    />
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
