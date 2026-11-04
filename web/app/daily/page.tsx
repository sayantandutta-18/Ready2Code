"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import DifficultyChip from "../../components/ui/DifficultyChip";
import { Flame, Shield, Calendar, ArrowRight, CheckCircle2, Clock, Zap } from "lucide-react";

export default function DailyChallengePage() {
  const [dailyData, setDailyData] = useState<any>({
    date: new Date().toISOString().split("T")[0],
    problem: {
      id: "1",
      slug: "two-sum",
      title: "Two Sum",
      difficulty: "easy",
      topic: "Arrays",
    },
    streak: 3,
    solved_today: false,
    freezes_left: 2,
  });

  const [freezeActive, setFreezeActive] = useState<boolean>(false);

  useEffect(() => {
    fetch("/api/daily")
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (data) setDailyData(data);
      })
      .catch(() => {});
  }, []);

  const handleUseFreeze = () => {
    if (dailyData.freezes_left > 0 && !freezeActive) {
      setFreezeActive(true);
      setDailyData((prev: any) => ({
        ...prev,
        freezes_left: prev.freezes_left - 1,
      }));
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 lg:px-8 py-12 space-y-8">
      {/* Title */}
      <div className="text-center max-w-xl mx-auto space-y-2">
        <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-semibold">
          <Flame className="w-4 h-4 fill-amber-500" />
          <span>Daily Ritual &bull; Keeps your cognitive engine sharp</span>
        </div>
        <h1 className="text-3xl font-black text-white tracking-tight">Today's DSA Challenge</h1>
        <p className="text-sm text-slate-400">
          Solve each daily challenge to maintain your streak, earn bonus XP, and reinforce patterns.
        </p>
      </div>

      {/* Streak Dashboard Card */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Streak Counter */}
        <div className="p-6 rounded-2xl bg-gradient-to-br from-[#121C2F] to-[#1A2740] border border-amber-500/30 flex flex-col justify-between shadow-xl">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Consecutive Active Days</span>
            <Flame className="w-5 h-5 text-amber-500 fill-amber-500" />
          </div>
          <div className="my-4">
            <div className="text-4xl font-black text-amber-400">{dailyData.streak}</div>
            <div className="text-xs text-slate-400 mt-1">Days on Fire 🔥</div>
          </div>
          <div className="text-[11px] text-slate-500">
            {dailyData.solved_today ? "Completed for today!" : "Solve today's challenge to extend"}
          </div>
        </div>

        {/* Streak Freeze Armor */}
        <div className="p-6 rounded-2xl bg-[#121C2F] border border-cyan-500/30 flex flex-col justify-between shadow-xl">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Streak Freezes</span>
            <Shield className="w-5 h-5 text-cyan-400" />
          </div>
          <div className="my-4">
            <div className="text-4xl font-black text-cyan-300">{dailyData.freezes_left}</div>
            <div className="text-xs text-slate-400 mt-1">Freezes in Vault</div>
          </div>
          <button
            onClick={handleUseFreeze}
            disabled={freezeActive || dailyData.freezes_left === 0}
            className="w-full py-1.5 rounded-lg bg-cyan-500/20 hover:bg-cyan-500/30 border border-cyan-500/40 text-cyan-300 text-xs font-semibold disabled:opacity-40 transition-colors"
          >
            {freezeActive ? "Shield Activated" : "Equip Freeze"}
          </button>
        </div>

        {/* Bonus XP */}
        <div className="p-6 rounded-2xl bg-[#121C2F] border border-violet-500/30 flex flex-col justify-between shadow-xl">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Daily Reward</span>
            <Zap className="w-5 h-5 text-violet-400 fill-violet-400" />
          </div>
          <div className="my-4">
            <div className="text-4xl font-black text-violet-300">+15 XP</div>
            <div className="text-xs text-slate-400 mt-1">Base + Streak Multiplier</div>
          </div>
          <div className="text-[11px] text-slate-500">Credited on first accepted run</div>
        </div>
      </div>

      {/* Today's Problem Main Card */}
      <div className="p-8 rounded-3xl bg-[#121C2F] border border-slate-800 shadow-2xl relative overflow-hidden">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-3">
            <div className="flex items-center gap-2 text-xs font-semibold text-slate-400">
              <Calendar className="w-4 h-4 text-cyan-400" />
              <span>{dailyData.date}</span>
              <span className="text-slate-600">&bull;</span>
              <span>Topic: {dailyData.problem.topic}</span>
            </div>

            <h2 className="text-2xl font-bold text-white flex items-center gap-3">
              <span>{dailyData.problem.title}</span>
              <DifficultyChip difficulty={dailyData.problem.difficulty} />
            </h2>

            <p className="text-sm text-slate-300 max-w-xl">
              Apply algorithmic principles to formulate an optimal solution. Verify all edge cases
              and benchmark your execution runtime percentiles.
            </p>
          </div>

          <Link
            href={`/problems/${dailyData.problem.slug}`}
            className="px-6 py-3.5 rounded-xl bg-gradient-to-r from-cyan-400 to-cyan-500 hover:from-cyan-300 hover:to-cyan-400 text-slate-950 font-bold text-sm shadow-xl shadow-cyan-500/25 flex items-center gap-2 transition-all shrink-0 self-start md:self-center"
          >
            <span>Solve in Arena</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>
    </div>
  );
}
