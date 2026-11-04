"use client";

import React, { useState } from "react";
import dynamic from "next/dynamic";
import Link from "next/link";
import { PlaySquare, Code2, Eye, HelpCircle } from "lucide-react";
import { TraceData } from "../../../components/3d/Visualizer3D";

// Lazy-load Visualizer3D with ssr: false
const Visualizer3D = dynamic(() => import("../../../components/3d/Visualizer3D"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-[450px] flex items-center justify-center text-slate-500 font-mono text-xs bg-[#0B1220] rounded-2xl border border-slate-800">
      Initializing 3D algorithm playback engine...
    </div>
  ),
});

const TWO_SUM_TRACE: TraceData = {
  algo: "two_sum",
  version: 1,
  scene: "array_with_map",
  input: { nums: [2, 7, 11, 15], target: 9 },
  frames: [
    {
      step: 0,
      array: [2, 7, 11, 15],
      pointers: { i: 0 },
      map: {},
      highlight: [0],
      note: "Initialize empty hash map. Start scanning from index 0 with value 2.",
    },
    {
      step: 1,
      array: [2, 7, 11, 15],
      pointers: { i: 0 },
      map: { "2": 0 },
      highlight: [0],
      note: "Target is 9. Required complement (9 - 2 = 7) is NOT in map. Store value 2 with index 0 in map.",
    },
    {
      step: 2,
      array: [2, 7, 11, 15],
      pointers: { i: 1 },
      map: { "2": 0 },
      highlight: [1],
      note: "Move pointer to index 1 (value 7). Calculate complement: target 9 - 7 = 2.",
    },
    {
      step: 3,
      array: [2, 7, 11, 15],
      pointers: { i: 1 },
      map: { "2": 0 },
      highlight: [0, 1],
      found: [0, 1],
      note: "Complement 2 is ALREADY in hash map at index 0! Return solution pair: [0, 1].",
    },
  ],
};

const BUBBLE_SORT_TRACE: TraceData = {
  algo: "bubble_sort",
  version: 1,
  scene: "array",
  input: { nums: [5, 3, 8, 4, 2] },
  frames: [
    {
      step: 0,
      array: [5, 3, 8, 4, 2],
      pointers: { j: 0 },
      highlight: [0, 1],
      note: "Compare index 0 (val: 5) and index 1 (val: 3). Since 5 > 3, perform 3D swap animation.",
    },
    {
      step: 1,
      array: [3, 5, 8, 4, 2],
      pointers: { j: 1 },
      highlight: [1, 2],
      note: "Compare index 1 (val: 5) and index 2 (val: 8). Since 5 <= 8, elements remain in place.",
    },
    {
      step: 2,
      array: [3, 5, 8, 4, 2],
      pointers: { j: 2 },
      highlight: [2, 3],
      note: "Compare index 2 (val: 8) and index 3 (val: 4). Since 8 > 4, swap them.",
    },
    {
      step: 3,
      array: [3, 5, 4, 8, 2],
      pointers: { j: 3 },
      highlight: [3, 4],
      note: "Compare index 3 (val: 8) and index 4 (val: 2). Since 8 > 2, swap them.",
    },
    {
      step: 4,
      array: [3, 5, 4, 2, 8],
      pointers: { j: 0 },
      highlight: [4],
      found: [4],
      note: "Pass complete. Element 8 has bubbled up to its correct sorted position at the end.",
    },
  ],
};

export default function VisualizerPage({ params }: { params: { algo: string } }) {
  const { algo } = params;
  const [selectedAlgo, setSelectedAlgo] = useState(algo === "bubble-sort" ? "bubble-sort" : "two-sum");

  const currentTrace = selectedAlgo === "bubble-sort" ? BUBBLE_SORT_TRACE : TWO_SUM_TRACE;

  return (
    <div className="max-w-6xl mx-auto px-4 lg:px-8 py-8 space-y-6">
      {/* Visualizer header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-black text-white tracking-tight flex items-center gap-3">
            <PlaySquare className="w-8 h-8 text-cyan-400" />
            <span>3D Algorithm Visualizer</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Frame-accurate 3D step-by-step playback with pointer markers and data structure telemetry.
          </p>
        </div>

        {/* Algorithm switcher */}
        <div className="flex items-center gap-2 bg-[#121C2F] p-1.5 rounded-xl border border-slate-800 text-xs">
          <button
            onClick={() => setSelectedAlgo("two-sum")}
            className={`px-3 py-1.5 rounded-lg font-medium transition-all ${
              selectedAlgo === "two-sum"
                ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/30"
                : "text-slate-400 hover:text-white"
            }`}
          >
            Two Sum (Hash Map)
          </button>
          <button
            onClick={() => setSelectedAlgo("bubble-sort")}
            className={`px-3 py-1.5 rounded-lg font-medium transition-all ${
              selectedAlgo === "bubble-sort"
                ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/30"
                : "text-slate-400 hover:text-white"
            }`}
          >
            Bubble Sort (Pillars)
          </button>
        </div>
      </div>

      {/* 3D Visualizer Component */}
      <Visualizer3D trace={currentTrace} />

      {/* Algorithm Reference Code Card */}
      <div className="p-6 rounded-2xl bg-[#121C2F] border border-slate-800 space-y-3 shadow-xl">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-bold text-slate-200 flex items-center gap-2">
            <Code2 className="w-4 h-4 text-cyan-400" />
            <span>Python Reference Trace Implementation</span>
          </h2>
          {selectedAlgo === "two-sum" && (
            <Link
              href="/problems/two-sum"
              className="text-xs text-cyan-400 hover:text-cyan-300 font-semibold"
            >
              Solve in Code Editor &rarr;
            </Link>
          )}
        </div>

        <pre className="p-4 rounded-xl bg-[#0B1220] border border-slate-800 text-xs text-slate-300 font-mono overflow-x-auto leading-relaxed">
          {selectedAlgo === "two-sum"
            ? `def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []`
            : `def bubble_sort(nums):
    n = len(nums)
    for i in range(n):
        for j in range(0, n - i - 1):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
    return nums`}
        </pre>
      </div>
    </div>
  );
}
