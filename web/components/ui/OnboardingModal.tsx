"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Sparkles,
  Flame,
  CheckCircle2,
  ArrowRight,
  X,
  Compass,
  Trophy,
  Zap,
  Code2,
} from "lucide-react";
import Button from "./Button";

export default function OnboardingModal() {
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(false);
  const [step, setStep] = useState<1 | 2 | 3>(1);
  const [selectedLevel, setSelectedLevel] = useState<"beginner" | "intermediate" | "advanced">("beginner");

  useEffect(() => {
    if (typeof window === "undefined") return;
    const dismissed = localStorage.getItem("ready2code_onboarding_dismissed");
    if (!dismissed) {
      setIsOpen(true);
    }
  }, []);

  const handleDismiss = () => {
    localStorage.setItem("ready2code_onboarding_dismissed", "true");
    setIsOpen(false);
  };

  const handleNext = () => {
    if (step < 3) {
      setStep((prev) => (prev + 1) as 1 | 2 | 3);
    } else {
      handleDismiss();
      // Jump to first recommended problem
      const recommendedSlug =
        selectedLevel === "beginner"
          ? "two-sum-sorted-offsets"
          : selectedLevel === "intermediate"
          ? "container-with-bounded-walls"
          : "largest-rectangle-histogram-area";
      router.push(`/problems/${recommendedSlug}`);
    }
  };

  if (!isOpen) return null;

  const levelProblems = {
    beginner: {
      slug: "two-sum-sorted-offsets",
      title: "Two Sum in Ascending Sorted Sequence",
      desc: "Perfect starter problem focusing on two pointers and sorting invariants.",
    },
    intermediate: {
      slug: "container-with-bounded-walls",
      title: "Container with Most Water Area",
      desc: "Classic greedy pointer convergence pattern used heavily in tech interviews.",
    },
    advanced: {
      slug: "largest-rectangle-histogram-area",
      title: "Largest Rectangle in Skyline Histogram",
      desc: "Challenging monotonic stack pattern problem with boundary optimizations.",
    },
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="onboarding-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/85 backdrop-blur-md animate-in fade-in duration-200"
    >
      <div
        className="w-full max-w-lg bg-[#121C2F] border border-slate-800 rounded-3xl shadow-2xl p-6 sm:p-8 relative overflow-hidden text-slate-200"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Glow Accents */}
        <div className="absolute -top-20 -right-20 w-44 h-44 bg-cyan-500/15 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -bottom-20 -left-20 w-44 h-44 bg-violet-500/15 rounded-full blur-3xl pointer-events-none" />

        {/* Dismiss Button */}
        <button
          onClick={handleDismiss}
          className="absolute top-5 right-5 p-1.5 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          aria-label="Skip onboarding"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Step Indicator */}
        <div className="flex items-center gap-2 mb-6">
          {[1, 2, 3].map((s) => (
            <div
              key={s}
              className={`h-1.5 rounded-full transition-all ${
                s === step
                  ? "w-8 bg-cyan-400 shadow-sm shadow-cyan-400/50"
                  : s < step
                  ? "w-4 bg-emerald-400"
                  : "w-4 bg-slate-800"
              }`}
            />
          ))}
          <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400 ml-auto">
            Step {step} of 3
          </span>
        </div>

        {/* Step 1: Pick Level */}
        {step === 1 && (
          <div className="space-y-5 animate-in slide-in-from-right duration-200">
            <div>
              <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-xs font-semibold mb-2">
                <Sparkles className="w-3.5 h-3.5" />
                <span>Welcome to Ready2Code</span>
              </div>
              <h2 id="onboarding-title" className="text-xl sm:text-2xl font-black text-white tracking-tight">
                Pick Your DSA Starting Level
              </h2>
              <p className="text-xs sm:text-sm text-slate-400 mt-1">
                We customize your problem queue and roadmap based on your current experience.
              </p>
            </div>

            <div className="space-y-2.5">
              {[
                {
                  id: "beginner" as const,
                  title: "Foundations & Blind 75",
                  desc: "Learn core arrays, two pointers, strings, and hash table patterns from scratch.",
                  badge: "Easy to Medium",
                },
                {
                  id: "intermediate" as const,
                  title: "Interview Pattern Mastery",
                  desc: "Master trees, graphs, sliding windows, heaps, and dynamic programming.",
                  badge: "Medium Core",
                },
                {
                  id: "advanced" as const,
                  title: "FAANG Hard & Speed Contests",
                  desc: "Tackle advanced graph cycles, 2D DP matrices, and 1v1 live coding battles.",
                  badge: "Hard & Contests",
                },
              ].map((lvl) => {
                const isSelected = selectedLevel === lvl.id;
                return (
                  <div
                    key={lvl.id}
                    onClick={() => setSelectedLevel(lvl.id)}
                    className={`p-3.5 sm:p-4 rounded-2xl border transition-all cursor-pointer flex items-start gap-3.5 ${
                      isSelected
                        ? "bg-cyan-950/30 border-cyan-500/50 shadow-lg shadow-cyan-500/10"
                        : "bg-[#0B1220] border-slate-800 hover:border-slate-700 hover:bg-[#10192a]"
                    }`}
                  >
                    <div
                      className={`w-5 h-5 rounded-full border mt-0.5 flex items-center justify-center shrink-0 ${
                        isSelected
                          ? "border-cyan-400 bg-cyan-400 text-slate-950"
                          : "border-slate-600 bg-transparent"
                      }`}
                    >
                      {isSelected && <CheckCircle2 className="w-4 h-4 fill-slate-950" />}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-sm text-white">{lvl.title}</span>
                        <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-slate-800 text-slate-400">
                          {lvl.badge}
                        </span>
                      </div>
                      <p className="text-xs text-slate-400 mt-0.5">{lvl.desc}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Step 2: First Problem */}
        {step === 2 && (
          <div className="space-y-5 animate-in slide-in-from-right duration-200">
            <div>
              <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs font-semibold mb-2">
                <Code2 className="w-3.5 h-3.5" />
                <span>Recommended First Challenge</span>
              </div>
              <h2 id="onboarding-title" className="text-xl sm:text-2xl font-black text-white tracking-tight">
                Solve Your First Problem
              </h2>
              <p className="text-xs sm:text-sm text-slate-400 mt-1">
                Get hands-on in our Monaco code editor with real Judge0 feedback.
              </p>
            </div>

            <div className="p-4 sm:p-5 rounded-2xl bg-[#0B1220] border border-slate-800 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs uppercase font-mono tracking-wider text-cyan-400">
                  Targeted for: {selectedLevel.toUpperCase()}
                </span>
                <span className="text-xs font-semibold text-emerald-400">Sample + Hidden Tests</span>
              </div>
              <h3 className="text-base sm:text-lg font-bold text-white">
                {levelProblems[selectedLevel].title}
              </h3>
              <p className="text-xs text-slate-300">
                {levelProblems[selectedLevel].desc}
              </p>
              <div className="pt-2 flex flex-wrap gap-2 text-[11px] text-slate-400">
                <span className="px-2 py-0.5 rounded bg-slate-800/80 border border-slate-700/60">
                  Monaco Editor
                </span>
                <span className="px-2 py-0.5 rounded bg-slate-800/80 border border-slate-700/60">
                  Tiered Hints
                </span>
                <span className="px-2 py-0.5 rounded bg-slate-800/80 border border-slate-700/60">
                  Ctrl+Enter Shortcut
                </span>
              </div>
            </div>
          </div>
        )}

        {/* Step 3: Streak & Daily Routine */}
        {step === 3 && (
          <div className="space-y-5 animate-in slide-in-from-right duration-200">
            <div>
              <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-semibold mb-2">
                <Flame className="w-3.5 h-3.5 fill-amber-400" />
                <span>Consistency Over Cramming</span>
              </div>
              <h2 id="onboarding-title" className="text-xl sm:text-2xl font-black text-white tracking-tight">
                Build Your Daily Coding Streak
              </h2>
              <p className="text-xs sm:text-sm text-slate-400 mt-1">
                Submitting at least once a day in your timezone keeps your streak alive and unlocks XP badges.
              </p>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="p-3.5 rounded-2xl bg-[#0B1220] border border-slate-800 text-center space-y-1">
                <Flame className="w-7 h-7 text-amber-400 fill-amber-400 mx-auto" />
                <div className="text-base font-bold text-white">Daily Flame</div>
                <p className="text-[11px] text-slate-400">Calculated in your local timezone</p>
              </div>

              <div className="p-3.5 rounded-2xl bg-[#0B1220] border border-slate-800 text-center space-y-1">
                <Zap className="w-7 h-7 text-violet-400 fill-violet-400 mx-auto" />
                <div className="text-base font-bold text-white">XP Rewards</div>
                <p className="text-[11px] text-slate-400">Earn XP on first solve & streak milestones</p>
              </div>
            </div>

            <div className="p-3 rounded-xl bg-slate-800/40 border border-slate-700/50 text-xs text-slate-300">
              Tip: Press <kbd className="px-1.5 py-0.5 rounded bg-slate-900 border border-slate-700 font-mono text-[10px]">Ctrl+Enter</kbd> to run samples and <kbd className="px-1.5 py-0.5 rounded bg-slate-900 border border-slate-700 font-mono text-[10px]">Ctrl+Shift+Enter</kbd> to submit!
            </div>
          </div>
        )}

        {/* Footer Navigation Buttons */}
        <div className="mt-7 pt-4 border-t border-slate-800 flex items-center justify-between gap-3">
          <button
            onClick={handleDismiss}
            className="text-xs text-slate-400 hover:text-slate-200 transition-colors font-medium px-2 py-1"
          >
            Skip Intro
          </button>

          <Button
            onClick={handleNext}
            rightIcon={<ArrowRight className="w-4 h-4" />}
            className="px-5"
          >
            {step === 3 ? "Start Solving" : "Continue"}
          </Button>
        </div>
      </div>
    </div>
  );
}
