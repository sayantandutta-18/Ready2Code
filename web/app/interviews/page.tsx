"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { MessageSquareQuote, CheckCircle2, XCircle } from "lucide-react";
import LoadingSkeleton from "../../components/ui/LoadingSkeleton";
import EmptyState from "../../components/ui/EmptyState";
import QueryErrorState from "../../components/ui/QueryErrorState";
import { fetchApi } from "../../lib/api";

interface InterviewRound {
  name: string;
  desc: string;
}

interface InterviewItem {
  id: string;
  author: string;
  company: string;
  role: string;
  date: string;
  verdict: "Offer" | "Rejected" | string;
  ctc: string;
  difficulty: "Easy" | "Medium" | "Hard" | string;
  rounds: InterviewRound[];
  advice: string;
}

export default function InterviewsPage() {
  const [selectedCompany, setSelectedCompany] = useState("All");
  const [selectedVerdict, setSelectedVerdict] = useState("All");

  const {
    data: interviews = [],
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<InterviewItem[]>({
    queryKey: ["interviews", { company: selectedCompany, verdict: selectedVerdict }],
    queryFn: () => {
      const params = new URLSearchParams();
      if (selectedCompany !== "All") params.set("company", selectedCompany);
      if (selectedVerdict !== "All") params.set("verdict", selectedVerdict);
      const queryStr = params.toString();
      return fetchApi<InterviewItem[]>(`/interviews${queryStr ? `?${queryStr}` : ""}`);
    },
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
                type="button"
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
                type="button"
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

        {isError && (
          <QueryErrorState
            title="Could not load interview debriefs"
            message={error instanceof Error ? error.message : "Error contacting interview archive"}
            onRetry={() => refetch()}
          />
        )}

        {/* Posts Grid */}
        {isLoading ? (
          <div className="space-y-4">
            <LoadingSkeleton rows={4} className="h-44" />
            <LoadingSkeleton rows={4} className="h-44" />
          </div>
        ) : interviews.length === 0 ? (
          <EmptyState
            title="No interview experiences found"
            description="No community debriefs match your selected filters. Try choosing 'All' companies and outcomes."
            actionText="Reset filters"
            onAction={() => {
              setSelectedCompany("All");
              setSelectedVerdict("All");
            }}
          />
        ) : (
          <div className="space-y-6">
            {interviews.map((item) => (
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
                    {item.rounds?.map((round, idx) => (
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
        )}
      </div>
    </div>
  );
}
