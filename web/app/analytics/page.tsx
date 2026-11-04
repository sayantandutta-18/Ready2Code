"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import TiltCard from "../../components/ui/TiltCard";
import {
  BarChart3,
  TrendingUp,
  AlertTriangle,
  RotateCcw,
  CheckCircle2,
  Clock,
  ArrowRight,
} from "lucide-react";

export default function AnalyticsPage() {
  const [analytics, setAnalytics] = useState<any>({
    weekly_solves: [
      { week: "Week 1", solves: 2 },
      { week: "Week 2", solves: 4 },
      { week: "Week 3", solves: 3 },
      { week: "Week 4", solves: 6 },
    ],
    topic_acceptance: [
      { topic: "Arrays", rate: 85.0, total_attempts: 14 },
      { topic: "Stack and Queue", rate: 75.0, total_attempts: 8 },
      { topic: "Linked List", rate: 70.0, total_attempts: 6 },
      { topic: "Binary Search", rate: 65.0, total_attempts: 6 },
      { topic: "Dynamic Programming", rate: 45.0, total_attempts: 12 },
    ],
    weak_topics: [{ topic: "Dynamic Programming", rate: 45.0 }],
    avg_time_to_solve_min: 18.4,
    total_submissions: 46,
  });

  useEffect(() => {
    fetch("/api/analytics")
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (data) setAnalytics(data);
      })
      .catch(() => {});
  }, []);

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
                {analytics.weak_topics.map((w: any) => w.topic).join(", ")}
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
            <RotateCcw className="w-4 h-4 text-violet-400" />
            <span>Spaced Repetition Schedule</span>
          </div>
          <div className="text-3xl font-black text-violet-300 font-mono">
            1 &bull; 3 &bull; 7 &bull; 21
          </div>
          <div className="text-[11px] text-slate-500">Forgetting curve retention intervals</div>
        </div>
      </div>

      {/* Solved Per Week Bar Chart & Topic Acceptance */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Weekly Solves Bar Chart */}
        <div className="p-6 rounded-2xl bg-[#121C2F] border border-slate-800 space-y-6 shadow-xl">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-cyan-400" />
            <span>Solved Problems Per Week</span>
          </h2>

          <div className="flex items-end justify-between gap-4 h-48 pt-6 px-2">
            {analytics.weekly_solves.map((w: any) => {
              const heightPct = Math.min(100, (w.solves / 8) * 100);
              return (
                <div key={w.week} className="flex-1 flex flex-col items-center gap-2 h-full justify-end">
                  <span className="font-mono text-xs font-bold text-cyan-300">{w.solves}</span>
                  <div className="w-full bg-slate-900 rounded-t-lg overflow-hidden flex items-end h-32">
                    <div
                      className="w-full bg-gradient-to-t from-cyan-600 to-cyan-400 rounded-t-lg transition-all duration-500"
                      style={{ height: `${heightPct}%` }}
                    />
                  </div>
                  <span className="text-[11px] text-slate-400 font-mono">{w.week}</span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Topic Acceptance Breakdown */}
        <div className="p-6 rounded-2xl bg-[#121C2F] border border-slate-800 space-y-4 shadow-xl">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
            <BarChart3 className="w-4 h-4 text-violet-400" />
            <span>Acceptance Rate by Topic</span>
          </h2>

          <div className="space-y-3.5">
            {analytics.topic_acceptance.map((t: any) => (
              <div key={t.topic} className="space-y-1">
                <div className="flex justify-between text-xs">
                  <span className="text-slate-200 font-semibold">{t.topic}</span>
                  <span
                    className={`font-mono font-bold ${
                      t.rate >= 70
                        ? "text-emerald-400"
                        : t.rate >= 50
                        ? "text-amber-400"
                        : "text-rose-400"
                    }`}
                  >
                    {t.rate}%
                  </span>
                </div>
                <div className="w-full h-2 rounded-full bg-slate-900 overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${
                      t.rate >= 70
                        ? "bg-emerald-400"
                        : t.rate >= 50
                        ? "bg-amber-400"
                        : "bg-rose-500"
                    }`}
                    style={{ width: `${t.rate}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
