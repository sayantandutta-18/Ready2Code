"use client";

import React from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { fetchApi } from "@/lib/api";
import LoadingSkeleton from "@/components/ui/LoadingSkeleton";
import QueryErrorState from "@/components/ui/QueryErrorState";
import EmptyState from "@/components/ui/EmptyState";
import DifficultyChip from "../../../components/ui/DifficultyChip";
import { ListTodo, CheckCircle2, Circle, ArrowLeft, ChevronRight, GripVertical } from "lucide-react";

interface ListItemProblem {
  id: string;
  slug: string;
  title: string;
  difficulty: "easy" | "medium" | "hard";
  topic: string;
  position: number;
  solved: boolean;
}

interface ListDetail {
  id: string;
  name: string;
  description: string;
  is_system: boolean;
  problems: ListItemProblem[];
  total_problems: number;
  solved_count: number;
  progress_pct: number;
}

export default function ListDetailPage({ params }: { params: { id: string } }) {
  const { id } = params;

  const {
    data: listData,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<ListDetail>({
    queryKey: ["list", id],
    queryFn: () => fetchApi<ListDetail>(`/lists/${id}`),
  });

  if (isLoading) {
    return (
      <div className="max-w-5xl mx-auto px-4 lg:px-8 py-10 space-y-6">
        <LoadingSkeleton variant="title" className="w-48 h-6" />
        <LoadingSkeleton variant="card" className="h-40" />
        <LoadingSkeleton variant="table" rows={6} />
      </div>
    );
  }

  if (isError || !listData) {
    return (
      <div className="max-w-5xl mx-auto px-4 lg:px-8 py-10">
        <QueryErrorState
          title="Failed to load problem list"
          message={error instanceof Error ? error.message : "The requested list could not be retrieved."}
          onRetry={() => refetch()}
        />
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 lg:px-8 py-10 space-y-8">
      {/* Back button */}
      <Link href="/lists" className="inline-flex items-center gap-1.5 min-h-[44px] px-2 text-xs text-slate-400 hover:text-cyan-400 font-mono">
        <ArrowLeft className="w-4 h-4" /> Back to Lists
      </Link>

      {/* Header Info */}
      <div className="p-8 rounded-3xl bg-[#121C2F] border border-slate-800 shadow-2xl space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl sm:text-3xl font-black text-white">{listData.name}</h1>
            <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-2xl">{listData.description}</p>
          </div>
          <div className="text-right sm:self-center">
            <div className="text-2xl font-black text-cyan-400 font-mono">{listData.progress_pct}%</div>
            <div className="text-xs text-slate-500">
              {listData.solved_count} / {listData.total_problems} Solved
            </div>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="w-full h-2 rounded-full bg-slate-900 overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-cyan-400 to-indigo-500 transition-all duration-500"
            style={{ width: `${listData.progress_pct}%` }}
          />
        </div>
      </div>

      {/* Problems Checklist Table */}
      {listData.problems.length === 0 ? (
        <EmptyState
          title="No problems in this list"
          description="This list is currently empty. Add problems to start tracking progress."
        />
      ) : (
        <div className="bg-[#121C2F] rounded-2xl border border-slate-800 overflow-hidden shadow-2xl">
          <div className="divide-y divide-slate-800/80">
            {listData.problems.map((p, index) => (
              <div
                key={p.slug}
                className="p-3.5 sm:p-4 flex flex-wrap sm:flex-nowrap items-center justify-between gap-3 hover:bg-slate-800/30 transition-colors group"
              >
                <div className="flex items-center gap-3 min-w-0 flex-1">
                  <GripVertical className="w-4 h-4 text-slate-600 cursor-grab shrink-0 hidden sm:block" />
                  {p.solved ? (
                    <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
                  ) : (
                    <Circle className="w-5 h-5 text-slate-600 shrink-0" />
                  )}
                  <div className="min-w-0 flex-1">
                    <Link
                      href={`/problems/${p.slug}`}
                      className="text-sm font-semibold text-slate-100 group-hover:text-cyan-300 transition-colors flex items-center gap-1.5"
                    >
                      <span className="text-slate-500 font-mono text-xs shrink-0">{index + 1}.</span>
                      <span className="truncate">{p.title}</span>
                    </Link>
                    <div className="text-[11px] text-slate-400 mt-0.5 truncate">Topic: {p.topic}</div>
                  </div>
                </div>

                <div className="flex items-center gap-2.5 shrink-0 ml-auto sm:ml-0">
                  <DifficultyChip difficulty={p.difficulty} />
                  <Link
                    href={`/problems/${p.slug}`}
                    className="min-h-[44px] px-3.5 py-2 rounded-xl bg-slate-800 group-hover:bg-cyan-500/20 text-slate-300 group-hover:text-cyan-300 text-xs font-semibold transition-all flex items-center gap-1.5 border border-slate-700"
                  >
                    <span>Solve</span>
                    <ChevronRight className="w-4 h-4" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

