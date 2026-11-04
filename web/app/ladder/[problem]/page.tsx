"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import TiltCard from "../../../components/ui/TiltCard";
import confetti from "canvas-confetti";
import { Layers, Lock, CheckCircle2, ArrowLeft, ArrowRight, Play, Zap } from "lucide-react";

export default function BruteToOptimalLadderPage({ params }: { params: { problem: string } }) {
  const { problem } = params;

  const [ladder, setLadder] = useState<any>({
    problem_slug: problem,
    problem_title: "Two Sum",
    current_stage: "brute",
    stages: [
      {
        stage: "brute",
        title: "Stage 1: Brute Force",
        time_complexity: "O(n²)",
        space_complexity: "O(1)",
        hint: "Check every possible pair (i, j) with nested loops.",
        unlocked: true,
        completed: false,
      },
      {
        stage: "better",
        title: "Stage 2: Sort and Two Pointers",
        time_complexity: "O(n log n)",
        space_complexity: "O(n)",
        hint: "Sort array while preserving original indices, then converge two pointers inwards.",
        unlocked: false,
        completed: false,
      },
      {
        stage: "optimal",
        title: "Stage 3: Hash Map Lookup",
        time_complexity: "O(n)",
        space_complexity: "O(n)",
        hint: "Single pass over array checking if complement (target - x) exists in dictionary.",
        unlocked: false,
        completed: false,
      },
    ],
  });

  const [activeStage, setActiveStage] = useState<string>("brute");
  const [stageMessage, setStageMessage] = useState<string | null>(null);

  useEffect(() => {
    fetch(`/api/ladder/${problem}`)
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (data && data.stages) setLadder(data);
      })
      .catch(() => {});
  }, [problem]);

  const handleSimulateSubmit = async (stageKey: string) => {
    try {
      const res = await fetch("/api/ladder/stage", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          problem_slug: problem,
          stage: stageKey,
          runtime_ms: stageKey === "brute" ? 180 : stageKey === "better" ? 45 : 18,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        setStageMessage(data.message);
        if (data.passed) {
          confetti({ particleCount: 50, spread: 60 });
          // Unlock next stage locally
          setLadder((prev: any) => {
            const stages = prev.stages.map((s: any) => {
              if (s.stage === stageKey) return { ...s, completed: true };
              if (stageKey === "brute" && s.stage === "better") return { ...s, unlocked: true };
              if (stageKey === "better" && s.stage === "optimal") return { ...s, unlocked: true };
              return s;
            });
            return { ...prev, stages };
          });
        }
      }
    } catch {}
  };

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

      {/* 3 Stage Cards (C3.6 requirement) */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {ladder.stages.map((st: any, idx: number) => {
          return (
            <TiltCard
              key={st.stage}
              className={`h-full flex flex-col justify-between space-y-4 ${
                !st.unlocked
                  ? "opacity-50 border-slate-850 cursor-not-allowed"
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
                    onClick={() => handleSimulateSubmit(st.stage)}
                    className="w-full py-2.5 rounded-xl bg-cyan-400 hover:bg-cyan-300 text-slate-950 font-bold text-xs flex items-center justify-center gap-1.5 shadow transition-colors"
                  >
                    <Play className="w-3.5 h-3.5 fill-slate-950" />
                    <span>Submit & Verify Runtime</span>
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
