"use client";

import React, { useMemo } from "react";
import { Flame, Calendar, Trophy, CheckCircle } from "lucide-react";

interface ActivityTowerProps {
  streak: number;
  longestStreak: number;
  solvedStats: {
    total: number;
    easy: number;
    medium: number;
    hard: number;
  };
}

export default function ActivityTower({
  streak,
  longestStreak,
  solvedStats,
}: ActivityTowerProps) {
  // Generate 52 weeks x 7 days grid
  const days = useMemo(() => {
    const list = [];
    const today = new Date();
    for (let i = 364; i >= 0; i--) {
      const d = new Date(today);
      d.setDate(d.getDate() - i);
      // Simulate plausible activity distributed over past year with higher recent activity
      const isRecent = i < 30;
      const seed = (d.getFullYear() * 1000 + d.getMonth() * 31 + d.getDate()) % 10;
      const count = isRecent && seed > 4 ? (seed % 4) + 1 : seed === 9 ? 2 : 0;
      list.push({
        date: d.toISOString().split("T")[0],
        count: count,
      });
    }
    return list;
  }, []);

  const getColor = (count: number) => {
    if (count === 0) return "bg-slate-900/80 border-slate-800";
    if (count === 1) return "bg-cyan-950 border-cyan-800 text-cyan-300";
    if (count === 2) return "bg-cyan-700 border-cyan-500 text-white";
    return "bg-cyan-400 border-cyan-200 text-slate-950 shadow-[0_0_8px_rgba(34,211,238,0.6)]";
  };

  return (
    <div className="bg-[#121C2F] rounded-2xl border border-slate-800 p-6 flex flex-col gap-6 shadow-xl">
      {/* Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-[#0B1220] border border-slate-800">
          <div className="flex items-center gap-2 text-slate-400 text-xs mb-1">
            <Flame className="w-4 h-4 text-amber-500" />
            <span>Current Streak</span>
          </div>
          <div className="text-2xl font-black text-amber-400">{streak} Days</div>
        </div>

        <div className="p-4 rounded-xl bg-[#0B1220] border border-slate-800">
          <div className="flex items-center gap-2 text-slate-400 text-xs mb-1">
            <Trophy className="w-4 h-4 text-violet-400" />
            <span>Longest Streak</span>
          </div>
          <div className="text-2xl font-black text-violet-300">{longestStreak} Days</div>
        </div>

        <div className="p-4 rounded-xl bg-[#0B1220] border border-slate-800">
          <div className="flex items-center gap-2 text-slate-400 text-xs mb-1">
            <CheckCircle className="w-4 h-4 text-emerald-400" />
            <span>Total Solved</span>
          </div>
          <div className="text-2xl font-black text-emerald-400">{solvedStats.total}</div>
        </div>

        <div className="p-4 rounded-xl bg-[#0B1220] border border-slate-800 flex items-center justify-around">
          <div className="text-center">
            <div className="text-[11px] text-emerald-400 font-semibold">Easy</div>
            <div className="text-lg font-bold text-slate-200">{solvedStats.easy}</div>
          </div>
          <div className="text-center">
            <div className="text-[11px] text-amber-400 font-semibold">Medium</div>
            <div className="text-lg font-bold text-slate-200">{solvedStats.medium}</div>
          </div>
          <div className="text-center">
            <div className="text-[11px] text-rose-400 font-semibold">Hard</div>
            <div className="text-lg font-bold text-slate-200">{solvedStats.hard}</div>
          </div>
        </div>
      </div>

      {/* Heatmap Grid */}
      <div>
        <div className="flex items-center justify-between text-xs text-slate-400 mb-3">
          <span className="flex items-center gap-1.5 font-semibold text-slate-300">
            <Calendar className="w-4 h-4 text-cyan-400" /> 365-Day Activity Tower
          </span>
          <div className="flex items-center gap-1.5 text-[11px]">
            <span>Less</span>
            <span className="w-2.5 h-2.5 rounded-sm bg-slate-900 border border-slate-800 inline-block" />
            <span className="w-2.5 h-2.5 rounded-sm bg-cyan-950 border border-cyan-800 inline-block" />
            <span className="w-2.5 h-2.5 rounded-sm bg-cyan-700 border border-cyan-500 inline-block" />
            <span className="w-2.5 h-2.5 rounded-sm bg-cyan-400 inline-block" />
            <span>More</span>
          </div>
        </div>

        <div className="overflow-x-auto pb-2">
          <div className="grid grid-rows-7 grid-flow-col gap-1 w-max">
            {days.map((d, idx) => (
              <div
                key={idx}
                title={`${d.date}: ${d.count} solutions`}
                className={`w-3.5 h-3.5 rounded-sm border transition-transform hover:scale-125 cursor-pointer ${getColor(
                  d.count
                )}`}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
