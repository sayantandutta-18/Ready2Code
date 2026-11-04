"use client";

import React, { useState } from "react";
import VerdictBadge from "./VerdictBadge";
import { Check, X, AlertCircle } from "lucide-react";

export interface TestCaseResult {
  test_index: number;
  input: string;
  expected_output: string;
  actual_output?: string;
  stderr?: string;
  verdict: string;
  status_description: string;
  runtime_ms: number;
  passed: boolean;
}

interface TestCaseTableProps {
  results: TestCaseResult[];
  overallStatus?: string;
}

export default function TestCaseTable({ results, overallStatus }: TestCaseTableProps) {
  const [activeTab, setActiveTab] = useState(0);

  if (!results || results.length === 0) {
    return (
      <div className="p-6 text-center text-slate-500 bg-[#121C2F]/50 rounded-xl border border-slate-800">
        Run code on sample test cases to view execution outputs.
      </div>
    );
  }

  const current = results[activeTab] || results[0];

  return (
    <div className="bg-[#121C2F] rounded-xl border border-slate-800 overflow-hidden flex flex-col">
      {/* Header bar with tabs */}
      <div className="flex items-center justify-between px-4 py-2.5 bg-[#0e1626] border-b border-slate-800">
        <div className="flex items-center gap-2 overflow-x-auto">
          {results.map((r, i) => (
            <button
              key={i}
              onClick={() => setActiveTab(i)}
              className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-medium transition-all ${
                activeTab === i
                  ? "bg-slate-800 text-cyan-300 border border-cyan-500/30"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-850"
              }`}
            >
              {r.passed ? (
                <Check className="w-3.5 h-3.5 text-emerald-400" />
              ) : (
                <X className="w-3.5 h-3.5 text-rose-400" />
              )}
              <span>Case {i + 1}</span>
            </button>
          ))}
        </div>

        <div className="flex items-center gap-3">
          <span className="text-xs text-slate-400">
            {results.filter((r) => r.passed).length}/{results.length} Passed
          </span>
          <VerdictBadge verdict={overallStatus === "Accepted" ? "AC" : current.verdict} size="sm" />
        </div>
      </div>

      {/* Detail viewer */}
      <div className="p-4 space-y-3 font-mono text-xs">
        <div>
          <div className="text-[11px] uppercase tracking-wider text-slate-400 mb-1">Input:</div>
          <pre className="p-2.5 rounded-lg bg-[#0B1220] border border-slate-800/80 text-slate-200 overflow-x-auto whitespace-pre-wrap">
            {current.input}
          </pre>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div>
            <div className="text-[11px] uppercase tracking-wider text-slate-400 mb-1">Expected Output:</div>
            <pre className="p-2.5 rounded-lg bg-[#0B1220] border border-slate-800/80 text-emerald-400 overflow-x-auto whitespace-pre-wrap">
              {current.expected_output}
            </pre>
          </div>
          <div>
            <div className="text-[11px] uppercase tracking-wider text-slate-400 mb-1">Actual Output:</div>
            <pre
              className={`p-2.5 rounded-lg bg-[#0B1220] border overflow-x-auto whitespace-pre-wrap ${
                current.passed
                  ? "border-emerald-500/30 text-emerald-300"
                  : "border-rose-500/30 text-rose-300"
              }`}
            >
              {current.actual_output || (current.passed ? current.expected_output : "<no output>")}
            </pre>
          </div>
        </div>

        {current.stderr && (
          <div>
            <div className="text-[11px] uppercase tracking-wider text-rose-400 flex items-center gap-1 mb-1">
              <AlertCircle className="w-3.5 h-3.5" /> Error Log / Stderr:
            </div>
            <pre className="p-2.5 rounded-lg bg-rose-950/20 border border-rose-500/30 text-rose-300 overflow-x-auto whitespace-pre-wrap">
              {current.stderr}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
