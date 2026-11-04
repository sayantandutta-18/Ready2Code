"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { Trophy, Zap, Flame, Award, ArrowUpRight } from "lucide-react";
import { fetchApi } from "../../lib/api";
import LoadingSkeleton from "../../components/ui/LoadingSkeleton";
import EmptyState from "../../components/ui/EmptyState";
import QueryErrorState from "../../components/ui/QueryErrorState";

interface LeaderboardUser {
  rank: number;
  username: string;
  display_name?: string;
  xp: number;
  solved: number;
  streak: number;
  rating: number;
}

export default function LeaderboardPage() {
  const [filter, setFilter] = useState<"all" | "weekly">("all");

  const {
    data: leaderboard = [],
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<LeaderboardUser[]>({
    queryKey: ["leaderboard", filter],
    queryFn: () => fetchApi<LeaderboardUser[]>(`/leaderboard?filter=${filter}`),
  });

  const top3 = leaderboard.slice(0, 3);
  const remaining = leaderboard.slice(3);

  return (
    <div className="max-w-5xl mx-auto px-4 lg:px-8 py-10 space-y-8">
      {/* Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-black text-white tracking-tight flex items-center gap-3">
            <Trophy className="w-8 h-8 text-amber-400" />
            <span>Global Leaderboard</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Top ranked engineers by total XP, streak consistency, and Elo contest rating.
          </p>
        </div>

        <div className="flex items-center gap-1 bg-[#121C2F] p-1 rounded-xl border border-slate-800 text-xs self-start sm:self-auto">
          <button
            onClick={() => setFilter("all")}
            className={`px-3 py-1.5 rounded-lg font-medium transition-all ${
              filter === "all"
                ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/30"
                : "text-slate-400 hover:text-white"
            }`}
          >
            All-Time XP
          </button>
          <button
            onClick={() => setFilter("weekly")}
            className={`px-3 py-1.5 rounded-lg font-medium transition-all ${
              filter === "weekly"
                ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/30"
                : "text-slate-400 hover:text-white"
            }`}
          >
            This Week
          </button>
        </div>
      </div>

      {isError && (
        <QueryErrorState
          title="Could not load leaderboard"
          message={error instanceof Error ? error.message : "Unable to load leaderboard data from backend."}
          onRetry={() => refetch()}
        />
      )}

      {isLoading ? (
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <LoadingSkeleton rows={2} className="h-44" />
            <LoadingSkeleton rows={2} className="h-44" />
            <LoadingSkeleton rows={2} className="h-44" />
          </div>
          <LoadingSkeleton rows={6} />
        </div>
      ) : leaderboard.length === 0 ? (
        <EmptyState
          title="No ranked competitors yet"
          description="Be the first to solve algorithmic challenges and claim the top podium spot on the global leaderboard!"
        />
      ) : (
        <>
          {/* Top 3 Podium Cards */}
          {top3.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {top3.map((user, idx) => (
                <div
                  key={user.username}
                  className={`p-6 rounded-2xl border flex flex-col justify-between shadow-xl relative overflow-hidden ${
                    idx === 0
                      ? "bg-gradient-to-br from-amber-500/15 via-[#162033] to-[#121C2F] border-amber-500/40 md:-translate-y-2"
                      : idx === 1
                      ? "bg-gradient-to-br from-slate-400/10 via-[#162033] to-[#121C2F] border-slate-400/30"
                      : "bg-gradient-to-br from-amber-700/15 via-[#162033] to-[#121C2F] border-amber-700/30"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-2xl">{idx === 0 ? "🥇" : idx === 1 ? "🥈" : "🥉"}</span>
                    <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                      Rank #{user.rank}
                    </span>
                  </div>

                  <div className="my-4 space-y-1">
                    <Link
                      href={`/profile/${user.username}`}
                      className="font-black text-lg text-white hover:text-cyan-300 transition-colors flex items-center gap-1.5"
                    >
                      <span>{user.display_name || user.username}</span>
                      <ArrowUpRight className="w-4 h-4 opacity-70" />
                    </Link>
                    <div className="text-xs text-slate-400 font-mono">@{user.username}</div>
                  </div>

                  <div className="grid grid-cols-3 gap-2 pt-3 border-t border-slate-800 text-center">
                    <div>
                      <div className="text-[10px] text-slate-500 uppercase font-mono">XP</div>
                      <div className="font-mono font-bold text-sm text-cyan-400">{user.xp}</div>
                    </div>
                    <div>
                      <div className="text-[10px] text-slate-500 uppercase font-mono">Solved</div>
                      <div className="font-mono font-bold text-sm text-white">{user.solved}</div>
                    </div>
                    <div>
                      <div className="text-[10px] text-slate-500 uppercase font-mono">Rating</div>
                      <div className="font-mono font-bold text-sm text-amber-400">{user.rating}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Remaining Ranks Table */}
          {remaining.length > 0 && (
            <div className="bg-[#121C2F] rounded-2xl border border-slate-800 overflow-hidden shadow-2xl">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-slate-800 text-[11px] uppercase tracking-wider text-slate-400 bg-[#0E1726]/60 font-semibold">
                    <th className="py-3 px-4 w-16 text-center">Rank</th>
                    <th className="py-3 px-4">Engineer</th>
                    <th className="py-3 px-4 w-28 text-right">XP</th>
                    <th className="py-3 px-4 w-24 text-right">Solved</th>
                    <th className="py-3 px-4 w-24 text-right">Streak</th>
                    <th className="py-3 px-4 w-28 text-right">Elo Rating</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 text-sm">
                  {remaining.map((u) => (
                    <tr key={u.username} className="hover:bg-slate-800/30 transition-colors">
                      <td className="py-3 px-4 text-center font-mono text-slate-400 font-semibold">
                        #{u.rank}
                      </td>
                      <td className="py-3 px-4 font-semibold text-slate-200">
                        <Link
                          href={`/profile/${u.username}`}
                          className="hover:text-cyan-300 transition-colors flex items-center gap-2"
                        >
                          <span>{u.display_name || u.username}</span>
                          <span className="text-xs text-slate-500 font-mono">(@{u.username})</span>
                        </Link>
                      </td>
                      <td className="py-3 px-4 text-right font-mono text-cyan-400 font-semibold">
                        {u.xp}
                      </td>
                      <td className="py-3 px-4 text-right font-mono text-slate-300">{u.solved}</td>
                      <td className="py-3 px-4 text-right font-mono text-amber-400 font-semibold">
                        {u.streak}d
                      </td>
                      <td className="py-3 px-4 text-right font-mono text-white font-bold">{u.rating}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </div>
  );
}
