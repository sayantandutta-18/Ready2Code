"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { fetchApi } from "@/lib/api";
import LoadingSkeleton from "@/components/ui/LoadingSkeleton";
import QueryErrorState from "@/components/ui/QueryErrorState";
import DifficultyChip from "../../../components/ui/DifficultyChip";
import { Calendar, CheckCircle2, Lock, ArrowLeft, ArrowRight, Sparkles } from "lucide-react";

interface PlanDayProblem {
  id: string;
  slug: string;
  title: string;
  difficulty: "easy" | "medium" | "hard";
  topic: string;
  solved: boolean;
}

interface PlanDay {
  day_number: number;
  problems: PlanDayProblem[];
  unlocked: boolean;
  completed: boolean;
}

interface PlanDetail {
  id: string;
  name: string;
  description: string;
  duration_days: number;
  current_day: number;
  days: PlanDay[];
}

export default function PlanDetailPage({ params }: { params: { id: string } }) {
  const { id } = params;
  const [activeDay, setActiveDay] = useState(1);

  const {
    data: planData,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<PlanDetail>({
    queryKey: ["plan", id, activeDay],
    queryFn: () => fetchApi<PlanDetail>(`/plans/${id}?current_day=${activeDay}`),
  });

  if (isLoading) {
    return (
      <div className="max-w-6xl mx-auto px-4 lg:px-8 py-10 space-y-6">
        <LoadingSkeleton variant="title" className="w-56 h-6" />
        <LoadingSkeleton variant="card" className="h-44" />
        <LoadingSkeleton variant="card" className="h-64" />
      </div>
    );
  }

  if (isError || !planData) {
    return (
      <div className="max-w-6xl mx-auto px-4 lg:px-8 py-10">
        <QueryErrorState
          title="Failed to load study plan"
          message={error instanceof Error ? error.message : "The requested plan could not be retrieved."}
          onRetry={() => refetch()}
        />
      </div>
    );
  }

  const currentDayData =
    planData.days.find((d) => d.day_number === activeDay) || planData.days[0];

  const handleMarkDayComplete = () => {
    setActiveDay((prev) => Math.min(planData.duration_days, prev + 1));
  };

  return (
    <div className="max-w-6xl mx-auto px-4 lg:px-8 py-10 space-y-8">
      {/* Back button */}
      <Link href="/lists" className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-cyan-400 font-mono">
        <ArrowLeft className="w-3.5 h-3.5" /> Back to Lists & Plans
      </Link>

      {/* Plan Header */}
      <div className="p-8 rounded-3xl bg-[#121C2F] border border-slate-800 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-6">
        <div>
          <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-amber-400 px-2 py-0.5 rounded bg-amber-950/60 border border-amber-500/30">
            {planData.duration_days}-Day Calendar Bootcamp
          </span>
          <h1 className="text-2xl sm:text-3xl font-black text-white mt-2">{planData.name}</h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-xl">
            {planData.description || "Complete daily assigned problems to progress systematically. Each completed day unlocks the subsequent session."}
          </p>
        </div>

        <div className="p-4 rounded-2xl bg-[#0B1220] border border-slate-800 text-center sm:self-center">
          <div className="text-xs text-slate-400 mb-1">Current Milestone</div>
          <div className="text-2xl font-black text-amber-400">Day {activeDay}</div>
          <div className="text-[11px] text-slate-500">of {planData.duration_days} Days</div>
        </div>
      </div>

      {/* 30-Day Calendar Grid */}
      <div className="bg-[#121C2F] rounded-2xl border border-slate-800 p-6 space-y-4 shadow-xl">
        <h2 className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
          <Calendar className="w-4 h-4 text-cyan-400" />
          <span>Interactive Calendar Grid</span>
        </h2>

        <div className="grid grid-cols-5 sm:grid-cols-6 md:grid-cols-10 gap-2.5">
          {planData.days.map((d) => {
            const isSelected = d.day_number === activeDay;
            return (
              <button
                key={d.day_number}
                disabled={!d.unlocked}
                onClick={() => setActiveDay(d.day_number)}
                className={`h-14 rounded-xl border flex flex-col items-center justify-center transition-all ${
                  isSelected
                    ? "bg-cyan-500 text-slate-950 ring-2 ring-cyan-300 font-bold scale-105 shadow-lg shadow-cyan-500/25"
                    : d.completed
                    ? "bg-emerald-950/40 border-emerald-500/40 text-emerald-300"
                    : d.unlocked
                    ? "bg-[#0B1220] border-slate-700/80 text-slate-200 hover:border-cyan-400"
                    : "bg-[#0B1220]/40 border-slate-850 text-slate-600 opacity-40 cursor-not-allowed"
                }`}
              >
                <div className="text-xs font-mono">Day {d.day_number}</div>
                <div className="text-[10px] mt-0.5">
                  {d.completed ? (
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                  ) : !d.unlocked ? (
                    <Lock className="w-3 h-3 text-slate-600" />
                  ) : (
                    "Active"
                  )}
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Active Day Checklist */}
      <div className="bg-[#121C2F] rounded-2xl border border-slate-800 p-6 space-y-4 shadow-2xl">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <span>Day {activeDay} Problem Set</span>
            {currentDayData?.completed && (
              <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                Completed
              </span>
            )}
          </h2>

          <button
            onClick={handleMarkDayComplete}
            disabled={!currentDayData?.unlocked || currentDayData?.completed}
            className={`px-4 py-1.5 rounded-xl font-bold text-xs shadow-md flex items-center gap-1.5 transition-all ${
              currentDayData?.completed
                ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 cursor-default"
                : "bg-emerald-500 hover:bg-emerald-400 text-slate-950 shadow-emerald-500/20"
            }`}
          >
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>{currentDayData?.completed ? "Day Completed" : "Mark Day Complete & Unlock Next"}</span>
          </button>
        </div>

        <div className="space-y-3">
          {(!currentDayData?.problems || currentDayData.problems.length === 0) ? (
            <div className="p-8 text-center text-xs text-slate-500 font-mono">
              Rest or review day: No mandatory problems assigned for this milestone.
            </div>
          ) : (
            currentDayData.problems.map((p) => (
              <div
                key={p.slug}
                className="p-4 rounded-xl bg-[#0B1220] border border-slate-800 flex items-center justify-between"
              >
                <div>
                  <div className="text-sm font-semibold text-slate-200">{p.title}</div>
                  <div className="text-xs text-slate-400 mt-0.5">Topic: {p.topic}</div>
                </div>
                <div className="flex items-center gap-3">
                  <DifficultyChip difficulty={p.difficulty} />
                  <Link
                    href={`/problems/${p.slug}`}
                    className="px-3.5 py-1.5 rounded-lg bg-cyan-400 hover:bg-cyan-300 text-slate-950 font-bold text-xs transition-colors"
                  >
                    Solve in Editor &rarr;
                  </Link>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
