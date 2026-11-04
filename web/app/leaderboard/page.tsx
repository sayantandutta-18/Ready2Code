"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { Trophy, Zap, Flame, Award, ArrowUpRight } from "lucide-react";

export default function LeaderboardPage() {
  const [filter, setFilter] = useState<"all" | "weekly">("all");
  const [leaderboard, setLeaderboard] = useState<any[]>([
    { rank: 1, username: "algo_ninja", display_name: "Ninja Coder", xp: 1450, solved: 12, streak: 14, rating: 1820 },
    { rank: 2, username: "byte_master", display_name: "Byte Master", xp: 1120, solved: 9, streak: 8, rating: 1750 },
    { rank: 3, username: "coder_alex", display_name: "Alex Vance", xp: 185, solved: 7, streak: 3, rating: 1540 },
    { rank: 4, username: "dev_siddharth", display_name: "Siddharth R", xp: 160, solved: 5, streak: 2, rating: 1510 },
  ]);

  useEffect(() => {
    fetch("/api/leaderboard")
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) setLeaderboard(data);
      })
      .catch(() => {});
  }, []);

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

      {/* Top 3 Podium */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4">
        {leaderboard.slice(0, 3).map((user, idx) => {
          const podiumBg = [
            "border-amber-400/50 bg-gradient-to-b from-amber-500/10 to-[#121C2F]",
            "border-slate-300/40 bg-gradient-to-b from-slate-300/10 to-[#121C2F]",
            "border-amber-700/40 bg-gradient-to-b from-amber-700/10 to-[#121C2F]",
          ][idx];

          const medalIcon = ["🥇", "🥈", "🥉"][idx];

          return (
            <div
              key={user.username}
              className={`p-6 rounded-3xl border ${podiumBg} flex flex-col items-center text-center space-y-3 shadow-2xl relative`}
            >
              <div className="text-3xl">{medalIcon}</div>
              <div>
                <h3 className="text-lg font-bold text-white">{user.display_name}</h3>
                <Link
                  href={`/profile/${user.username}`}
                  className="text-xs text-cyan-400 hover:underline font-mono"
                >
                  @{user.username}
                </Link>
              </div>

              <div className="w-full pt-3 border-t border-slate-800/80 flex items-center justify-around text-xs">
                <div>
                  <div className="text-slate-500 text-[10px] uppercase font-mono">Rating</div>
                  <div className="font-bold text-slate-200">{user.rating}</div>
                </div>
                <div>
                  <div className="text-slate-500 text-[10px] uppercase font-mono">Solved</div>
                  <div className="font-bold text-emerald-400">{user.solved}</div>
                </div>
                <div>
                  <div className="text-slate-500 text-[10px] uppercase font-mono">XP</div>
                  <div className="font-bold text-violet-400">{user.xp}</div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Full Leaderboard Table */}
      <div className="bg-[#121C2F] rounded-2xl border border-slate-800 overflow-hidden shadow-2xl">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-slate-800 text-[11px] uppercase tracking-wider text-slate-400 bg-[#0B1220]/60 font-semibold">
              <th className="py-3 px-4 w-16 text-center">Rank</th>
              <th className="py-3 px-4">User</th>
              <th className="py-3 px-4 w-28 text-center">Streak</th>
              <th className="py-3 px-4 w-28 text-center">Solved</th>
              <th className="py-3 px-4 w-32 text-center">Elo Rating</th>
              <th className="py-3 px-4 w-32 text-right">Total XP</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-sm">
            {leaderboard.map((u, i) => (
              <tr key={u.username} className="hover:bg-slate-800/40 transition-colors">
                <td className="py-3.5 px-4 text-center font-mono font-bold text-slate-400">
                  #{i + 1}
                </td>
                <td className="py-3.5 px-4">
                  <Link
                    href={`/profile/${u.username}`}
                    className="font-semibold text-slate-200 hover:text-cyan-300 flex items-center gap-1.5 transition-colors"
                  >
                    <span>{u.display_name}</span>
                    <span className="text-xs text-slate-500 font-mono">(@{u.username})</span>
                  </Link>
                </td>
                <td className="py-3.5 px-4 text-center">
                  <span className="inline-flex items-center gap-1 text-amber-400 text-xs font-semibold">
                    <Flame className="w-3.5 h-3.5 fill-amber-500" />
                    <span>{u.streak}d</span>
                  </span>
                </td>
                <td className="py-3.5 px-4 text-center font-mono text-emerald-400 font-semibold">
                  {u.solved}
                </td>
                <td className="py-3.5 px-4 text-center font-mono text-slate-300">
                  {u.rating}
                </td>
                <td className="py-3.5 px-4 text-right font-mono font-bold text-violet-400">
                  {u.xp} XP
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
