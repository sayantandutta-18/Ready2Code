"use client";

import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import LoadingSkeleton from "../../components/ui/LoadingSkeleton";
import EmptyState from "../../components/ui/EmptyState";
import QueryErrorState from "../../components/ui/QueryErrorState";
import { fetchApi } from "../../lib/api";
import {
  GraduationCap,
  Building2,
  Cpu,
  FileText,
  Clock,
  Languages,
  ChevronDown,
  ChevronUp,
} from "lucide-react";

interface PlacementQuestion {
  id: string;
  title: string;
  question: string;
  answer: string;
  full_answer_md?: string;
}

export default function PlacementPrepPage() {
  const [activeTrack, setActiveTrack] = useState<string>("cs_core");
  const [lang, setLang] = useState<"en" | "hi" | "bn">("en");
  const [expandedId, setExpandedId] = useState<string | null>("os-1");

  const tracks = [
    { id: "cs_core", name: "CS Fundamentals Core", icon: Cpu, desc: "OS, DBMS, Networks, OOP" },
    { id: "aptitude", name: "Company Aptitude Tests", icon: Clock, desc: "TCS NQT, Infosys, Wipro, Cognizant" },
    { id: "product_dsa", name: "Product Company Tracks", icon: Building2, desc: "Google, Amazon, Meta, Uber" },
    { id: "resume_prep", name: "ATS Resume & STAR Guide", icon: FileText, desc: "Interview formulas & project framing" },
  ];

  const {
    data: questions = [],
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<PlacementQuestion[]>({
    queryKey: ["placement-questions", { track: activeTrack, lang }],
    queryFn: () => fetchApi<PlacementQuestion[]>(`/placement/questions?track=${activeTrack}&lang=${lang}`),
  });

  return (
    <div className="max-w-6xl mx-auto px-4 lg:px-8 py-10 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-semibold mb-2">
            <GraduationCap className="w-4 h-4 text-emerald-400" />
            <span>Placement Prep & Regional Explanations</span>
          </div>
          <h1 className="text-3xl font-black text-white tracking-tight">Campus & Career Placement Hub</h1>
          <p className="text-sm text-slate-400 mt-1 max-w-xl">
            Complete tracks covering Indian campus recruiters, product engineering rounds, and core
            CS fundamentals with bilingual summaries.
          </p>
        </div>

        {/* Regional Language Toggle (C3.10 requirement: English, Hindi, Bengali) */}
        <div className="flex items-center gap-2 bg-[#121C2F] p-1.5 rounded-xl border border-slate-800 text-xs self-start sm:self-auto">
          <Languages className="w-4 h-4 text-cyan-400 ml-1.5" />
          <button
            type="button"
            onClick={() => setLang("en")}
            className={`px-3 py-1 rounded-lg font-medium transition-all ${
              lang === "en"
                ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/30"
                : "text-slate-400 hover:text-white"
            }`}
          >
            English
          </button>
          <button
            type="button"
            onClick={() => setLang("hi")}
            className={`px-3 py-1 rounded-lg font-medium transition-all ${
              lang === "hi"
                ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/30"
                : "text-slate-400 hover:text-white"
            }`}
          >
            हिंदी
          </button>
          <button
            type="button"
            onClick={() => setLang("bn")}
            className={`px-3 py-1 rounded-lg font-medium transition-all ${
              lang === "bn"
                ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/30"
                : "text-slate-400 hover:text-white"
            }`}
          >
            বাংলা
          </button>
        </div>
      </div>

      {/* Track Selector Bar */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {tracks.map((t) => {
          const Icon = t.icon;
          const isSelected = activeTrack === t.id;
          return (
            <button
              key={t.id}
              type="button"
              onClick={() => setActiveTrack(t.id)}
              className={`p-4 rounded-2xl border text-left transition-all ${
                isSelected
                  ? "bg-cyan-500/10 border-cyan-400 shadow-lg shadow-cyan-500/10 text-cyan-300 ring-1 ring-cyan-400/50"
                  : "bg-[#121C2F] border-slate-800 text-slate-300 hover:border-slate-700"
              }`}
            >
              <Icon className={`w-5 h-5 mb-2 ${isSelected ? "text-cyan-400" : "text-slate-400"}`} />
              <div className="text-xs font-bold text-white">{t.name}</div>
              <div className="text-[10px] text-slate-400 mt-0.5">{t.desc}</div>
            </button>
          );
        })}
      </div>

      {isError && (
        <QueryErrorState
          title="Could not load questions"
          message={error instanceof Error ? error.message : "Error contacting placement question bank"}
          onRetry={() => refetch()}
        />
      )}

      {/* Questions Accordion List */}
      <div className="bg-[#121C2F] rounded-2xl border border-slate-800 p-6 space-y-4 shadow-xl">
        <h2 className="text-base font-bold text-white">Interview Questions & Explanations</h2>

        {isLoading ? (
          <LoadingSkeleton rows={4} className="h-28" />
        ) : questions.length === 0 ? (
          <EmptyState
            title="No questions in this track"
            description="Select another placement track to explore questions."
          />
        ) : (
          <div className="space-y-3">
            {questions.map((q) => {
              const isExpanded = expandedId === q.id;
              return (
                <div
                  key={q.id}
                  className="rounded-xl border border-slate-800 bg-[#0B1220] overflow-hidden transition-all"
                >
                  <button
                    type="button"
                    onClick={() => setExpandedId(isExpanded ? null : q.id)}
                    className="w-full p-4 text-left flex items-center justify-between text-sm font-semibold text-slate-200 hover:text-cyan-300"
                  >
                    <span>{q.title}</span>
                    {isExpanded ? (
                      <ChevronUp className="w-4 h-4 text-slate-400" />
                    ) : (
                      <ChevronDown className="w-4 h-4 text-slate-400" />
                    )}
                  </button>

                  {isExpanded && (
                    <div className="px-4 pb-4 pt-1 border-t border-slate-800/80 space-y-3 text-xs">
                      <p className="text-slate-400 font-sans italic">{q.question}</p>
                      <div className="p-3 rounded-lg bg-[#121C2F] border border-cyan-500/20 text-slate-200 leading-relaxed font-sans">
                        <div className="text-[10px] uppercase font-mono font-bold text-cyan-400 mb-1">
                          Explanation ({lang === "hi" ? "हिंदी" : lang === "bn" ? "বাংলা" : "English"}):
                        </div>
                        {q.answer}
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
