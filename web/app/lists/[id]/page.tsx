"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import DifficultyChip from "../../../components/ui/DifficultyChip";
import { ListTodo, CheckCircle2, Circle, ArrowLeft, ChevronRight, GripVertical } from "lucide-react";

export default function ListDetailPage({ params }: { params: { id: string } }) {
  const { id } = params;

  const [listData, setListData] = useState<any>({
    name: "Blind 75 High-Frequency Core",
    description: "Essential foundational algorithmic patterns curated for top tech interviews.",
    total_problems: 8,
    solved_count: 5,
    progress_pct: 62.5,
    problems: [
      { id: "1", slug: "two-sum", title: "Two Sum", difficulty: "easy", topic: "Arrays", solved: true, position: 0 },
      { id: "2", slug: "valid-parentheses", title: "Valid Parentheses", difficulty: "easy", topic: "Stack", solved: true, position: 1 },
      { id: "3", slug: "best-time-to-buy-and-sell-stock", title: "Best Time to Buy and Sell Stock", difficulty: "easy", topic: "Arrays", solved: true, position: 2 },
      { id: "4", slug: "binary-search", title: "Binary Search", difficulty: "easy", topic: "Binary Search", solved: true, position: 3 },
      { id: "5", slug: "reverse-linked-list", title: "Reverse Linked List", difficulty: "easy", topic: "Linked List", solved: true, position: 4 },
      { id: "6", slug: "maximum-subarray", title: "Maximum Subarray", difficulty: "medium", topic: "Arrays", solved: false, position: 5 },
      { id: "7", slug: "climbing-stairs", title: "Climbing Stairs", difficulty: "easy", topic: "DP", solved: false, position: 6 },
      { id: "8", slug: "number-of-islands", title: "Number of Islands", difficulty: "medium", topic: "Graphs", solved: false, position: 7 },
    ],
  });

  useEffect(() => {
    fetch(`/api/lists/${id}`)
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (data && data.problems) setListData(data);
      })
      .catch(() => {});
  }, [id]);

  return (
    <div className="max-w-5xl mx-auto px-4 lg:px-8 py-10 space-y-8">
      {/* Back button */}
      <Link href="/lists" className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-cyan-400 font-mono">
        <ArrowLeft className="w-3.5 h-3.5" /> Back to Lists
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
      <div className="bg-[#121C2F] rounded-2xl border border-slate-800 overflow-hidden shadow-2xl">
        <div className="divide-y divide-slate-800/80">
          {listData.problems.map((p: any, index: number) => (
            <div
              key={p.slug}
              className="p-4 flex items-center justify-between hover:bg-slate-800/30 transition-colors group"
            >
              <div className="flex items-center gap-3">
                <GripVertical className="w-4 h-4 text-slate-600 cursor-grab" />
                {p.solved ? (
                  <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                ) : (
                  <Circle className="w-5 h-5 text-slate-600" />
                )}
                <div>
                  <Link
                    href={`/problems/${p.slug}`}
                    className="text-sm font-semibold text-slate-100 group-hover:text-cyan-300 transition-colors flex items-center gap-2"
                  >
                    <span className="text-slate-500 font-mono text-xs">{index + 1}.</span>
                    <span>{p.title}</span>
                  </Link>
                  <div className="text-[11px] text-slate-400 mt-0.5">Topic: {p.topic}</div>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <DifficultyChip difficulty={p.difficulty} />
                <Link
                  href={`/problems/${p.slug}`}
                  className="px-3 py-1 rounded-lg bg-slate-800 group-hover:bg-cyan-500/20 text-slate-300 group-hover:text-cyan-300 text-xs font-semibold transition-all flex items-center gap-1 border border-slate-700"
                >
                  <span>Solve</span>
                  <ChevronRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
