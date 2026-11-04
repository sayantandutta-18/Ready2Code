"use client";

import { useState } from "react";
import Link from "next/link";
import { MessageSquareQuote, Building2, CheckCircle2, XCircle, Search, ThumbsUp, Calendar, ArrowRight } from "lucide-react";
import TiltCard from "@/components/ui/TiltCard";

const INTERVIEWS_DATA = [
  {
    id: "exp-1",
    author: "Rohan V.",
    company: "Google",
    role: "Software Engineer (L3)",
    date: "October 2026",
    verdict: "Offer",
    ctc: "₹45 LPA",
    difficulty: "Hard",
    rounds: [
      { name: "OA (Online Assessment)", desc: "2 graph questions involving Dijkstra and disjoint set union." },
      { name: "Technical Round 1", desc: "Sliding window maximum with monotonic deque + follow-up on 2D matrix." },
      { name: "Technical Round 2", desc: "Dynamic programming on trees with subtree memoization." },
      { name: "Googlyness", desc: "Hypothetical engineering conflict scenarios and cross-team communication." }
    ],
    advice: "Do not jump straight into coding. Talk out loud for the first 5 minutes to validate edge cases and explain time/space trade-offs."
  },
  {
    id: "exp-2",
    author: "Sneha M.",
    company: "Amazon",
    role: "SDE-1",
    date: "September 2026",
    verdict: "Offer",
    ctc: "₹34 LPA",
    difficulty: "Medium",
    rounds: [
      { name: "OA", desc: "Two Sum variant with stock profit optimization + debugging section." },
      { name: "Round 1 (DSA)", desc: "Lowest common ancestor in binary tree + Amazon LP Customer Obsession." },
      { name: "Round 2 (DSA)", desc: "Rotting Oranges multi-source BFS with edge cases." },
      { name: "Round 3 (Bar Raiser)", desc: "LRU Cache design and deep dive into 'Deliver Results' principle." }
    ],
    advice: "Prepare 2 real stories in STAR format (Situation, Task, Action, Result) for every Amazon Leadership Principle."
  },
  {
    id: "exp-3",
    author: "Arjun K.",
    company: "Microsoft",
    role: "Software Engineer",
    date: "August 2026",
    verdict: "Offer",
    ctc: "₹28 LPA",
    difficulty: "Medium",
    rounds: [
      { name: "Round 1", desc: "Reverse Linked List in K-groups + edge case discussion." },
      { name: "Round 2", desc: "Course Schedule topological sort (Kahn's algorithm)." },
      { name: "Round 3 (Director)", desc: "Project architecture deep dive and concurrency questions." }
    ],
    advice: "Focus on clean code, naming conventions, and handling null/empty pointer checks before the interviewer asks."
  },
  {
    id: "exp-4",
    author: "Pooja D.",
    company: "Uber",
    role: "Software Engineer 1",
    date: "November 2026",
    verdict: "Rejected",
    ctc: "₹42 LPA",
    difficulty: "Hard",
    rounds: [
      { name: "Round 1 (DSA)", desc: "Word Search II with Trie optimization. Got stuck on prefix pruning." },
      { name: "Round 2 (DSA)", desc: "Trapping Rain Water with two pointers. Passed all test cases." }
    ],
    advice: "Uber's algorithmic bar is high. Practice hard Trie and Backtracking problems under a strict 35-minute timer."
  }
];

export default function InterviewsPage() {
  const [selectedCompany, setSelectedCompany] = useState("All");
  const [selectedVerdict, setSelectedVerdict] = useState("All");

  const filtered = INTERVIEWS_DATA.filter((item) => {
    const matchesCompany = selectedCompany === "All" || item.company.toLowerCase() === selectedCompany.toLowerCase();
    const matchesVerdict = selectedVerdict === "All" || item.verdict.toLowerCase() === selectedVerdict.toLowerCase();
    return matchesCompany && matchesVerdict;
  });

  return (
    <div className="min-h-screen bg-[#070D18] text-slate-100 py-10 px-4 md:px-8">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <div className="space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-violet-500/10 border border-violet-500/30 text-violet-400 text-xs font-semibold">
            <MessageSquareQuote className="w-3.5 h-3.5" />
            Verified Community Interview Experiences
          </div>
          <h1 className="text-3xl md:text-4xl font-black tracking-tight text-white">
            Real Interview Debriefs & Compensation
          </h1>
          <p className="text-slate-400 text-sm md:text-base max-w-2xl">
            Browse real round-by-round interview breakdowns, questions asked, salary offers, and actionable tips from successful candidates.
          </p>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap items-center justify-between gap-4 bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex flex-wrap items-center gap-2 text-xs">
            <span className="text-slate-400 font-semibold mr-1">Company:</span>
            {["All", "Google", "Amazon", "Microsoft", "Uber"].map((c) => (
              <button
                key={c}
                onClick={() => setSelectedCompany(c)}
                className={`px-3 py-1 rounded-full transition-all ${
                  selectedCompany === c
                    ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-bold"
                    : "bg-slate-800/80 text-slate-400 hover:text-white"
                }`}
              >
                {c}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-2 text-xs">
            <span className="text-slate-400 font-semibold">Outcome:</span>
            {["All", "Offer", "Rejected"].map((v) => (
              <button
                key={v}
                onClick={() => setSelectedVerdict(v)}
                className={`px-3 py-1 rounded-full transition-all ${
                  selectedVerdict === v
                    ? "bg-violet-500/20 text-violet-300 border border-violet-500/40 font-bold"
                    : "bg-slate-800/80 text-slate-400 hover:text-white"
                }`}
              >
                {v}
              </button>
            ))}
          </div>
        </div>

        {/* Posts Grid */}
        <div className="space-y-6">
          {filtered.map((item) => (
            <div
              key={item.id}
              className="bg-slate-900/40 border border-slate-800 hover:border-slate-700 rounded-2xl p-6 space-y-5 transition-all shadow-lg"
            >
              {/* Header Info */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800/80 pb-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-400 to-indigo-500 flex items-center justify-center font-bold text-slate-950">
                    {item.company.charAt(0)}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h2 className="text-lg font-bold text-white">{item.company}</h2>
                      <span className="text-xs text-slate-400">• {item.role}</span>
                    </div>
                    <div className="text-xs text-slate-500 flex items-center gap-2 mt-0.5">
                      <span>By {item.author}</span>
                      <span>•</span>
                      <span>{item.date}</span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <span className="text-xs font-mono font-bold text-slate-300 bg-slate-800 px-2.5 py-1 rounded-md">
                    CTC: {item.ctc}
                  </span>
                  <span
                    className={`text-xs px-2.5 py-1 rounded-full font-bold flex items-center gap-1.5 ${
                      item.verdict === "Offer"
                        ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/30"
                        : "bg-rose-500/10 text-rose-400 border border-rose-500/30"
                    }`}
                  >
                    {item.verdict === "Offer" ? (
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    ) : (
                      <XCircle className="w-3.5 h-3.5 text-rose-400" />
                    )}
                    {item.verdict}
                  </span>
                </div>
              </div>

              {/* Rounds Breakdown */}
              <div className="space-y-3">
                <div className="text-xs font-mono uppercase tracking-wider text-slate-400 font-bold">
                  Interview Rounds Breakdown
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {item.rounds.map((round, idx) => (
                    <div key={idx} className="p-3 rounded-lg bg-slate-900/80 border border-slate-800/80 text-xs space-y-1">
                      <div className="font-semibold text-cyan-300">{round.name}</div>
                      <div className="text-slate-400">{round.desc}</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Candidate Advice */}
              <div className="bg-slate-950/60 rounded-xl p-4 border border-slate-800/60 text-xs text-slate-300">
                <span className="text-amber-400 font-bold">Key Tip: </span>
                {item.advice}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
