"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import dynamic from "next/dynamic";
import TiltCard from "../components/ui/TiltCard";
import DifficultyChip from "../components/ui/DifficultyChip";
import {
  Code,
  ArrowRight,
  Flame,
  Layers,
  Sparkles,
  Cpu,
  Trophy,
  CheckCircle,
  ExternalLink,
  UserPlus,
} from "lucide-react";

// Lazy-load HeroCube with ssr: false as required in C0.4
const HeroCube = dynamic(() => import("../components/3d/HeroCube"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-[360px] flex items-center justify-center text-slate-500 font-mono text-sm">
      Initializing 3D spatial canvas...
    </div>
  ),
});

export default function HomePage() {
  const [dailyProblem, setDailyProblem] = useState<any>({
    title: "Two Sum",
    slug: "two-sum",
    difficulty: "easy",
    topic: "Arrays",
  });

  useEffect(() => {
    fetch("/api/daily")
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (data && data.problem) {
          setDailyProblem(data.problem);
        }
      })
      .catch(() => {});
  }, []);

  return (
    <div className="relative overflow-hidden">
      {/* Background radial glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[450px] bg-gradient-to-b from-cyan-500/15 via-violet-500/10 to-transparent blur-3xl -z-10 pointer-events-none" />

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 lg:px-8 pt-12 pb-20">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          {/* Left Hero Content */}
          <div className="lg:col-span-7 flex flex-col gap-6 text-left">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-xs font-semibold w-fit">
              <Sparkles className="w-4 h-4 text-cyan-400" />
              <span>Next-Gen 3D Algorithm Mastery Platform</span>
            </div>

            <h1 className="text-4xl sm:text-6xl font-black tracking-tight leading-[1.1]">
              Master Algorithms in{" "}
              <span className="bg-gradient-to-r from-cyan-400 via-teal-300 to-indigo-400 bg-clip-text text-transparent">
                Three Dimensions
              </span>
            </h1>

            <p className="text-lg text-slate-300 max-w-2xl font-light leading-relaxed">
              Step beyond static code. Ready2Code pairs a sub-millisecond LeetCode-style judge
              with step-by-step 3D algorithm execution traces, Socratic AI guidance, and structured
              topic island progression.
            </p>

            <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 pt-2 w-full sm:w-auto">
              <Link
                href="/problems"
                className="min-h-[44px] px-6 py-3 rounded-xl bg-gradient-to-r from-cyan-400 to-cyan-500 hover:from-cyan-300 hover:to-cyan-400 text-slate-950 font-bold text-sm shadow-xl shadow-cyan-500/25 flex items-center justify-center gap-2 hover:scale-105 transition-all"
              >
                <span>Start Solving Free</span>
                <ArrowRight className="w-4 h-4" />
              </Link>

              <Link
                href="/roadmap"
                className="min-h-[44px] px-6 py-3 rounded-xl bg-[#121C2F] hover:bg-slate-800 border border-slate-700/80 text-slate-200 text-sm font-semibold flex items-center justify-center gap-2 transition-all hover:border-cyan-500/40"
              >
                <Layers className="w-4 h-4 text-cyan-400" />
                <span>Explore 3D Roadmap</span>
              </Link>
            </div>

            {/* Quick stats pills */}
            <div className="flex flex-wrap items-center gap-3 sm:gap-6 pt-4 text-xs font-medium text-slate-400">
              <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>12 Hand-Crafted Starter Problems</span>
              </div>
              <div className="flex items-center gap-2">
                <Cpu className="w-4 h-4 text-cyan-400 shrink-0" />
                <span>Judge0 Code Sandbox</span>
              </div>
            </div>
          </div>

          {/* Right Hero 3D Spatial Cube */}
          <div className="lg:col-span-5 relative flex flex-col items-center justify-center">
            <div className="w-full max-w-[420px] aspect-square relative rounded-3xl bg-gradient-to-b from-[#121C2F]/80 to-[#0B1220]/90 border border-slate-800 shadow-[0_20px_50px_rgba(0,0,0,0.6)] backdrop-blur-sm p-4 flex flex-col items-center justify-center">
              <div className="absolute top-3 right-3 text-[10px] uppercase tracking-wider font-mono px-2 py-0.5 rounded bg-cyan-950/60 border border-cyan-500/30 text-cyan-300">
                Interactive 3D Glass
              </div>
              <HeroCube />
              <p className="text-xs text-slate-400 text-center -mt-4">
                Drag to rotate &bull; Click to open starter problem
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Today's Daily Problem Teaser Banner */}
      <section className="max-w-7xl mx-auto px-4 lg:px-8 pb-16">
        <div className="p-6 rounded-2xl bg-gradient-to-r from-[#121C2F] via-[#16233B] to-[#121C2F] border border-cyan-500/30 flex flex-col md:flex-row items-center justify-between gap-6 shadow-2xl relative overflow-hidden">
          <div className="absolute -right-10 -bottom-10 w-48 h-48 bg-amber-500/10 blur-3xl pointer-events-none rounded-full" />

          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-amber-500/15 border border-amber-500/30 flex items-center justify-center text-amber-400">
              <Flame className="w-6 h-6 fill-amber-500" />
            </div>
            <div>
              <div className="text-xs font-semibold text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
                <span>Daily Challenge</span>
                <span className="text-slate-500">&bull;</span>
                <span className="text-slate-400 font-mono">Streak +5 XP</span>
              </div>
              <div className="text-xl font-bold text-white mt-0.5 flex items-center gap-3">
                <span>{dailyProblem.title}</span>
                <DifficultyChip difficulty={dailyProblem.difficulty} />
              </div>
              <div className="text-xs text-slate-400 mt-1">Topic: {dailyProblem.topic}</div>
            </div>
          </div>

          <Link
            href={`/problems/${dailyProblem.slug}`}
            className="min-h-[44px] w-full sm:w-auto px-5 py-2.5 rounded-xl bg-cyan-400 hover:bg-cyan-300 text-slate-950 font-bold text-sm shadow-md shadow-cyan-500/20 flex items-center justify-center gap-2 transition-all shrink-0"
          >
            <span>Solve Today's Problem</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </section>

      {/* Feature Catalog Grid with 3D Tilt Cards */}
      <section className="max-w-7xl mx-auto px-4 lg:px-8 py-12">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Designed for Modern Engineers
          </h2>
          <p className="text-slate-400 text-sm mt-2">
            Every feature engineered to build intuitive mental models of data structures.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <TiltCard className="flex flex-col gap-3">
            <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
              <Layers className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-slate-100">3D Step-by-Step Visualizer</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Watch arrays transform into 3D pillars, hash maps manifest as spatial panels, and
              pointers step synchronously with playback and scrubbing controls.
            </p>
            <Link
              href="/visualizer/two-sum"
              className="text-xs font-semibold text-cyan-400 hover:text-cyan-300 flex items-center gap-1 mt-auto pt-2"
            >
              <span>Launch Visualizer</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </Link>
          </TiltCard>

          <TiltCard className="flex flex-col gap-3">
            <div className="w-10 h-10 rounded-xl bg-violet-500/10 border border-violet-500/30 flex items-center justify-center text-violet-400">
              <Sparkles className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-slate-100">Socratic AI Assistant</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Never get answers spoiled. Three tiered hints provide gentle conceptual cues, pattern
              recognition, and data structure nudges at calibrated XP costs.
            </p>
            <Link
              href="/problems/two-sum"
              className="text-xs font-semibold text-violet-400 hover:text-violet-300 flex items-center gap-1 mt-auto pt-2"
            >
              <span>Try Socratic Hints</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </Link>
          </TiltCard>

          <TiltCard className="flex flex-col gap-3">
            <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400">
              <Trophy className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-slate-100">3D Topic Islands Roadmap</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Ascend through Arrays, Strings, Linked Lists, Trees, Graphs, and Dynamic Programming.
              Unlock subsequent islands by mastering 80% of prior foundations.
            </p>
            <Link
              href="/roadmap"
              className="text-xs font-semibold text-amber-400 hover:text-amber-300 flex items-center gap-1 mt-auto pt-2"
            >
              <span>View Topic Map</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </Link>
          </TiltCard>
        </div>

        {/* Call to Action: Sign Up & Sign In */}
        <div className="mt-16 rounded-3xl bg-gradient-to-r from-cyan-950/60 via-slate-900 to-indigo-950/60 border border-cyan-500/30 p-8 sm:p-12 text-center relative overflow-hidden shadow-2xl">
          <div className="absolute top-0 right-0 -mt-12 -mr-12 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />
          <div className="absolute bottom-0 left-0 -mb-12 -ml-12 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

          <div className="relative z-10 max-w-2xl mx-auto flex flex-col items-center">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-xs font-mono uppercase tracking-wider mb-4">
              <Sparkles className="w-3.5 h-3.5" />
              Join 1,000+ Placement Aspirants
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight mb-3">
              Ready to Master Algorithms in 3D?
            </h2>
            <p className="text-slate-300 text-sm sm:text-base leading-relaxed mb-8">
              Create your account in seconds to save your code drafts, earn streak freezes, and prepare for placement rounds with 100+ curated problems.
            </p>

            <div className="flex flex-col sm:flex-row items-center gap-4 w-full sm:w-auto">
              <Link
                href="/register"
                className="w-full sm:w-auto px-7 py-3 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-500 hover:from-cyan-400 hover:to-indigo-400 text-slate-950 font-bold text-sm shadow-xl shadow-cyan-500/25 transition-all flex items-center justify-center gap-2 group cursor-pointer"
              >
                <UserPlus className="w-4 h-4" />
                <span>Create Free Account</span>
                <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
              </Link>
              <Link
                href="/login"
                className="w-full sm:w-auto px-6 py-3 rounded-xl bg-slate-800/80 hover:bg-slate-800 border border-slate-700 text-slate-200 hover:text-white font-medium text-sm transition-colors text-center"
              >
                Sign In to Existing Account
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
