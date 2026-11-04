"use client";

import React, { useState } from "react";
import dynamic from "next/dynamic";
import Link from "next/link";
import DifficultyChip from "../../components/ui/DifficultyChip";
import { Compass, BookOpen, ChevronRight, Lock, CheckCircle2 } from "lucide-react";
import { RoadmapTopic } from "../../components/3d/Roadmap3D";

// Lazy-load Roadmap3D with ssr: false (Section 4.6 requirement)
const Roadmap3D = dynamic(() => import("../../components/3d/Roadmap3D"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-[460px] flex items-center justify-center text-slate-500 font-mono text-sm bg-[#0B1220] rounded-2xl border border-slate-800">
      Rendering 3D topic spatial universe...
    </div>
  ),
});

const DEFAULT_TOPICS: RoadmapTopic[] = [
  { id: "1", slug: "arrays", name: "Arrays", totalProblems: 4, solvedCount: 3, order: 1 },
  { id: "2", slug: "strings", name: "Strings", totalProblems: 2, solvedCount: 1, order: 2 },
  { id: "3", slug: "linked-list", name: "Linked List", totalProblems: 2, solvedCount: 1, order: 3 },
  { id: "4", slug: "stack-and-queue", name: "Stack and Queue", totalProblems: 2, solvedCount: 1, order: 4 },
  { id: "5", slug: "trees", name: "Trees", totalProblems: 2, solvedCount: 0, order: 5 },
  { id: "6", slug: "graphs", name: "Graphs", totalProblems: 2, solvedCount: 0, order: 6 },
  { id: "7", slug: "dp", name: "Dynamic Programming", totalProblems: 3, solvedCount: 0, order: 7 },
];

const TOPIC_PROBLEMS: Record<string, any[]> = {
  arrays: [
    { slug: "two-sum", title: "Two Sum", difficulty: "easy", status: "solved" },
    { slug: "best-time-to-buy-and-sell-stock", title: "Best Time to Buy and Sell Stock", difficulty: "easy", status: "solved" },
    { slug: "maximum-subarray", title: "Maximum Subarray", difficulty: "medium", status: "solved" },
    { slug: "merge-intervals", title: "Merge Intervals", difficulty: "medium", status: "todo" },
  ],
  strings: [
    { slug: "longest-substring-without-repeating-characters", title: "Longest Substring Without Repeating Characters", difficulty: "medium", status: "solved" },
  ],
  "linked-list": [
    { slug: "reverse-linked-list", title: "Reverse Linked List", difficulty: "easy", status: "solved" },
  ],
  "stack-and-queue": [
    { slug: "valid-parentheses", title: "Valid Parentheses", difficulty: "easy", status: "solved" },
  ],
  trees: [
    { slug: "binary-tree-inorder-traversal", title: "Binary Tree Inorder Traversal", difficulty: "easy", status: "todo" },
  ],
  graphs: [
    { slug: "number-of-islands", title: "Number of Islands", difficulty: "medium", status: "todo" },
  ],
  dp: [
    { slug: "climbing-stairs", title: "Climbing Stairs", difficulty: "easy", status: "todo" },
    { slug: "coin-change", title: "Coin Change", difficulty: "medium", status: "todo" },
  ],
};

export default function RoadmapPage() {
  const [selectedTopic, setSelectedTopic] = useState<RoadmapTopic>(DEFAULT_TOPICS[0]);

  const activeProblems = TOPIC_PROBLEMS[selectedTopic.slug] || [];

  return (
    <div className="max-w-7xl mx-auto px-4 lg:px-8 py-8 space-y-8">
      {/* Title */}
      <div>
        <h1 className="text-3xl font-black text-white tracking-tight flex items-center gap-3">
          <Compass className="w-8 h-8 text-cyan-400" />
          <span>3D Topic Island Roadmap</span>
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Progress from foundational arrays through advanced graph theory and dynamic programming.
          Master 80% to unlock subsequent islands.
        </p>
      </div>

      {/* 3D Scene Platform */}
      <Roadmap3D
        topics={DEFAULT_TOPICS}
        onSelectTopic={(t) => setSelectedTopic(t)}
        selectedTopicSlug={selectedTopic.slug}
      />

      {/* Drawer showing problems for selected topic */}
      <div className="bg-[#121C2F] rounded-2xl border border-slate-800 p-6 shadow-2xl">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-4">
          <div className="flex items-center gap-3">
            <BookOpen className="w-5 h-5 text-cyan-400" />
            <h2 className="text-lg font-bold text-white">
              {selectedTopic.name} &bull; Practice Curriculum
            </h2>
          </div>
          <span className="text-xs text-slate-400 font-mono">
            {selectedTopic.solvedCount} of {selectedTopic.totalProblems} Solved
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {activeProblems.map((prob) => (
            <Link
              key={prob.slug}
              href={`/problems/${prob.slug}`}
              className="p-3.5 rounded-xl bg-[#0B1220] border border-slate-800/80 hover:border-cyan-500/40 flex items-center justify-between group transition-all"
            >
              <div className="flex items-center gap-3">
                {prob.status === "solved" ? (
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                ) : (
                  <span className="w-3.5 h-3.5 rounded-full border border-slate-600 block" />
                )}
                <div>
                  <div className="text-sm font-semibold text-slate-200 group-hover:text-cyan-300 transition-colors">
                    {prob.title}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <DifficultyChip difficulty={prob.difficulty} />
                <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-cyan-400 transition-colors" />
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
