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
import { useAuth } from "../../lib/authContext";
import {
  Search,
  Shuffle,
  CheckCircle2,
  Clock,
  Circle,
  Filter,
  Tag as TagIcon,
  BookOpen,
  RotateCcw,
  ChevronLeft,
  ChevronRight,
  ArrowUpDown,
  ArrowUp,
  ArrowDown,
  Zap,
} from "lucide-react";

interface ProblemItem {
  id: string;
  slug: string;
  title: string;
  difficulty: "easy" | "medium" | "hard";
  topic: string;
  tags: string[];
  status: "todo" | "attempted" | "solved";
  best_runtime_ms?: number | null;
  acceptance_rate: number;
}

interface PaginatedProblemsResponse {
  items: ProblemItem[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

function ProblemsContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { user } = useAuth();

  // Read initial filter values from URL query string
  const initialTopic = searchParams.get("topic") || "all";
  const initialDifficulty = searchParams.get("difficulty") || "all";
  const initialStatus = searchParams.get("status") || "all";
  const initialCompany = searchParams.get("company") || "all";
  const initialTag = searchParams.get("tag") || "all";
  const initialSort = searchParams.get("sort") || "id";
  const initialOrder = searchParams.get("order") || "asc";
  const initialSearch = searchParams.get("q") || "";
  const initialPage = parseInt(searchParams.get("page") || "1", 10);

  const [topic, setTopic] = useState(initialTopic);
  const [difficulty, setDifficulty] = useState(initialDifficulty);
  const [status, setStatus] = useState(initialStatus);
  const [company, setCompany] = useState(initialCompany);
  const [tag, setTag] = useState(initialTag);
  const [sortBy, setSortBy] = useState(initialSort);
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">(initialOrder as "asc" | "desc");
  const [page, setPage] = useState(initialPage);
  const [search, setSearch] = useState(initialSearch);
  const [debouncedSearch, setDebouncedSearch] = useState(initialSearch);

  // 300ms search input debounce (C1.3 specification)
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(search);
      setPage(1); // Reset to page 1 on search change
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
    if (tag !== "all") params.set("tag", tag);
    if (sortBy !== "id") params.set("sort", sortBy);
    if (sortOrder !== "asc") params.set("order", sortOrder);
    if (page > 1) params.set("page", String(page));
    if (debouncedSearch) params.set("q", debouncedSearch);

    const queryString = params.toString();
    const targetUrl = queryString ? `/problems?${queryString}` : "/problems";
    router.replace(targetUrl, { scroll: false });
  }, [topic, difficulty, status, company, tag, sortBy, sortOrder, page, debouncedSearch, router]);

  // Server-side filtered, sorted, and paginated query (25 per page)
  const {
    data: pagedData,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<PaginatedProblemsResponse>({
    queryKey: [
      "problems",
      {
        topic,
        difficulty,
        company,
        tag,
        status,
        search: debouncedSearch,
        sortBy,
        sortOrder,
        page,
        userId: user?.id,
      },
    ],
    queryFn: () => {
      const query = new URLSearchParams({
        topic,
        difficulty,
        company: company === "all" ? "" : company,
        tag: tag === "all" ? "" : tag,
        status,
        search: debouncedSearch,
        sort_by: sortBy,
        sort_order: sortOrder,
        page: String(page),
        limit: "25",
      });
      if (user?.id) {
        query.set("user_id", user.id);
      }
      return fetchApi<PaginatedProblemsResponse>(`/problems?${query.toString()}`);
    },
  });

  const problems = pagedData?.items || [];
  const totalCount = pagedData?.total || 0;
  const totalPages = pagedData?.total_pages || 1;

  const handleClearFilters = () => {
    setTopic("all");
    setDifficulty("all");
    setStatus("all");
    setCompany("all");
    setTag("all");
    setSortBy("id");
    setSortOrder("asc");
    setPage(1);
    setSearch("");
    setDebouncedSearch("");
  };

  const handleSort = (field: string) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortBy(field);
      setSortOrder("asc");
    }
    setPage(1);
  };

  // Random unsolved problem picker
  const handleRandomProblem = () => {
    const unsolved = problems.filter((p) => p.status !== "solved");
    const candidates = unsolved.length > 0 ? unsolved : problems;
    if (candidates.length > 0) {
      const chosen = candidates[Math.floor(Math.random() * candidates.length)];
      router.push(`/problems/${chosen.slug}`);
    }
  };

  const renderSortIndicator = (field: string) => {
    if (sortBy !== field) {
      return <ArrowUpDown className="w-3 h-3 text-slate-500 inline ml-1 opacity-60" />;
    }
    return sortOrder === "asc" ? (
      <ArrowUp className="w-3 h-3 text-cyan-400 inline ml-1" />
    ) : (
      <ArrowDown className="w-3 h-3 text-cyan-400 inline ml-1" />
    );
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
              {isLoading ? "..." : `${totalCount} Available`}
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

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2.5 pt-1">
          {/* Topic Filter */}
          <div>
            <label className="text-[10px] font-mono uppercase text-slate-400 block mb-1">Topic</label>
            <select
              value={topic}
              onChange={(e) => {
                setTopic(e.target.value);
                setPage(1);
              }}
              aria-label="Filter by Topic"
              className="w-full bg-[#0B1220] border border-slate-700 rounded-xl px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-cyan-400"
            >
              <option value="all">All Topics</option>
              <option value="arrays">Arrays & Hashing</option>
              <option value="two-pointers">Two Pointers & Sliding Window</option>
              <option value="strings">Strings</option>
              <option value="stack-and-queue">Stack & Queue</option>
              <option value="linked-list">Linked List</option>
              <option value="trees">Trees</option>
              <option value="graphs">Graphs</option>
              <option value="binary-search">Binary Search</option>
              <option value="dp">Dynamic Programming</option>
              <option value="heap-and-intervals">Heap & Intervals</option>
            </select>
          </div>

          {/* Difficulty Filter */}
          <div>
            <label className="text-[10px] font-mono uppercase text-slate-400 block mb-1">Difficulty</label>
            <select
              value={difficulty}
              onChange={(e) => {
                setDifficulty(e.target.value);
                setPage(1);
              }}
              aria-label="Filter by Difficulty"
              className="w-full bg-[#0B1220] border border-slate-700 rounded-xl px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-cyan-400"
            >
              <option value="all">All Difficulties</option>
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>

          {/* Status Filter */}
          <div>
            <label className="text-[10px] font-mono uppercase text-slate-400 block mb-1">Status</label>
            <select
              value={status}
              onChange={(e) => {
                setStatus(e.target.value);
                setPage(1);
              }}
              aria-label="Filter by Status"
              className="w-full bg-[#0B1220] border border-slate-700 rounded-xl px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-cyan-400"
            >
              <option value="all">All Statuses</option>
              <option value="todo">Todo</option>
              <option value="attempted">Attempted</option>
              <option value="solved">Solved</option>
            </select>
          </div>

          {/* Pattern / Tag Filter */}
          <div>
            <label className="text-[10px] font-mono uppercase text-slate-400 block mb-1">Pattern / Tag</label>
            <select
              value={tag}
              onChange={(e) => {
                setTag(e.target.value);
                setPage(1);
              }}
              aria-label="Filter by Tag"
              className="w-full bg-[#0B1220] border border-slate-700 rounded-xl px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-cyan-400"
            >
              <option value="all">All Tags</option>
              <option value="Two Pointers">Two Pointers</option>
              <option value="Sliding Window">Sliding Window</option>
              <option value="Hash Map">Hash Map</option>
              <option value="Binary Search">Binary Search</option>
              <option value="Monotonic Stack">Monotonic Stack</option>
              <option value="Fast & Slow Pointers">Fast & Slow Pointers</option>
              <option value="Breadth-First Search">BFS Traversal</option>
              <option value="Depth-First Search">DFS Traversal</option>
              <option value="Dynamic Programming">Dynamic Programming</option>
              <option value="Heap">Heap & Priority Queue</option>
              <option value="Intervals">Intervals</option>
            </select>
          </div>

          {/* Company Filter */}
          <div>
            <label className="text-[10px] font-mono uppercase text-slate-400 block mb-1">Company</label>
            <select
              value={company}
              onChange={(e) => {
                setCompany(e.target.value);
                setPage(1);
              }}
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
              <tr className="border-b border-slate-800 text-[11px] uppercase tracking-wider text-slate-400 bg-[#0E1726]/60 font-semibold select-none">
                <th
                  onClick={() => handleSort("status")}
                  className="py-3.5 px-4 w-16 text-center cursor-pointer hover:text-cyan-300 transition-colors"
                >
                  Status {renderSortIndicator("status")}
                </th>
                <th
                  onClick={() => handleSort("title")}
                  className="py-3.5 px-4 cursor-pointer hover:text-cyan-300 transition-colors"
                >
                  Title {renderSortIndicator("title")}
                </th>
                <th
                  onClick={() => handleSort("difficulty")}
                  className="py-3.5 px-4 w-32 cursor-pointer hover:text-cyan-300 transition-colors"
                >
                  Difficulty {renderSortIndicator("difficulty")}
                </th>
                <th
                  onClick={() => handleSort("topic")}
                  className="py-3.5 px-4 w-44 cursor-pointer hover:text-cyan-300 transition-colors"
                >
                  Topic {renderSortIndicator("topic")}
                </th>
                <th className="py-3.5 px-4">Tags</th>
                <th
                  onClick={() => handleSort("acceptance")}
                  className="py-3.5 px-4 w-28 text-right cursor-pointer hover:text-cyan-300 transition-colors"
                >
                  Acceptance {renderSortIndicator("acceptance")}
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-sm">
              {isLoading ? (
                <tr>
                  <td colSpan={6} className="py-8 px-4">
                    <LoadingSkeleton rows={10} />
                  </td>
                </tr>
              ) : problems.length === 0 ? (
                <tr>
                  <td colSpan={6} className="p-8">
                    <EmptyState
                      title="No problems match these filters"
                      description="Try clearing your search query or broadening the selected topic, difficulty, or tag filters."
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
                      <Link href={`/problems/${p.slug}`} className="flex items-center gap-2">
                        <span className="text-slate-500 font-mono text-xs">
                          {(page - 1) * 25 + index + 1}.
                        </span>
                        <span>{p.title}</span>
                        {p.status === "solved" && p.best_runtime_ms && (
                          <span
                            title="Your best recorded runtime"
                            className="inline-flex items-center gap-1 text-[10px] font-mono px-1.5 py-0.5 rounded bg-cyan-950/80 text-cyan-400 border border-cyan-800/60 ml-1.5"
                          >
                            <Zap className="w-2.5 h-2.5" />
                            {p.best_runtime_ms} ms
                          </span>
                        )}
                      </Link>
                    </td>
                    <td className="py-3.5 px-4">
                      <DifficultyChip difficulty={p.difficulty} />
                    </td>
                    <td className="py-3.5 px-4 text-xs text-slate-300">{p.topic}</td>
                    <td className="py-3.5 px-4">
                      <div className="flex flex-wrap gap-1.5">
                        {p.tags.slice(0, 3).map((t) => (
                          <span
                            key={t}
                            onClick={(e) => {
                              e.stopPropagation();
                              setTag(t);
                              setPage(1);
                            }}
                            className="px-2 py-0.5 rounded-md bg-[#0B1220] border border-slate-700/60 text-[11px] text-slate-400 hover:text-cyan-300 hover:border-cyan-500/40 transition-colors cursor-pointer"
                          >
                            {t}
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

        {/* Server-Side Pagination Bar (25 items per page) */}
        {!isLoading && totalCount > 0 && (
          <div className="flex flex-col sm:flex-row items-center justify-between px-6 py-4 border-t border-slate-800 bg-[#0E1726]/40 gap-3 text-xs text-slate-400">
            <div>
              Showing{" "}
              <span className="text-slate-200 font-mono font-medium">
                {(page - 1) * 25 + 1}–{Math.min(page * 25, totalCount)}
              </span>{" "}
              of <span className="text-slate-200 font-mono font-medium">{totalCount}</span> problems
            </div>

            <div className="flex items-center gap-1.5">
              <button
                onClick={() => setPage((prev) => Math.max(1, prev - 1))}
                disabled={page <= 1}
                className="px-3 py-1.5 rounded-lg border border-slate-700 bg-[#0B1220] hover:bg-slate-800 text-slate-300 disabled:opacity-40 disabled:pointer-events-none flex items-center gap-1 transition-colors"
                aria-label="Previous Page"
              >
                <ChevronLeft className="w-3.5 h-3.5" />
                <span>Prev</span>
              </button>

              {Array.from({ length: totalPages }).map((_, idx) => {
                const pNum = idx + 1;
                const isCurrent = pNum === page;
                return (
                  <button
                    key={pNum}
                    onClick={() => setPage(pNum)}
                    className={`w-8 h-8 rounded-lg font-mono font-medium text-xs transition-colors ${
                      isCurrent
                        ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm"
                        : "bg-[#0B1220] border border-slate-700 hover:bg-slate-800 text-slate-400"
                    }`}
                  >
                    {pNum}
                  </button>
                );
              })}

              <button
                onClick={() => setPage((prev) => Math.min(totalPages, prev + 1))}
                disabled={page >= totalPages}
                className="px-3 py-1.5 rounded-lg border border-slate-700 bg-[#0B1220] hover:bg-slate-800 text-slate-300 disabled:opacity-40 disabled:pointer-events-none flex items-center gap-1 transition-colors"
                aria-label="Next Page"
              >
                <span>Next</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        )}
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
