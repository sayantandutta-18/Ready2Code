"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { fetchApi } from "@/lib/api";
import LoadingSkeleton from "@/components/ui/LoadingSkeleton";
import QueryErrorState from "@/components/ui/QueryErrorState";
import EmptyState from "@/components/ui/EmptyState";
import DifficultyChip from "../../../components/ui/DifficultyChip";
import {
  Trophy,
  Clock,
  ArrowLeft,
  ChevronRight,
  CheckCircle2,
  AlertCircle,
  TrendingUp,
} from "lucide-react";

interface ContestProblem {
  id: string;
  slug: string;
  title: string;
  difficulty: "easy" | "medium" | "hard";
  points: number;
  position: number;
}

interface ContestDetail {
  id: string;
  title: string;
  starts_at: string;
  duration_min: number;
  type: string;
  status: string;
  problems: ContestProblem[];
}

interface StandingEntry {
  rank: number;
  user_id: string;
  username: string;
  score: number;
  penalty_min: number;
  finished_at?: string | null;
}

export default function ContestArenaPage({ params }: { params: { id: string } }) {
  const { id } = params;
  const [activeTab, setActiveTab] = useState<"problems" | "standings">("problems");
  const [timeLeft, setTimeLeft] = useState<string>("90:00");

  const {
    data: contest,
    isLoading: contestLoading,
    isError: contestError,
    error: contestErrObj,
    refetch: refetchContest,
  } = useQuery<ContestDetail>({
    queryKey: ["contest", id],
    queryFn: () => fetchApi<ContestDetail>(`/contests/${id}`),
  });

  const {
    data: standings = [],
    isLoading: standingsLoading,
  } = useQuery<StandingEntry[]>({
    queryKey: ["contest-standings", id],
    queryFn: () => fetchApi<StandingEntry[]>(`/contests/${id}/standings`),
    refetchInterval: 10000, // Live poll every 10 seconds (C2.2 requirement)
  });

  // Calculate real countdown based on contest start time and duration
  useEffect(() => {
    if (!contest?.starts_at || !contest?.duration_min) return;

    const updateTimer = () => {
      const startTime = new Date(contest.starts_at).getTime();
      const endTime = startTime + contest.duration_min * 60 * 1000;
      const now = Date.now();
      const diffMs = endTime - now;

      if (diffMs <= 0) {
        setTimeLeft("Finished");
      } else {
        const totalSecs = Math.floor(diffMs / 1000);
        const mins = Math.floor(totalSecs / 60);
        const secs = totalSecs % 60;
        setTimeLeft(`${mins}:${secs < 10 ? "0" : ""}${secs}`);
      }
    };

    updateTimer();
    const interval = setInterval(updateTimer, 1000);
    return () => clearInterval(interval);
  }, [contest?.starts_at, contest?.duration_min]);

  if (contestLoading) {
    return (
      <div className="max-w-6xl mx-auto px-4 lg:px-8 py-10 space-y-6">
        <LoadingSkeleton variant="title" className="w-48 h-6" />
        <LoadingSkeleton variant="card" className="h-44" />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <LoadingSkeleton variant="card" className="h-40" />
          <LoadingSkeleton variant="card" className="h-40" />
          <LoadingSkeleton variant="card" className="h-40" />
        </div>
      </div>
    );
  }

  if (contestError || !contest) {
    return (
      <div className="max-w-6xl mx-auto px-4 lg:px-8 py-10">
        <QueryErrorState
          title="Failed to load contest arena"
          message={contestErrObj instanceof Error ? contestErrObj.message : "The requested contest arena could not be retrieved."}
          onRetry={() => refetchContest()}
        />
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 lg:px-8 py-10 space-y-8">
      {/* Back button */}
      <Link href="/contests" className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-cyan-400 font-mono">
        <ArrowLeft className="w-3.5 h-3.5" /> Back to Contests
      </Link>

      {/* Live Contest Header */}
      <div className="p-8 rounded-3xl bg-[#121C2F] border border-slate-800 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-6">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className={`px-2.5 py-0.5 rounded-full text-[11px] font-bold border ${
              contest.status === "live"
                ? "bg-rose-500/15 border-rose-500/30 text-rose-400 animate-pulse"
                : "bg-cyan-500/15 border-cyan-500/30 text-cyan-400"
            }`}>
              {contest.status === "live" ? "LIVE ARENA" : contest.status.toUpperCase()}
            </span>
            <span className="text-xs text-slate-400 font-mono">{contest.duration_min} Mins &bull; Penalty 5 mins/WA</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-white">{contest.title}</h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-xl">
            Accepted solutions score points. Wrong answers apply a 5-minute penalty to your tiebreak.
          </p>
        </div>

        <div className="p-4 rounded-2xl bg-[#0B1220] border border-slate-800 text-center sm:self-center">
          <div className="text-xs text-slate-400 mb-1 flex items-center justify-center gap-1">
            <Clock className="w-3.5 h-3.5 text-amber-400" /> Time Remaining
          </div>
          <div className="text-3xl font-black text-amber-400 font-mono">{timeLeft}</div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-3 text-sm">
        <button
          onClick={() => setActiveTab("problems")}
          className={`px-4 py-2 rounded-xl font-semibold transition-all ${
            activeTab === "problems"
              ? "bg-cyan-500/15 text-cyan-300 border border-cyan-500/30 shadow-sm shadow-cyan-500/20"
              : "text-slate-400 hover:text-white"
          }`}
        >
          Contest Problems ({contest.problems.length})
        </button>
        <button
          onClick={() => setActiveTab("standings")}
          className={`px-4 py-2 rounded-xl font-semibold transition-all ${
            activeTab === "standings"
              ? "bg-cyan-500/15 text-cyan-300 border border-cyan-500/30 shadow-sm shadow-cyan-500/20"
              : "text-slate-400 hover:text-white"
          }`}
        >
          Live Standings (Auto-refresh 10s)
        </button>
      </div>

      {/* Tab: Problems */}
      {activeTab === "problems" && (
        contest.problems.length === 0 ? (
          <EmptyState
            title="No problems registered"
            description="Problems for this contest have not been published yet."
          />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {contest.problems.map((p) => (
              <div
                key={p.slug}
                className="p-6 rounded-2xl bg-[#121C2F] border border-slate-800 flex flex-col justify-between space-y-4 hover:border-cyan-500/40 transition-all shadow-xl"
              >
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-mono text-cyan-400 uppercase font-bold">
                      Problem {p.position}
                    </span>
                    <span className="px-2 py-0.5 rounded bg-violet-950/60 border border-violet-500/30 text-violet-300 font-mono text-xs font-bold">
                      {p.points} Pts
                    </span>
                  </div>
                  <h3 className="text-lg font-bold text-white">{p.title}</h3>
                  <DifficultyChip difficulty={p.difficulty} />
                </div>

                <Link
                  href={`/problems/${p.slug}`}
                  className="w-full py-2.5 rounded-xl bg-cyan-400 hover:bg-cyan-300 text-slate-950 font-bold text-xs text-center flex items-center justify-center gap-1.5 shadow transition-colors"
                >
                  <span>Enter & Solve</span>
                  <ChevronRight className="w-4 h-4" />
                </Link>
              </div>
            ))}
          </div>
        )
      )}

      {/* Tab: Standings Table (10s live polling) */}
      {activeTab === "standings" && (
        <div className="bg-[#121C2F] rounded-2xl border border-slate-800 overflow-hidden shadow-2xl">
          <div className="p-4 bg-[#0E1726]/80 border-b border-slate-800 flex items-center justify-between text-xs text-slate-400">
            <span className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span>Polling live every 10 seconds</span>
            </span>
            <span className="font-mono">{standings.length} Active Competitors</span>
          </div>

          {standingsLoading && standings.length === 0 ? (
            <div className="p-6">
              <LoadingSkeleton variant="table" rows={4} />
            </div>
          ) : standings.length === 0 ? (
            <div className="p-8 text-center text-sm text-slate-400 font-mono">
              No contest submissions recorded yet. Be the first to submit a solution!
            </div>
          ) : (
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-800 text-[11px] uppercase tracking-wider text-slate-400 bg-[#0B1220]/60 font-semibold">
                  <th className="py-3 px-4 w-16 text-center">Rank</th>
                  <th className="py-3 px-4">Contestant</th>
                  <th className="py-3 px-4 w-32 text-center">Score</th>
                  <th className="py-3 px-4 w-36 text-right">Penalty Time</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-sm font-mono">
                {standings.map((s, idx) => (
                  <tr key={idx} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-3 px-4 text-center">
                      <span
                        className={`inline-flex items-center justify-center w-6 h-6 rounded-full text-xs font-bold ${
                          s.rank === 1
                            ? "bg-amber-400 text-slate-950"
                            : s.rank === 2
                            ? "bg-slate-300 text-slate-950"
                            : s.rank === 3
                            ? "bg-amber-700 text-white"
                            : "text-slate-400"
                        }`}
                      >
                        {s.rank}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-sans font-semibold text-slate-200">
                      {s.username}
                    </td>
                    <td className="py-3 px-4 text-center font-bold text-cyan-300">
                      {s.score}
                    </td>
                    <td className="py-3 px-4 text-right text-xs text-slate-400">
                      {s.penalty_min} mins
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
}
