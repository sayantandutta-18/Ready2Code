"use client";

import React, { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import confetti from "canvas-confetti";
import CodeEditor from "../../../components/ui/CodeEditor";
import TestCaseTable, { TestCaseResult } from "../../../components/ui/TestCaseTable";
import DifficultyChip from "../../../components/ui/DifficultyChip";
import VerdictBadge from "../../../components/ui/VerdictBadge";
import LoadingSkeleton from "../../../components/ui/LoadingSkeleton";
import QueryErrorState from "../../../components/ui/QueryErrorState";
import EmptyState from "../../../components/ui/EmptyState";
import { fetchApi } from "../../../lib/api";
import { useAuth } from "../../../lib/authContext";
import {
  Play,
  Send,
  Bookmark,
  Sparkles,
  BookOpen,
  HelpCircle,
  PlaySquare,
  History,
  Layers,
  Check,
  Loader2,
  CheckCircle2,
} from "lucide-react";

const DEFAULT_STARTER_CODES: Record<string, string> = {
  python: `def solution():
    # Write your solution here
    pass
`,
  javascript: `function solution() {
    // Write your solution here
}
`,
  "c++": `#include <vector>
using namespace std;

class Solution {
public:
    void solve() {
        // Write your solution here
    }
};
`,
  java: `class Solution {
    public void solve() {
        // Write your solution here
    }
}
`,
};

export default function ProblemSolvePage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const router = useRouter();
  const queryClient = useQueryClient();
  const { user, requireAuth } = useAuth();

  const [activeTab, setActiveTab] = useState<
    "statement" | "hints" | "editorial" | "notes" | "ai" | "submissions"
  >("statement");
  const [mobileView, setMobileView] = useState<"statement" | "editor">("statement");
  const [language, setLanguage] = useState<string>("python");
  const [code, setCode] = useState<string>("");

  // Notes state & autosave
  const [noteContent, setNoteContent] = useState<string>("");
  const [noteStatus, setNoteStatus] = useState<"saved" | "saving" | "unsaved" | "sign-in" | "error">("saved");
  const noteTimerRef = useRef<NodeJS.Timeout | null>(null);

  // Bookmarking
  const [isBookmarked, setIsBookmarked] = useState<boolean>(false);

  // Toast message
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  // Execution states
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [testResults, setTestResults] = useState<TestCaseResult[]>([]);
  const [submissionVerdict, setSubmissionVerdict] = useState<any>(null);
  const [editorialRevealed, setEditorialRevealed] = useState<boolean>(false);

  // Socratic hints state
  const [unlockedHintLevel, setUnlockedHintLevel] = useState<number>(1);
  const [aiReview, setAiReview] = useState<any>(null);

  // Past submissions list
  const [pastSubmissions, setPastSubmissions] = useState<any[]>([]);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 3500);
  };

  // Fetch problem details with TanStack Query
  const {
    data: problem,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery({
    queryKey: ["problem", slug, user?.id],
    queryFn: () => {
      const url = user ? `/problems/${slug}?user_id=${user.id}` : `/problems/${slug}`;
      return fetchApi<any>(url);
    },
  });

  // Keep editorial revealed if user already solved it
  useEffect(() => {
    if (problem?.user_status === "solved") {
      setEditorialRevealed(true);
    }
  }, [problem]);

  // Load user note & bookmark status
  useEffect(() => {
    if (user) {
      fetchApi<{ body_md: string }>(`/notes/${slug}`)
        .then((data) => {
          if (data && data.body_md) {
            setNoteContent(data.body_md);
            setNoteStatus("saved");
          }
        })
        .catch(() => {});

      fetchApi<{ bookmarked: boolean }>(`/users/me/bookmarks?problem_id=${slug}`)
        .then((data) => {
          if (data) setIsBookmarked(data.bookmarked);
        })
        .catch(() => {});
    }

    fetchApi<any[]>(`/submissions?problem_id=${slug}`)
      .then((data) => {
        if (Array.isArray(data)) setPastSubmissions(data);
      })
      .catch(() => {});
  }, [slug, user]);

  // Build starter codes dictionary combining backend starter_code + defaults
  const starterCodes: Record<string, string> = {
    ...DEFAULT_STARTER_CODES,
  };
  if (problem?.starter_code) {
    if (typeof problem.starter_code === "object") {
      Object.assign(starterCodes, problem.starter_code);
    } else if (typeof problem.starter_code === "string") {
      starterCodes["python"] = problem.starter_code;
    }
  }

  // Restore draft or starter code when problem/language changes
  useEffect(() => {
    if (typeof window === "undefined") return;
    const key = `ready2code_draft_${slug}_${language}`;
    const savedDraft = localStorage.getItem(key);
    if (savedDraft !== null && savedDraft.trim().length > 0) {
      setCode(savedDraft);
    } else if (starterCodes[language]) {
      setCode(starterCodes[language]);
    }
  }, [slug, language, problem]);

  // Unsaved code confirmation before leaving window
  useEffect(() => {
    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      const defaultCode = starterCodes[language] || "";
      if (code.trim().length > 0 && code !== defaultCode) {
        e.preventDefault();
        e.returnValue = "You have unsaved code changes. Are you sure you want to leave?";
        return e.returnValue;
      }
    };
    window.addEventListener("beforeunload", handleBeforeUnload);
    return () => window.removeEventListener("beforeunload", handleBeforeUnload);
  }, [code, language, starterCodes]);

  // Autosave notes to server
  const handleNoteChange = (text: string) => {
    setNoteContent(text);
    if (!user) {
      setNoteStatus("sign-in");
      return;
    }
    setNoteStatus("unsaved");
    if (noteTimerRef.current) clearTimeout(noteTimerRef.current);
    noteTimerRef.current = setTimeout(async () => {
      setNoteStatus("saving");
      try {
        await fetchApi<{ status: string }>("/notes", {
          method: "POST",
          body: JSON.stringify({ problem_id: slug, body_md: text }),
        });
        setNoteStatus("saved");
      } catch {
        setNoteStatus("error");
      }
    }, 1500);
  };

  // Toggle bookmark with server persistence
  const handleToggleBookmark = () => {
    requireAuth(async () => {
      try {
        const data = await fetchApi<{ bookmarked: boolean }>("/users/me/bookmarks/toggle", {
          method: "POST",
          body: JSON.stringify({ problem_id: slug }),
        });
        setIsBookmarked(data.bookmarked);
        showToast(data.bookmarked ? "Problem bookmarked!" : "Bookmark removed.");
      } catch {
        showToast("Could not update bookmark.");
      }
    });
  };

  // Run on Sample Tests
  const handleRun = async () => {
    setIsRunning(true);
    setSubmissionVerdict(null);
    try {
      const data = await fetchApi<any>("/submissions/run", {
        method: "POST",
        body: JSON.stringify({
          problem_id: slug,
          language,
          code,
        }),
      });
      setTestResults(data.results || []);
      showToast(data.overall_status === "Accepted" ? "Sample tests passed!" : "Some sample tests failed.");
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Judge is unavailable, try again";
      showToast(msg);
    } finally {
      setIsRunning(false);
    }
  };

  // Submit on Hidden Tests
  const handleSubmit = () => {
    requireAuth(async () => {
      setIsSubmitting(true);
      try {
        const data = await fetchApi<any>("/submissions", {
          method: "POST",
          body: JSON.stringify({
            problem_id: slug,
            language,
            code,
            user_id: user?.id,
          }),
        });
        setSubmissionVerdict(data);
        if (data.verdict === "AC") {
          setEditorialRevealed(true);
          showToast(`Accepted! Beats ${data.runtime_percentile}% of submissions.`);
          confetti({
            particleCount: 90,
            spread: 70,
            origin: { y: 0.6 },
            colors: ["#22D3EE", "#8B5CF6", "#22C55E"],
          });
          // Invalidate problems list query so it shows "Solved"
          queryClient.invalidateQueries({ queryKey: ["problems"] });
          queryClient.invalidateQueries({ queryKey: ["problem", slug] });
        } else {
          showToast(`Verdict: ${data.verdict} on test #${data.failed_test_index || 1}`);
        }

        // Refresh past submissions
        fetchApi<any[]>(`/submissions?problem_id=${slug}`)
          .then((d) => Array.isArray(d) && setPastSubmissions(d))
          .catch(() => {});
      } catch (err: unknown) {
        const msg = err instanceof Error ? err.message : "Judge is unavailable, try again";
        showToast(msg);
      } finally {
        setIsSubmitting(false);
      }
    });
  };

  // Keyboard shortcut: Ctrl+Enter runs samples, Ctrl+Shift+Enter submits
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        e.preventDefault();
        if (e.shiftKey) {
          handleSubmit();
        } else {
          handleRun();
        }
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [code, language]);

  // AI Code Review
  const handleRequestAiReview = async () => {
    try {
      const res = await fetch("/api/ai/review", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ problem_id: slug, code }),
      });
      if (res.ok) {
        const data = await res.json();
        setAiReview(data);
        setActiveTab("ai");
        showToast("AI code complexity analysis generated.");
      }
    } catch {}
  };

  if (isLoading) {
    return (
      <div className="max-w-7xl mx-auto px-4 lg:px-8 py-10 space-y-6">
        <div className="h-8 w-64 bg-slate-800 rounded-lg animate-pulse" />
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-5 p-6 rounded-2xl bg-[#121C2F] border border-slate-800">
            <LoadingSkeleton rows={12} />
          </div>
          <div className="lg:col-span-7 h-[500px] rounded-2xl bg-[#121C2F] border border-slate-800 flex items-center justify-center text-slate-500 font-mono text-xs">
            Loading editor and problem workspace...
          </div>
        </div>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-16">
        <QueryErrorState
          title={`Problem '${slug}' could not be loaded`}
          message={error instanceof Error ? error.message : "Unable to reach the Ready2Code backend."}
          onRetry={() => refetch()}
        />
        <div className="text-center mt-4">
          <Link href="/problems" className="text-xs text-cyan-400 hover:underline">
            &larr; Back to Problem Arena
          </Link>
        </div>
      </div>
    );
  }

  if (!problem) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-16">
        <EmptyState
          title="Problem Not Found"
          description={`The problem '${slug}' was not found in the database.`}
          actionText="Back to Problems"
          onAction={() => router.push("/problems")}
        />
      </div>
    );
  }

  return (
    <div className="h-[calc(100vh-65px)] flex flex-col overflow-hidden bg-[#0B1220]">
      {/* Toast Notification Banner */}
      {toastMessage && (
        <div className="fixed top-16 right-6 z-50 bg-[#121C2F] border border-cyan-500/40 text-cyan-200 px-4 py-2.5 rounded-xl shadow-2xl text-xs font-semibold flex items-center gap-2 animate-bounce">
          <Check className="w-4 h-4 text-cyan-400" />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Top Problem Header */}
      <div className="px-4 sm:px-6 py-2.5 bg-[#121C2F] border-b border-slate-800 flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-2 sm:gap-3 min-w-0">
          <Link href="/problems" className="min-h-[44px] flex items-center text-xs text-slate-400 hover:text-cyan-400 font-mono shrink-0">
            &larr; Problems
          </Link>
          <span className="text-slate-600">/</span>
          <h1 className="text-sm sm:text-base font-bold text-white flex items-center gap-2 truncate">
            <span className="truncate">{problem.title}</span>
            <DifficultyChip difficulty={problem.difficulty} />
            {problem.user_status === "solved" && (
              <span className="inline-flex items-center gap-1 text-[11px] font-mono px-2 py-0.5 rounded-full bg-emerald-950 border border-emerald-700/60 text-emerald-300 shrink-0">
                <CheckCircle2 className="w-3 h-3 text-emerald-400" /> Solved
              </span>
            )}
          </h1>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          {/* Optimization Ladder shortcut */}
          <Link
            href={`/ladder/${slug}`}
            className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-violet-500/10 hover:bg-violet-500/20 text-violet-300 border border-violet-500/30 text-xs font-semibold transition-all min-h-[44px]"
            title="Brute to Optimal Ladder"
          >
            <Layers className="w-3.5 h-3.5 text-violet-400" />
            <span>Optimization Ladder</span>
          </Link>

          {/* Visualizer shortcut */}
          <Link
            href={`/visualizer/${slug}`}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 text-xs font-semibold transition-all min-h-[44px]"
            title="Launch 3D Algorithm Visualizer"
          >
            <PlaySquare className="w-3.5 h-3.5 text-cyan-400" />
            <span className="hidden sm:inline">3D Visualizer</span>
          </Link>

          {/* Bookmark Button */}
          <button
            onClick={handleToggleBookmark}
            className={`min-w-[44px] min-h-[44px] flex items-center justify-center rounded-xl border text-xs transition-colors ${
              isBookmarked
                ? "bg-amber-500/20 border-amber-500/40 text-amber-300"
                : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white"
            }`}
            title="Bookmark Problem"
            aria-label="Bookmark Problem"
          >
            <Bookmark className={`w-4 h-4 ${isBookmarked ? "fill-amber-400" : ""}`} />
          </button>
        </div>
      </div>

      {/* Mobile Tab Switcher (Below 768px: Problem vs Code) (Rule 5 & Rule 6) */}
      <div className="md:hidden flex bg-[#0B1220] p-1.5 border-b border-slate-800 text-sm font-semibold shrink-0">
        <button
          onClick={() => setMobileView("statement")}
          className={`flex-1 min-h-[44px] py-2 font-bold text-center rounded-xl transition-all ${
            mobileView === "statement"
              ? "bg-gradient-to-r from-cyan-500/20 to-indigo-500/20 text-cyan-300 border border-cyan-500/30 shadow-sm"
              : "text-slate-400 hover:text-white"
          }`}
        >
          Problem
        </button>
        <button
          onClick={() => setMobileView("editor")}
          className={`flex-1 min-h-[44px] py-2 font-bold text-center rounded-xl transition-all ${
            mobileView === "editor"
              ? "bg-gradient-to-r from-cyan-500/20 to-indigo-500/20 text-cyan-300 border border-cyan-500/30 shadow-sm"
              : "text-slate-400 hover:text-white"
          }`}
        >
          Code
        </button>
      </div>

      {/* Main Split Pane Layout */}
      <div className="flex-1 grid grid-cols-1 md:grid-cols-12 overflow-hidden">
        {/* Left Pane: Tabs (Description, Hints, Editorial, Notes, AI Review, Submissions) */}
        <div
          className={`md:col-span-5 border-r border-slate-800 flex-col h-full bg-[#0D1524] overflow-hidden ${
            mobileView === "statement" ? "flex" : "hidden md:flex"
          }`}
        >
          {/* Tab buttons */}
          <div className="flex items-center gap-1 p-2 bg-[#121C2F] border-b border-slate-800 text-xs overflow-x-auto">
            <button
              onClick={() => setActiveTab("statement")}
              className={`min-h-[44px] flex items-center gap-1.5 px-3 py-1.5 rounded-lg font-medium transition-all ${
                activeTab === "statement"
                  ? "bg-slate-800 text-cyan-300 border border-cyan-500/30"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              <BookOpen className="w-3.5 h-3.5" />
              <span>Description</span>
            </button>

            <button
              onClick={() => setActiveTab("hints")}
              className={`min-h-[44px] flex items-center gap-1.5 px-3 py-1.5 rounded-lg font-medium transition-all ${
                activeTab === "hints"
                  ? "bg-slate-800 text-cyan-300 border border-cyan-500/30"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              <HelpCircle className="w-3.5 h-3.5" />
              <span>Hints</span>
            </button>

            <button
              onClick={() => setActiveTab("editorial")}
              className={`min-h-[44px] flex items-center gap-1.5 px-3 py-1.5 rounded-lg font-medium transition-all ${
                activeTab === "editorial"
                  ? "bg-slate-800 text-cyan-300 border border-cyan-500/30"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>Editorial</span>
            </button>

            <button
              onClick={() => setActiveTab("notes")}
              className={`min-h-[44px] flex items-center gap-1.5 px-3 py-1.5 rounded-lg font-medium transition-all ${
                activeTab === "notes"
                  ? "bg-slate-800 text-cyan-300 border border-cyan-500/30"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              <span>Notes</span>
            </button>

            <button
              onClick={() => setActiveTab("ai")}
              className={`min-h-[44px] flex items-center gap-1.5 px-3 py-1.5 rounded-lg font-medium transition-all ${
                activeTab === "ai"
                  ? "bg-slate-800 text-cyan-300 border border-cyan-500/30"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              <Sparkles className="w-3.5 h-3.5 text-violet-400" />
              <span>AI Review</span>
            </button>

            <button
              onClick={() => setActiveTab("submissions")}
              className={`min-h-[44px] flex items-center gap-1.5 px-3 py-1.5 rounded-lg font-medium transition-all ${
                activeTab === "submissions"
                  ? "bg-slate-800 text-cyan-300 border border-cyan-500/30"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              <History className="w-3.5 h-3.5" />
              <span>Submissions</span>
            </button>
          </div>

          {/* Tab content area */}
          <div className="flex-1 overflow-y-auto p-5 text-sm">
            {activeTab === "statement" && (
              <div className="space-y-4">
                <div className="flex items-center justify-between text-xs text-slate-400 pb-2 border-b border-slate-800/80">
                  <span className="font-mono">{problem.topic}</span>
                  <div className="flex items-center gap-1">
                    {(problem.tags || []).map((t: string) => (
                      <span key={t} className="px-2 py-0.5 rounded bg-slate-800 text-[10px] text-slate-300">
                        {t}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Render Markdown Statement */}
                <div className="space-y-3 text-xs text-slate-300 leading-relaxed font-sans">
                  {(problem.statement_md || "").split("\n").map((line: string, lIdx: number) => {
                    const trimmed = line.trim();
                    if (!trimmed) return <div key={lIdx} className="h-2" />;
                    if (trimmed.startsWith("### ")) {
                      return (
                        <h3 key={lIdx} className="text-sm font-bold text-white pt-2">
                          {trimmed.slice(4)}
                        </h3>
                      );
                    }
                    if (trimmed.startsWith("## ")) {
                      return (
                        <h2 key={lIdx} className="text-base font-bold text-white pt-2">
                          {trimmed.slice(3)}
                        </h2>
                      );
                    }
                    if (trimmed.startsWith("- ")) {
                      return (
                        <li key={lIdx} className="ml-4 list-disc text-slate-300">
                          {trimmed.slice(2)}
                        </li>
                      );
                    }

                    const parts = line.split(/(\*\*.*?\*\*|`.*?`)/g);
                    return (
                      <p key={lIdx} className="min-h-[1.25rem] leading-relaxed">
                        {parts.map((part: string, pIdx: number) => {
                          if (part.startsWith("**") && part.endsWith("**") && part.length >= 4) {
                            return <strong key={pIdx} className="font-semibold text-white">{part.slice(2, -2)}</strong>;
                          }
                          if (part.startsWith("`") && part.endsWith("`") && part.length >= 2) {
                            return (
                              <code key={pIdx} className="px-1.5 py-0.5 rounded bg-slate-800 text-cyan-300 font-mono text-xs border border-slate-700/80">
                                {part.slice(1, -1)}
                              </code>
                            );
                          }
                          return part;
                        })}
                      </p>
                    );
                  })}
                </div>

                {/* Examples */}
                {problem.sample_tests && problem.sample_tests.length > 0 && (
                  <div className="pt-4 border-t border-slate-800/80 space-y-3">
                    <h3 className="text-xs uppercase font-mono font-bold tracking-wider text-slate-400">
                      Examples:
                    </h3>
                    {problem.sample_tests.map((test: any, idx: number) => (
                      <div key={idx} className="p-3.5 rounded-xl bg-[#121C2F] border border-slate-800 text-xs font-mono space-y-1.5 shadow-sm">
                        <div className="text-slate-400 font-semibold">Example {idx + 1}:</div>
                        <div className="text-slate-300"><span className="text-cyan-400 font-semibold">Input: </span>{test.input_text}</div>
                        <div className="text-slate-300"><span className="text-emerald-400 font-semibold">Output: </span>{test.expected_output}</div>
                      </div>
                    ))}
                  </div>
                )}

                {/* Constraints */}
                <div className="pt-4 border-t border-slate-800/80">
                  <h3 className="text-xs uppercase font-mono font-bold tracking-wider text-slate-400 mb-2">
                    Constraints:
                  </h3>
                  <ul className="list-disc pl-5 text-xs text-slate-400 space-y-1 font-mono">
                    <li>Time Limit: {problem.time_limit_ms || 1000} ms</li>
                    <li>Memory Limit: {problem.memory_limit_mb || 128} MB</li>
                    <li>Language support: Python 3, JavaScript, C++, Java</li>
                  </ul>
                </div>
              </div>
            )}

            {activeTab === "hints" && (
              <div className="space-y-4">
                <div className="p-3 rounded-xl bg-violet-500/10 border border-violet-500/20 text-xs text-violet-300 flex items-center gap-2">
                  <Sparkles className="w-4 h-4 shrink-0 text-violet-400" />
                  <span>Socratic hints guide your intuition without giving away the full code.</span>
                </div>

                {(problem.hints || []).map((h: any) => (
                  <div
                    key={h.level}
                    className="p-4 rounded-xl bg-[#121C2F] border border-slate-800 space-y-2"
                  >
                    <div className="flex items-center justify-between text-xs font-semibold">
                      <span className="text-cyan-400">Level {h.level} Hint</span>
                      <span className="text-slate-500 font-mono">-{h.xp_cost || h.level * 2} XP</span>
                    </div>
                    {unlockedHintLevel >= h.level ? (
                      <p className="text-xs text-slate-300 font-sans">{h.text}</p>
                    ) : (
                      <button
                        onClick={() => setUnlockedHintLevel(h.level)}
                        className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 font-medium transition-colors"
                      >
                        Unlock Hint ({h.xp_cost || h.level * 2} XP)
                      </button>
                    )}
                  </div>
                ))}
              </div>
            )}

            {activeTab === "editorial" && (
              <div className="space-y-4">
                {!editorialRevealed ? (
                  <div className="p-8 text-center bg-[#121C2F] rounded-2xl border border-slate-800 space-y-3">
                    <p className="text-slate-400 text-xs">
                      Editorial solution is gated until you solve the problem or choose to reveal it.
                    </p>
                    <button
                      onClick={() => setEditorialRevealed(true)}
                      className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs font-semibold text-slate-200 transition-colors"
                    >
                      Reveal Editorial Now
                    </button>
                  </div>
                ) : (
                  <div className="prose prose-invert max-w-none text-xs text-slate-300 whitespace-pre-line bg-[#121C2F] p-4 rounded-xl border border-slate-800">
                    {problem.editorial?.body_md ||
                      "### Optimal Approach\n\nApply the canonical pattern to minimize space and time complexity.\n\n- Time Complexity: O(n)\n- Space Complexity: O(1)"}
                  </div>
                )}
              </div>
            )}

            {activeTab === "notes" && (
              <div className="space-y-3 h-full flex flex-col">
                <div className="flex items-center justify-between text-xs text-slate-400">
                  <span>Markdown scratchpad</span>
                  <div className="flex items-center gap-1.5 font-mono text-[11px]">
                    {noteStatus === "saved" && (
                      <span className="text-emerald-400 flex items-center gap-1">
                        <CheckCircle2 className="w-3 h-3" /> Saved
                      </span>
                    )}
                    {noteStatus === "saving" && (
                      <span className="text-amber-400 flex items-center gap-1">
                        <Loader2 className="w-3 h-3 animate-spin" /> Saving...
                      </span>
                    )}
                    {noteStatus === "unsaved" && (
                      <span className="text-slate-400">&bull; Unsaved changes</span>
                    )}
                    {noteStatus === "sign-in" && (
                      <button
                        onClick={() => requireAuth(() => {})}
                        className="text-cyan-400 hover:underline flex items-center gap-1"
                      >
                        Sign in to save notes
                      </button>
                    )}
                    {noteStatus === "error" && (
                      <span className="text-red-400">Failed to save note</span>
                    )}
                  </div>
                </div>
                <textarea
                  value={noteContent}
                  onChange={(e) => handleNoteChange(e.target.value)}
                  placeholder="Record your pattern observations, edge cases, and learnings here (autosaved to server)..."
                  className="flex-1 w-full min-h-[300px] p-3 rounded-xl bg-[#0B1220] border border-slate-800 text-slate-200 text-xs font-mono focus:outline-none focus:border-cyan-400 transition-colors"
                />
              </div>
            )}

            {activeTab === "ai" && (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-bold text-white flex items-center gap-1.5">
                    <Sparkles className="w-4 h-4 text-violet-400" />
                    <span>AI Complexity & Code Review</span>
                  </h3>
                  <button
                    onClick={handleRequestAiReview}
                    className="px-3 py-1 rounded-lg bg-violet-600 hover:bg-violet-500 text-white text-xs font-semibold shadow"
                  >
                    Analyze Code
                  </button>
                </div>

                {aiReview ? (
                  <div className="space-y-3">
                    <div className="grid grid-cols-2 gap-3">
                      <div className="p-3 rounded-xl bg-[#121C2F] border border-slate-800">
                        <div className="text-[10px] text-slate-400 uppercase font-mono">Time Complexity</div>
                        <div className="text-base font-bold text-cyan-300">{aiReview.time_complexity}</div>
                      </div>
                      <div className="p-3 rounded-xl bg-[#121C2F] border border-slate-800">
                        <div className="text-[10px] text-slate-400 uppercase font-mono">Space Complexity</div>
                        <div className="text-base font-bold text-violet-300">{aiReview.space_complexity}</div>
                      </div>
                    </div>
                    <div className="p-3 rounded-xl bg-[#121C2F] border border-slate-800 text-xs space-y-1">
                      <div className="text-amber-400 font-semibold">Bottleneck Analysis:</div>
                      <p className="text-slate-300">{aiReview.slow_parts}</p>
                    </div>
                    <div className="p-3 rounded-xl bg-emerald-950/20 border border-emerald-500/30 text-xs space-y-1">
                      <div className="text-emerald-400 font-semibold">Optimization Suggestion:</div>
                      <p className="text-emerald-200">{aiReview.suggestion}</p>
                    </div>
                  </div>
                ) : (
                  <div className="p-6 text-center text-slate-500 bg-[#121C2F] rounded-xl border border-slate-800 text-xs">
                    Click "Analyze Code" to receive instant time & space complexity feedback.
                  </div>
                )}
              </div>
            )}

            {activeTab === "submissions" && (
              <div className="space-y-3">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                  Submission History
                </h3>
                {pastSubmissions.length === 0 ? (
                  <div className="p-6 text-center text-slate-500 bg-[#121C2F] rounded-xl border border-slate-800 text-xs">
                    No submissions recorded yet for this problem.
                  </div>
                ) : (
                  <div className="space-y-2">
                    {pastSubmissions.map((s: any) => (
                      <div
                        key={s.id}
                        className="p-3 rounded-xl bg-[#121C2F] border border-slate-800 flex items-center justify-between text-xs font-mono"
                      >
                        <div className="flex items-center gap-2">
                          <VerdictBadge verdict={s.verdict} size="sm" />
                          <span className="text-slate-400">{s.language}</span>
                        </div>
                        <div className="flex items-center gap-3 text-slate-400 text-[11px]">
                          <span>{s.runtime_ms} ms</span>
                          <span>{s.memory_kb} KB</span>
                          <span className="text-slate-500">{s.created_at?.split("T")[0]}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Right Pane: Monaco Code Editor & Execution Results (Rule 5 & Rule 6) */}
        <div
          className={`md:col-span-7 flex-col h-full bg-[#0B1220] overflow-hidden ${
            mobileView === "editor" ? "flex" : "hidden md:flex"
          }`}
        >
          {/* Code Editor */}
          <div className="flex-1 overflow-hidden p-3 pb-0 min-h-[300px]">
            <CodeEditor
              problemSlug={slug}
              language={language}
              onLanguageChange={setLanguage}
              code={code}
              onCodeChange={setCode}
              defaultStarterCodes={starterCodes}
            />
          </div>

          {/* Action Execution Footer Bar (Reachable without scrolling past statement) */}
          <div className="p-3 border-t border-slate-800 bg-[#121C2F] flex flex-wrap items-center justify-between gap-3 shrink-0">
            <div className="flex items-center gap-3">
              {submissionVerdict && (
                <div className="flex items-center gap-2">
                  <VerdictBadge verdict={submissionVerdict.verdict} size="sm" />
                  <span className="text-xs font-mono text-slate-400">
                    {submissionVerdict.runtime_ms} ms &bull; Beats{" "}
                    {submissionVerdict.runtime_percentile}%
                  </span>
                </div>
              )}
            </div>

            <div className="flex items-center gap-2.5">
              <button
                onClick={handleRun}
                disabled={isRunning || isSubmitting}
                className="min-h-[44px] px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-200 font-semibold text-xs flex items-center gap-1.5 transition-colors disabled:opacity-50"
                title="Run on sample test cases (Ctrl + Enter)"
              >
                <Play className="w-4 h-4 fill-slate-200" />
                <span>{isRunning ? "Running..." : "Run"}</span>
                <kbd className="hidden sm:inline-block px-1.5 py-0.5 rounded bg-slate-900 border border-slate-700 text-[10px] text-slate-400 font-mono ml-1">
                  Ctrl+Enter
                </kbd>
              </button>

              <button
                onClick={handleSubmit}
                disabled={isRunning || isSubmitting}
                className="min-h-[44px] px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-bold text-xs shadow-lg shadow-emerald-500/20 flex items-center gap-1.5 transition-all disabled:opacity-50"
                title="Submit solution against hidden tests (Ctrl + Shift + Enter)"
              >
                <Send className="w-4 h-4" />
                <span>{isSubmitting ? "Submitting..." : "Submit"}</span>
                <kbd className="hidden sm:inline-block px-1.5 py-0.5 rounded bg-emerald-950 border border-emerald-700/60 text-[10px] text-emerald-300 font-mono ml-1">
                  Ctrl+Shift+Enter
                </kbd>
              </button>
            </div>
          </div>

          {/* Test Case Output Drawer */}
          {testResults.length > 0 && (
            <div className="max-h-56 overflow-y-auto p-3 pt-0 bg-[#121C2F]">
              <TestCaseTable results={testResults} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
