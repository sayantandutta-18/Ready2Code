"use client";

import { useState } from "react";
import Link from "next/link";
import { ArrowLeft, CheckCircle2, Circle, Clock, Building2, BookOpen, Layers, Award } from "lucide-react";

export default function CompanyDetailPage({ params }: { params: { name: string } }) {
  const companyName = params.name.charAt(0).toUpperCase() + params.name.slice(1);
  const [completedDays, setCompletedDays] = useState<number[]>([1, 2, 3]);

  const toggleDay = (day: number) => {
    if (completedDays.includes(day)) {
      setCompletedDays(completedDays.filter((d) => d !== day));
    } else {
      setCompletedDays([...completedDays, day]);
    }
  };

  const schedule = [
    { day: 1, title: "Array Two-Pointers & Sliding Window", problems: ["two-sum", "container-with-most-water", "longest-substring-without-repeating-characters"] },
    { day: 2, title: "Stack & Monotonic Queue Patterns", problems: ["valid-parentheses", "min-stack", "daily-temperatures"] },
    { day: 3, title: "Linked List Reversals & Cycles", problems: ["reverse-linked-list", "merge-two-sorted-lists", "linked-list-cycle"] },
    { day: 4, title: "Binary Search Variations & Rotated Arrays", problems: ["binary-search", "search-in-rotated-sorted-array", "find-minimum-in-rotated-sorted-array"] },
    { day: 5, title: "Tree Traversals & Binary Search Trees", problems: ["maximum-depth-of-binary-tree", "validate-binary-search-tree", "invert-binary-tree"] },
    { day: 6, title: "Graph BFS / DFS & Grid Traversal", problems: ["number-of-islands", "rotting-oranges", "course-schedule"] },
    { day: 7, title: "Dynamic Programming 1D & 2D Foundations", problems: ["climbing-stairs", "coin-change", "longest-common-subsequence"] },
    { day: 8, title: "Intervals & Greedy Scheduling", problems: ["merge-intervals", "insert-interval", "non-overlapping-intervals"] }
  ];

  return (
    <div className="min-h-screen bg-[#070D18] text-slate-100 py-10 px-4 md:px-8">
      <div className="max-w-5xl mx-auto space-y-8">
        <Link
          href="/companies"
          className="inline-flex items-center gap-2 text-xs font-semibold text-slate-400 hover:text-cyan-400 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to All Companies
        </Link>

        {/* Company Header */}
        <div className="rounded-2xl bg-gradient-to-r from-cyan-950/40 to-slate-900 border border-cyan-500/30 p-8 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/20 text-cyan-300 text-xs font-mono font-bold">
              <Building2 className="w-3.5 h-3.5" />
              60-Day Interview Preparation Roadmap
            </div>
            <h1 className="text-3xl md:text-5xl font-black text-white">{companyName} Prep Track</h1>
            <p className="text-sm text-slate-300 max-w-xl">
              Targeted curriculum focusing on the exact algorithm patterns and difficulty tiers asked during {companyName} hiring drives.
            </p>
          </div>

          <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 text-center shrink-0 w-full md:w-56">
            <div className="text-xs text-slate-400">Roadmap Progress</div>
            <div className="text-3xl font-black text-cyan-400 font-mono mt-1">
              {Math.round((completedDays.length / schedule.length) * 100)}%
            </div>
            <div className="text-xs text-slate-500 mt-1">
              {completedDays.length} of {schedule.length} Milestones Cleared
            </div>
          </div>
        </div>

        {/* Hiring Rounds Breakdown */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6 space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Layers className="w-4 h-4 text-cyan-400" />
            Interview Evaluation Stages
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {[
              { round: "Round 1", title: "Online Assessment", time: "90 Mins", desc: "2-3 algorithmic problems with strict time limit and hidden edge cases." },
              { round: "Round 2", title: "Core Data Structures", time: "45 Mins", desc: "Live coding on trees, linked lists, and hash maps with emphasis on clean code." },
              { round: "Round 3", title: "Advanced Algorithms", time: "45 Mins", desc: "Graph traversals, dynamic programming, or shortest path optimizations." },
              { round: "Round 4", title: "Culture & Systems", time: "45 Mins", desc: "Behavioral deep dive, problem solving mindset, and situational judgement." }
            ].map((r, i) => (
              <div key={i} className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2">
                <div className="flex items-center justify-between text-xs text-cyan-400 font-mono">
                  <span>{r.round}</span>
                  <span className="text-slate-500">{r.time}</span>
                </div>
                <div className="text-sm font-bold text-slate-200">{r.title}</div>
                <p className="text-xs text-slate-400 leading-relaxed">{r.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Day-by-Day Checklist */}
        <div className="space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <BookOpen className="w-4 h-4 text-amber-400" />
            Day-by-Day Milestones
          </h2>

          <div className="space-y-3">
            {schedule.map((item) => {
              const isDone = completedDays.includes(item.day);
              return (
                <div
                  key={item.day}
                  className={`p-4 rounded-xl border transition-all flex flex-col md:flex-row items-start md:items-center justify-between gap-4 ${
                    isDone
                      ? "bg-emerald-950/15 border-emerald-500/30 text-emerald-200"
                      : "bg-slate-900/40 border-slate-800 text-slate-300"
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <button
                      onClick={() => toggleDay(item.day)}
                      className="text-slate-400 hover:text-emerald-400 transition-colors"
                    >
                      {isDone ? (
                        <CheckCircle2 className="w-5 h-5 text-emerald-400 fill-emerald-500/20" />
                      ) : (
                        <Circle className="w-5 h-5 text-slate-600" />
                      )}
                    </button>
                    <div>
                      <div className="text-xs font-mono text-slate-500">Day {item.day}</div>
                      <div className="font-bold text-sm text-slate-200">{item.title}</div>
                    </div>
                  </div>

                  {/* Problem links */}
                  <div className="flex flex-wrap items-center gap-2">
                    {item.problems.map((prob) => (
                      <Link
                        key={prob}
                        href={`/problems/${prob}`}
                        className="px-2.5 py-1 rounded-md bg-slate-800 hover:bg-cyan-500 hover:text-slate-950 text-slate-300 text-xs font-mono transition-colors"
                      >
                        {prob}
                      </Link>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
