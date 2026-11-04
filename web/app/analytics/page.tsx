"use client";

import React from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import TiltCard from "../../components/ui/TiltCard";
import LoadingSkeleton from "../../components/ui/LoadingSkeleton";
import QueryErrorState from "../../components/ui/QueryErrorState";
import { fetchApi } from "../../lib/api";
import {
  BarChart3,
  TrendingUp,
  AlertTriangle,
  RotateCcw,
  CheckCircle2,
  Clock,
  ArrowRight,
} from "lucide-react";

interface WeeklySolve {
  week: string;
  solves: number;
}

interface TopicAcceptance {
  topic: string;
  rate: number;
  total_attempts: number;
}

interface WeakTopic {
  topic: string;
  rate: number;
}

interface AnalyticsData {
  weekly_solves: WeeklySolve[];
  topic_acceptance: TopicAcceptance[];
  weak_topics: WeakTopic[];
  avg_time_to_solve_min: number;
  total_submissions: number;
}

export default function AnalyticsPage() {
  const {
    data: analytics,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<AnalyticsData>({
    queryKey: ["analytics"],
    queryFn: () => fetchApi<AnalyticsData>("/analytics"),
  });

  return (
    <div className="max-w-6xl mx-auto px-4 lg:px-8 py-10 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-black text-white tracking-tight flex items-center gap-3">
            <BarChart3 className="w-8 h-8 text-cyan-400" />
            <span>Learner Performance Analytics</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Real-time telemetry on algorithmic velocity, acceptance rates, and weak-topic detection.
          </p>
        </div>

        <Link
          href="/review"
          className="px-4 py-2.5 rounded-xl bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white font-semibold text-xs shadow-lg shadow-violet-600/20 flex items-center gap-2 self-start sm:self-auto transition-all"
        >
          <RotateCcw className="w-4 h-4" />
          <span>Open Spaced Review Queue</span>
        </Link>
      </div>

      {isError && (
        <QueryErrorState
          title="Could not load analytics"
          message={error instanceof Error ? error.message : "Error contacting analytics API"}
          onRetry={() => refetch()}
        />
      )}

      {isLoading ? (
        <div className="space-y-6">
          <LoadingSkeleton rows={2} className="h-28" />
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <LoadingSkeleton rows={4} className="h-64" />
            <LoadingSkeleton rows={4} className="h-64" />
          </div>
        </div>
      ) : analytics ? (
        <>
          {/* Weak Topics Attention Banner (C2.5 specification) */}
          {analytics.weak_topics?.length > 0 && (
            <div className="p-6 rounded-2xl bg-amber-950/20 border border-amber-500/40 flex flex-col sm:flex-row sm:items-center justify-between gap-4 shadow-xl">
              <div className="flex items-center gap-3.5">
                <div className="p-3 rounded-xl bg-amber-500/20 text-amber-400 shrink-0">
                  <AlertTriangle className="w-6 h-6" />
                </div>
                <div>
                  <div className="text-xs uppercase font-mono font-bold tracking-wider text-amber-400">
                    Cognitive Bottleneck Detected
                  </div>
                  <div className="text-base font-bold text-white mt-0.5">
                    Practice Recommended:{" "}
                    {analytics.weak_topics.map((w) => w.topic).join(", ")}
                  </div>
                  <div className="text-xs text-slate-400 mt-0.5">
                    Acceptance rate is below 50% across repeated submissions.
                  </div>
                </div>
              </div>

              <Link
                href="/problems?topic=dp"
                className="px-4 py-2 rounded-xl bg-amber-400 hover:bg-amber-300 text-slate-950 font-bold text-xs shrink-0 self-start sm:self-center transition-all shadow"
              >
                Target Weak Topic
              </Link>
            </div>
          )}

          {/* Top Metrics Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
            <div className="p-6 rounded-2xl bg-[#121C2F] border border-slate-800 space-y-1 shadow-xl">
              <div className="text-xs text-slate-400 flex items-center gap-1.5">
                <Clock className="w-4 h-4 text-cyan-400" />
                <span>Average Solve Time</span>
              </div>
              <div className="text-3xl font-black text-cyan-300 font-mono">
                {analytics.avg_time_to_solve_min} <span className="text-base text-slate-400">mins</span>
              </div>
              <div className="text-[11px] text-slate-500">Benchmark: 20 mins for interviews</div>
            </div>

            <div className="p-6 rounded-2xl bg-[#121C2F] border border-slate-800 space-y-1 shadow-xl">
              <div className="text-xs text-slate-400 flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                <span>Total Evaluated Runs</span>
              </div>
              <div className="text-3xl font-black text-emerald-400 font-mono">
                {analytics.total_submissions}
              </div>
              <div className="text-[11px] text-slate-500">Includes sample & hidden executions</div>
            </div>

            <div className="p-6 rounded-2xl bg-[#121C2F] border border-slate-800 space-y-1 shadow-xl">
              <div className="text-xs text-slate-400 flex items-center gap-1.5">
                <TrendingUp className="w-4 h-4 text-violet-400" />
                <span>Weekly Trend</span>
              </div>
              <div className="text-3xl font-black text-violet-300 font-mono">
                +{analytics.weekly_solves[analytics.weekly_solves.length - 1]?.solves || 0}
              </div>
              <div className="text-[11px] text-slate-500">Solves in current active week</div>
            </div>
          </div>

          {/* Main Visualizations Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Weekly Solves Bar Chart */}
            <div className="lg:col-span-6 p-6 rounded-2xl bg-[#121C2F] border border-slate-800 space-y-6 shadow-xl">
              <div className="flex items-center justify-between">
                <h3 className="font-bold text-white text-base">Weekly Solves Velocity</h3>
                <span className="text-xs text-slate-400 font-mono">Past 4 Weeks</span>
              </div>

              <div className="h-52 flex items-end justify-between gap-4 pt-6 px-4 border-b border-slate-800">
                {analytics.weekly_solves.map((w) => {
                  const maxSolve = Math.max(...analytics.weekly_solves.map((s) => s.solves), 1);
                  const heightPct = Math.round((w.solves / maxSolve) * 100);
                  return (
                    <div key={w.week} className="flex-1 flex flex-col items-center gap-2 group">
                      <div className="text-xs font-mono text-cyan-400 opacity-0 group-hover:opacity-100 transition-opacity">
                        {w.solves}
                      </div>
                      <div
                        className="w-full bg-gradient-to-t from-cyan-600 to-cyan-400 rounded-t-lg transition-all duration-500 group-hover:brightness-110"
                        style={{ height: `${heightPct}%` }}
                      />
                      <span className="text-[11px] text-slate-400 font-mono">{w.week}</span>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Topic Acceptance Breakdown */}
            <div className="lg:col-span-6 p-6 rounded-2xl bg-[#121C2F] border border-slate-800 space-y-6 shadow-xl">
              <div className="flex items-center justify-between">
                <h3 className="font-bold text-white text-base">Topic Acceptance Rates</h3>
                <span className="text-xs text-slate-400 font-mono">Weighted by Attempts</span>
              </div>

              <div className="space-y-4">
                {analytics.topic_acceptance.map((t) => (
                  <div key={t.topic} className="space-y-1.5">
                    <div className="flex justify-between text-xs font-semibold">
                      <span className="text-slate-200">{t.topic}</span>
                      <span
                        className={`font-mono ${
                          t.rate >= 70
                            ? "text-emerald-400"
                            : t.rate >= 50
                            ? "text-cyan-400"
                            : "text-amber-400"
                        }`}
                      >
                        {t.rate}% ({t.total_attempts} attempts)
                      </span>
                    </div>
                    <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all duration-500 ${
                          t.rate >= 70
                            ? "bg-emerald-400"
                            : t.rate >= 50
                            ? "bg-cyan-400"
                            : "bg-amber-400"
                        }`}
                        style={{ width: `${t.rate}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </>
      ) : null}
    </div>
  );
}
