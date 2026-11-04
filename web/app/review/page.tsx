"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import DifficultyChip from "../../components/ui/DifficultyChip";
import { RotateCcw, Calendar, CheckCircle2, XCircle, ArrowLeft, ChevronRight, Brain } from "lucide-react";

export default function ReviewQueuePage() {
  const [reviewData, setReviewData] = useState<any>({
    due_today: [
      {
        problem_id: "1",
        slug: "two-sum",
        title: "Two Sum",
        difficulty: "easy",
        topic: "Arrays",
        interval_days: 1,
      },
      {
        problem_id: "6",
        slug: "maximum-subarray",
        title: "Maximum Subarray",
        difficulty: "medium",
        topic: "Arrays",
        interval_days: 1,
      },
    ],
    upcoming: [
      {
        problem_id: "2",
        slug: "valid-parentheses",
        title: "Valid Parentheses",
        difficulty: "easy",
        topic: "Stack",
        due_date: "In 3 Days",
        interval_days: 3,
      },
      {
        problem_id: "8",
        slug: "number-of-islands",
        title: "Number of Islands",
        difficulty: "medium",
        topic: "Graphs",
        due_date: "In 7 Days",
        interval_days: 7,
      },
    ],
    overdue_count: 0,
  });

  const [activeItem, setActiveItem] = useState<any>(null);

  useEffect(() => {
    fetch("/api/review")
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (data) {
          setReviewData(data);
          if (data.due_today?.length > 0) setActiveItem(data.due_today[0]);
        }
      })
      .catch(() => {});
  }, []);

  const handleGrade = async (passed: boolean) => {
    if (!activeItem) return;
    try {
      await fetch("/api/review/grade", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          problem_id: activeItem.problem_id,
          passed: passed,
        }),
      });

      // Advance queue locally
      setReviewData((prev: any) => {
        const nextDue = prev.due_today.filter((x: any) => x.slug !== activeItem.slug);
        setActiveItem(nextDue.length > 0 ? nextDue[0] : null);
        return {
          ...prev,
          due_today: nextDue,
        };
      });
    } catch {}
  };

  return (
    <div className="max-w-5xl mx-auto px-4 lg:px-8 py-10 space-y-8">
      {/* Back button */}
      <Link href="/analytics" className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-cyan-400 font-mono">
        <ArrowLeft className="w-3.5 h-3.5" /> Back to Analytics
      </Link>

      {/* Header */}
      <div className="p-8 rounded-3xl bg-[#121C2F] border border-slate-800 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-violet-500/10 border border-violet-500/30 text-violet-300 text-xs font-semibold mb-2">
            <Brain className="w-4 h-4 text-violet-400" />
            <span>Spaced Repetition &bull; Ebbinghaus Retention Engine</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-white">Daily Review Deck</h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-xl">
            Problems automatically reappear at 1, 3, 7, and 21 days intervals to convert short-term
            pattern recall into permanent algorithmic intuition.
          </p>
        </div>

        <div className="p-4 rounded-2xl bg-[#0B1220] border border-slate-800 text-center sm:self-center">
          <div className="text-xs text-slate-400 mb-1">Due for Review Today</div>
          <div className="text-3xl font-black text-cyan-300 font-mono">
            {reviewData.due_today?.length || 0}
          </div>
          <div className="text-[11px] text-slate-500">Cards Remaining</div>
        </div>
      </div>

      {/* Active Review Flashcard */}
      {activeItem ? (
        <div className="p-8 rounded-3xl bg-gradient-to-br from-[#121C2F] to-[#16233B] border border-cyan-500/30 space-y-6 shadow-2xl">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <span className="text-xs font-mono uppercase tracking-wider text-cyan-400">
              Active Recall Card &bull; Current Interval: {activeItem.interval_days} Day(s)
            </span>
            <DifficultyChip difficulty={activeItem.difficulty} />
          </div>

          <div className="space-y-2">
            <h2 className="text-2xl font-black text-white">{activeItem.title}</h2>
            <div className="text-xs text-slate-400">Topic: {activeItem.topic}</div>
            <p className="text-sm text-slate-300 pt-2 leading-relaxed">
              Mentally trace your optimal strategy for this problem. What is the time complexity?
              Which data structure eliminates redundant iterations?
            </p>
          </div>

          <div className="pt-4 border-t border-slate-800 flex flex-wrap items-center justify-between gap-4">
            <Link
              href={`/problems/${activeItem.slug}`}
              className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition-colors"
            >
              Open in Code Editor &rarr;
            </Link>

            <div className="flex items-center gap-3">
              <button
                onClick={() => handleGrade(false)}
                className="px-4 py-2 rounded-xl bg-rose-500/20 hover:bg-rose-500/30 text-rose-300 border border-rose-500/40 text-xs font-bold flex items-center gap-1.5 transition-all"
              >
                <XCircle className="w-4 h-4" />
                <span>Forgot (Reset to 1 Day)</span>
              </button>

              <button
                onClick={() => handleGrade(true)}
                className="px-5 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-xs font-bold flex items-center gap-1.5 shadow transition-all"
              >
                <CheckCircle2 className="w-4 h-4 text-slate-950" />
                <span>Recalled (Advance Interval)</span>
              </button>
            </div>
          </div>
        </div>
      ) : (
        <div className="p-12 text-center bg-[#121C2F] rounded-3xl border border-slate-800 space-y-3">
          <CheckCircle2 className="w-12 h-12 text-emerald-400 mx-auto" />
          <h2 className="text-xl font-bold text-white">All Caught Up For Today!</h2>
          <p className="text-xs text-slate-400 max-w-md mx-auto">
            You have successfully reviewed all scheduled problems. New cards will appear according
            to your forgetting curve.
          </p>
        </div>
      )}

      {/* Upcoming Review Schedule */}
      <div className="bg-[#121C2F] rounded-2xl border border-slate-800 p-6 space-y-4 shadow-xl">
        <h2 className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
          <Calendar className="w-4 h-4 text-violet-400" />
          <span>Upcoming Spaced Interval Pipeline</span>
        </h2>

        <div className="divide-y divide-slate-800/80">
          {(reviewData.upcoming || []).map((u: any) => (
            <div key={u.slug} className="py-3 flex items-center justify-between text-xs">
              <div className="flex items-center gap-2">
                <span className="font-semibold text-slate-200">{u.title}</span>
                <span className="text-slate-500">({u.topic})</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="font-mono text-cyan-400">{u.due_date}</span>
                <span className="px-2 py-0.5 rounded bg-[#0B1220] border border-slate-700 text-slate-400 font-mono">
                  {u.interval_days}d interval
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
