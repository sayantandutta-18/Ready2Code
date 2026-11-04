"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import DifficultyChip from "../../components/ui/DifficultyChip";
import LoadingSkeleton from "../../components/ui/LoadingSkeleton";
import EmptyState from "../../components/ui/EmptyState";
import QueryErrorState from "../../components/ui/QueryErrorState";
import { fetchApi } from "../../lib/api";
import { RotateCcw, Calendar, CheckCircle2, XCircle, ArrowLeft, ChevronRight, Brain } from "lucide-react";

interface ReviewItem {
  problem_id: string;
  slug: string;
  title: string;
  difficulty: "easy" | "medium" | "hard";
  topic: string;
  interval_days: number;
  due_date?: string;
}

interface ReviewQueueData {
  due_today: ReviewItem[];
  upcoming: ReviewItem[];
  overdue_count: number;
}

export default function ReviewQueuePage() {
  const queryClient = useQueryClient();
  const [selectedItem, setSelectedItem] = useState<ReviewItem | null>(null);

  const {
    data: reviewData,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<ReviewQueueData>({
    queryKey: ["review-queue"],
    queryFn: () => fetchApi<ReviewQueueData>("/review"),
  });

  const dueItems = reviewData?.due_today || [];
  const activeItem = selectedItem || dueItems[0] || null;

  const gradeMutation = useMutation({
    mutationFn: ({ problemId, passed }: { problemId: string; passed: boolean }) =>
      fetchApi("/review/grade", {
        method: "POST",
        body: JSON.stringify({ problem_id: problemId, passed }),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["review-queue"] });
      setSelectedItem(null);
    },
  });

  const handleGrade = (passed: boolean) => {
    if (!activeItem) return;
    gradeMutation.mutate({ problemId: activeItem.problem_id, passed });
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
            {dueItems.length}
          </div>
          <div className="text-[11px] text-slate-500">Cards Remaining</div>
        </div>
      </div>

      {isError && (
        <QueryErrorState
          title="Could not load review deck"
          message={error instanceof Error ? error.message : "Error contacting review service"}
          onRetry={() => refetch()}
        />
      )}

      {isLoading ? (
        <LoadingSkeleton rows={4} className="h-64" />
      ) : activeItem ? (
        <div className="p-8 rounded-3xl bg-gradient-to-br from-[#121C2F] to-[#16243D] border border-violet-500/30 shadow-2xl space-y-6">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono uppercase tracking-wider text-violet-400 font-semibold">
              Current Active Recall Card &bull; Interval: {activeItem.interval_days} Day(s)
            </span>
            <DifficultyChip difficulty={activeItem.difficulty} />
          </div>

          <div className="space-y-2">
            <h2 className="text-2xl font-bold text-white">{activeItem.title}</h2>
            <p className="text-xs text-slate-400 font-mono">Topic: {activeItem.topic}</p>
            <p className="text-sm text-slate-300 pt-2 leading-relaxed">
              Without looking at the full solution, formulate your optimal intuition, data structure,
              and asymptotic time complexity in your head.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-center gap-4 pt-4 border-t border-slate-800">
            <Link
              href={`/problems/${activeItem.slug}`}
              className="w-full sm:w-auto px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold transition-all text-center"
            >
              Solve in Arena
            </Link>

            <div className="flex-1 flex items-center justify-end gap-3 w-full sm:w-auto">
              <button
                type="button"
                onClick={() => handleGrade(false)}
                disabled={gradeMutation.isPending}
                className="flex-1 sm:flex-initial inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-rose-500/15 hover:bg-rose-500/25 border border-rose-500/30 text-rose-300 font-bold text-xs transition-all disabled:opacity-50"
              >
                <XCircle className="w-4 h-4" />
                <span>Forgot / Reset Interval</span>
              </button>

              <button
                type="button"
                onClick={() => handleGrade(true)}
                disabled={gradeMutation.isPending}
                className="flex-1 sm:flex-initial inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-500/15 hover:bg-emerald-500/25 border border-emerald-500/30 text-emerald-300 font-bold text-xs transition-all disabled:opacity-50"
              >
                <CheckCircle2 className="w-4 h-4" />
                <span>Remembered (+Advance)</span>
              </button>
            </div>
          </div>
        </div>
      ) : (
        <EmptyState
          title="Review queue cleared!"
          description="You have completed all active recall flashcards for today. Great job keeping your algorithmic recall sharp!"
          icon={<CheckCircle2 className="w-7 h-7 text-emerald-400" />}
        />
      )}

      {/* Upcoming Deck Preview */}
      {reviewData?.upcoming && reviewData.upcoming.length > 0 && (
        <div className="space-y-4 pt-4">
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Calendar className="w-4 h-4 text-slate-400" />
            <span>Upcoming Spaced Cards</span>
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {reviewData.upcoming.map((u) => (
              <div
                key={u.problem_id}
                className="p-4 rounded-xl bg-[#121C2F]/60 border border-slate-800 flex items-center justify-between"
              >
                <div>
                  <div className="text-sm font-semibold text-slate-200">{u.title}</div>
                  <div className="text-xs text-slate-500 font-mono mt-0.5">
                    {u.topic} &bull; Interval: {u.interval_days} Days
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-xs font-mono font-semibold text-cyan-400 bg-cyan-950/60 border border-cyan-800 px-2 py-0.5 rounded">
                    {u.due_date}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
