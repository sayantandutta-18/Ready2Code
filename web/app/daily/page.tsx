"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import DifficultyChip from "../../components/ui/DifficultyChip";
import LoadingSkeleton from "../../components/ui/LoadingSkeleton";
import QueryErrorState from "../../components/ui/QueryErrorState";
import { fetchApi } from "../../lib/api";
import { Flame, Shield, Calendar, ArrowRight, CheckCircle2, Clock, Zap } from "lucide-react";

interface DailyData {
  date: string;
  problem: {
    id: string;
    slug: string;
    title: string;
    difficulty: "easy" | "medium" | "hard";
    topic: string;
  };
  streak: number;
  solved_today: boolean;
  freezes_left: number;
}

export default function DailyChallengePage() {
  const [freezeActive, setFreezeActive] = useState<boolean>(false);

  const {
    data: dailyData,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<DailyData>({
    queryKey: ["daily-problem"],
    queryFn: () => fetchApi<DailyData>("/daily"),
  });

  const handleUseFreeze = async () => {
    if ((dailyData?.freezes_left ?? 0) > 0 && !freezeActive) {
      try {
        await fetchApi("/daily/freeze", { method: "POST" });
        setFreezeActive(true);
        refetch();
        try {
          localStorage.setItem(`ready2code_freeze_${dailyData?.date}`, "active");
        } catch {}
      } catch (err) {
        setFreezeActive(true);
      }
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

      {isError && (
        <QueryErrorState
          title="Could not load daily challenge"
          message={error instanceof Error ? error.message : "Error contacting daily challenge service"}
          onRetry={() => refetch()}
        />
      )}

      {isLoading ? (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <LoadingSkeleton rows={2} className="h-40" />
            <LoadingSkeleton rows={2} className="h-40" />
            <LoadingSkeleton rows={2} className="h-40" />
          </div>
          <LoadingSkeleton rows={3} className="h-48" />
        </div>
      ) : dailyData ? (
        <>
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
                <div className="text-4xl font-black text-cyan-300">
                  {freezeActive ? Math.max(0, dailyData.freezes_left - 1) : dailyData.freezes_left}
                </div>
                <div className="text-xs text-slate-400 mt-1">Freezes in Vault</div>
              </div>
              <button
                type="button"
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
                  <span>Topic: {dailyData.problem?.topic}</span>
                </div>

                <h2 className="text-2xl font-bold text-white flex items-center gap-3">
                  <span>{dailyData.problem?.title}</span>
                  {dailyData.problem?.difficulty && (
                    <DifficultyChip difficulty={dailyData.problem.difficulty} />
                  )}
                </h2>

                <p className="text-sm text-slate-300 max-w-xl">
                  Apply algorithmic principles to formulate an optimal solution. Verify all edge cases
                  and benchmark your execution runtime percentiles.
                </p>
              </div>

              {dailyData.problem?.slug && (
                <Link
                  href={`/problems/${dailyData.problem.slug}`}
                  className="px-6 py-3.5 rounded-xl bg-gradient-to-r from-cyan-400 to-cyan-500 hover:from-cyan-300 hover:to-cyan-400 text-slate-950 font-bold text-sm shadow-xl shadow-cyan-500/25 flex items-center gap-2 transition-all shrink-0 self-start md:self-center"
                >
                  <span>Solve in Arena</span>
                  <ArrowRight className="w-4 h-4" />
                </Link>
              )}
            </div>
          </div>
        </>
      ) : null}
    </div>
  );
}
