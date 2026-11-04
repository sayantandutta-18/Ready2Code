"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import DifficultyChip from "../../../components/ui/DifficultyChip";
import {
  Trophy,
  Clock,
  ArrowLeft,
  ChevronRight,
  Send,
  CheckCircle2,
  AlertCircle,
  TrendingUp,
} from "lucide-react";

export default function ContestArenaPage({ params }: { params: { id: string } }) {
  const { id } = params;

  const [contest, setContest] = useState<any>({
    id: id,
    title: "Ready2Code Weekly Contest 101",
    starts_at: new Date(Date.now() - 3600000).toISOString(),
    duration_min: 90,
    status: "live",
    problems: [
      { id: "1", slug: "two-sum", title: "Two Sum", difficulty: "easy", points: 100, position: 1 },
      { id: "6", slug: "maximum-subarray", title: "Maximum Subarray", difficulty: "medium", points: 200, position: 2 },
      { id: "8", slug: "number-of-islands", title: "Number of Islands", difficulty: "medium", points: 300, position: 3 },
    ],
  });

  const [standings, setStandings] = useState<any[]>([
    { rank: 1, username: "algo_ninja", score: 300, penalty_min: 3.0 },
    { rank: 2, username: "byte_master", score: 100, penalty_min: 5.0 },
    { rank: 3, username: "coder_alex", score: 100, penalty_min: 12.4 },
  ]);

  const [activeTab, setActiveTab] = useState<"problems" | "standings">("problems");
  const [timeLeft, setTimeLeft] = useState<string>("34:12");

  // Fetch contest details & 10s polling for live standings (C2.2 specification)
  useEffect(() => {
    const fetchContest = () => {
      fetch(`/api/contests/${id}`)
        .then((res) => (res.ok ? res.json() : null))
        .then((data) => {
          if (data && data.problems) setContest(data);
        })
        .catch(() => {});
    };

    const fetchStandings = () => {
      fetch(`/api/contests/${id}/standings`)
        .then((res) => (res.ok ? res.json() : null))
        .then((data) => {
          if (Array.isArray(data) && data.length > 0) setStandings(data);
        })
        .catch(() => {});
    };

    fetchContest();
    fetchStandings();

    // Poll every 10 seconds for live standings (C2.2 requirement)
    const interval = setInterval(fetchStandings, 10000);
    return () => clearInterval(interval);
  }, [id]);

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
            <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-rose-500/15 border border-rose-500/30 text-rose-400 animate-pulse">
              LIVE ARENA
            </span>
            <span className="text-xs text-slate-400 font-mono">90 Mins &bull; Penalty 5 mins/WA</span>
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
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {contest.problems.map((p: any) => (
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
        </div>
      )}
    </div>
  );
}
