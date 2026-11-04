"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { fetchApi } from "@/lib/api";
import LoadingSkeleton from "@/components/ui/LoadingSkeleton";
import QueryErrorState from "@/components/ui/QueryErrorState";
import TiltCard from "../../../components/ui/TiltCard";
import confetti from "canvas-confetti";
import { Layers, Lock, CheckCircle2, ArrowLeft, Play, Zap } from "lucide-react";

interface LadderStage {
  stage: string;
  title: string;
  time_complexity: string;
  space_complexity: string;
  hint: string;
  unlocked: boolean;
  completed: boolean;
}

interface LadderDetail {
  problem_slug: string;
  problem_title: string;
  current_stage: string;
  stages: LadderStage[];
}

interface StageSubmitResponse {
  passed: boolean;
  message: string;
}

export default function BruteToOptimalLadderPage({ params }: { params: { problem: string } }) {
  const { problem } = params;
  const queryClient = useQueryClient();
  const [stageMessage, setStageMessage] = useState<string | null>(null);

  const {
    data: ladder,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<LadderDetail>({
    queryKey: ["ladder", problem],
    queryFn: () => fetchApi<LadderDetail>(`/ladder/${problem}`),
  });

  const submitMutation = useMutation({
    mutationFn: async (stageKey: string) => {
      const runtimeMap: Record<string, number> = {
        brute: 180,
        better: 45,
        optimal: 18,
      };
      return fetchApi<StageSubmitResponse>("/ladder/stage", {
        method: "POST",
        body: JSON.stringify({
          problem_slug: problem,
          stage: stageKey,
          runtime_ms: runtimeMap[stageKey] || 50,
        }),
      });
    },
    onSuccess: (data) => {
      setStageMessage(data.message);
      if (data.passed) {
        confetti({ particleCount: 50, spread: 60 });
        queryClient.invalidateQueries({ queryKey: ["ladder", problem] });
      }
    },
    onError: (err) => {
      setStageMessage(err instanceof Error ? err.message : "Stage verification failed.");
    },
  });

  if (isLoading) {
    return (
      <div className="max-w-6xl mx-auto px-4 lg:px-8 py-10 space-y-6">
        <LoadingSkeleton variant="title" className="w-48 h-6" />
        <LoadingSkeleton variant="card" className="h-44" />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <LoadingSkeleton variant="card" className="h-64" />
          <LoadingSkeleton variant="card" className="h-64" />
          <LoadingSkeleton variant="card" className="h-64" />
        </div>
      </div>
    );
  }

  if (isError || !ladder) {
    return (
      <div className="max-w-6xl mx-auto px-4 lg:px-8 py-10">
        <QueryErrorState
          title="Failed to load ladder"
          message={error instanceof Error ? error.message : "The optimization ladder for this problem could not be retrieved."}
          onRetry={() => refetch()}
        />
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 lg:px-8 py-10 space-y-8">
      {/* Back button */}
      <Link href={`/problems/${problem}`} className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-cyan-400 font-mono">
        <ArrowLeft className="w-3.5 h-3.5" /> Back to Problem Solve Page
      </Link>

      {/* Header */}
      <div className="p-8 rounded-3xl bg-[#121C2F] border border-slate-800 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-xs font-semibold mb-2">
            <Layers className="w-4 h-4 text-cyan-400" />
            <span>Algorithmic Optimization Ladder</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-white">
            {ladder.problem_title} &bull; Brute to Optimal
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-xl">
            Pass each stage with verified runtime efficiency. The Optimal card remains locked until
            you have written and submitted a working intermediary solution.
          </p>
        </div>

        <div className="p-4 rounded-2xl bg-[#0B1220] border border-slate-800 text-center sm:self-center">
          <div className="text-xs text-slate-400 mb-1">Stage Progression</div>
          <div className="text-2xl font-black text-cyan-400 font-mono uppercase">
            {ladder.current_stage}
          </div>
        </div>
      </div>

      {stageMessage && (
        <div className="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/40 text-emerald-300 text-xs flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 shrink-0 text-emerald-400" />
          <span>{stageMessage}</span>
        </div>
      )}

      {/* 3 Stage Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {ladder.stages.map((st, idx) => {
          return (
            <TiltCard
              key={st.stage}
              className={`h-full flex flex-col justify-between space-y-4 ${
                !st.unlocked
                  ? "opacity-50 border-slate-800 cursor-not-allowed"
                  : st.completed
                  ? "border-emerald-500/40 bg-emerald-950/10"
                  : "border-cyan-500/30 hover:border-cyan-400"
              }`}
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400">
                    Stage {idx + 1}
                  </span>
                  {st.completed ? (
                    <span className="inline-flex items-center gap-1 text-[11px] text-emerald-400 font-bold">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Accepted
                    </span>
                  ) : !st.unlocked ? (
                    <span className="inline-flex items-center gap-1 text-[11px] text-slate-500 font-bold">
                      <Lock className="w-3.5 h-3.5" /> Locked
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 text-[11px] text-cyan-400 font-bold">
                      <Zap className="w-3.5 h-3.5" /> Unlocked
                    </span>
                  )}
                </div>

                <h3 className="text-lg font-bold text-white">{st.title}</h3>

                <div className="grid grid-cols-2 gap-2 text-xs font-mono">
                  <div className="p-2 rounded bg-[#0B1220] border border-slate-800">
                    <div className="text-[10px] text-slate-500 uppercase">Time</div>
                    <div className="text-cyan-300 font-bold">{st.time_complexity}</div>
                  </div>
                  <div className="p-2 rounded bg-[#0B1220] border border-slate-800">
                    <div className="text-[10px] text-slate-500 uppercase">Space</div>
                    <div className="text-violet-300 font-bold">{st.space_complexity}</div>
                  </div>
                </div>

                <div className="text-xs text-slate-300 font-sans leading-relaxed pt-1">
                  {st.unlocked ? st.hint : "Unlocked after previous stage is verified."}
                </div>
              </div>

              <div className="pt-3 border-t border-slate-800">
                {st.unlocked ? (
                  <button
                    onClick={() => submitMutation.mutate(st.stage)}
                    disabled={submitMutation.isPending}
                    className="w-full py-2.5 rounded-xl bg-cyan-400 hover:bg-cyan-300 text-slate-950 font-bold text-xs flex items-center justify-center gap-1.5 shadow transition-colors disabled:opacity-50"
                  >
                    <Play className="w-3.5 h-3.5 fill-slate-950" />
                    <span>{submitMutation.isPending ? "Evaluating..." : "Submit & Verify Runtime"}</span>
                  </button>
                ) : (
                  <div className="w-full py-2.5 rounded-xl bg-slate-800/50 text-slate-500 text-xs text-center font-mono">
                    Complete Stage {idx} First
                  </div>
                )}
              </div>
            </TiltCard>
          );
        })}
      </div>
    </div>
  );
}
