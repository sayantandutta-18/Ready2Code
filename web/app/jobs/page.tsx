"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Briefcase, MapPin, Building2, CheckCircle2, ShieldCheck, Zap, ArrowRight, ExternalLink } from "lucide-react";
import LoadingSkeleton from "../../components/ui/LoadingSkeleton";
import EmptyState from "../../components/ui/EmptyState";
import QueryErrorState from "../../components/ui/QueryErrorState";
import { fetchApi } from "../../lib/api";

interface JobItem {
  id: string;
  company: string;
  role: string;
  location: string;
  ctc: string;
  min_elo: number;
  tags: string[];
  description: string;
}

export default function JobsPage() {
  const queryClient = useQueryClient();
  const [appliedJobs, setAppliedJobs] = useState<string[]>(() => {
    if (typeof window !== "undefined") {
      try {
        const saved = localStorage.getItem("ready2code_applied_jobs");
        if (saved) return JSON.parse(saved);
      } catch {}
    }
    return [];
  });
  const userElo = 1640;

  const {
    data: jobs = [],
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<JobItem[]>({
    queryKey: ["jobs"],
    queryFn: () => fetchApi<JobItem[]>("/jobs"),
  });

  const applyMutation = useMutation({
    mutationFn: (jobId: string) =>
      fetchApi(`/jobs/${jobId}/apply`, {
        method: "POST",
        body: JSON.stringify({
          user_id: "usr_alex",
          username: "coder_alex",
          elo: userElo,
          certificate_code: "R2C-DSA-2026-X99",
        }),
      }),
    onSuccess: (_, jobId) => {
      setAppliedJobs((prev) => {
        const next = [...prev, jobId];
        try {
          localStorage.setItem("ready2code_applied_jobs", JSON.stringify(next));
        } catch {}
        return next;
      });
    },
  });

  const handleApply = (jobId: string) => {
    if (!appliedJobs.includes(jobId)) {
      applyMutation.mutate(jobId);
    }
  };

  return (
    <div className="min-h-screen bg-[#070D18] text-slate-100 py-10 px-4 md:px-8">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <div className="space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold">
            <Briefcase className="w-3.5 h-3.5" />
            Verified Skill Hiring Board
          </div>
          <h1 className="text-3xl md:text-4xl font-black tracking-tight text-white">
            Skip the Resume Black Hole
          </h1>
          <p className="text-slate-400 text-sm md:text-base max-w-2xl">
            Top tech engineering teams hire directly through Ready2Code verified skill badges and Elo ratings.
            Fast-Track applications bypass HR screeners directly to the technical hiring manager.
          </p>
        </div>

        {/* User Verified Status Bar */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-cyan-500/20 text-cyan-400 flex items-center justify-center font-bold">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <div className="text-sm font-bold text-white flex items-center gap-2">
                Your Ready2Code Verified Profile
                <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono">Qualified for Most Roles</span>
              </div>
              <div className="text-xs text-slate-400">Competitive Rating: <strong className="text-amber-400 font-mono">1,640 ELO</strong> • Proctored: <strong>DSA Verified</strong></div>
            </div>
          </div>
          <Link
            href="/portfolio/coder_alex"
            className="text-xs text-cyan-400 hover:text-cyan-300 font-semibold flex items-center gap-1 self-start sm:self-auto"
          >
            <span>View Public Portfolio</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </Link>
        </div>

        {isError && (
          <QueryErrorState
            title="Could not load hiring board"
            message={error instanceof Error ? error.message : "Error contacting job listings server"}
            onRetry={() => refetch()}
          />
        )}

        {/* Job Listings Grid */}
        {isLoading ? (
          <div className="space-y-4">
            <LoadingSkeleton rows={4} className="h-44" />
            <LoadingSkeleton rows={4} className="h-44" />
          </div>
        ) : jobs.length === 0 ? (
          <EmptyState
            title="No active roles"
            description="Check back soon for upcoming hiring drives."
          />
        ) : (
          <div className="space-y-4">
            {jobs.map((job) => {
              const isQualified = userElo >= job.min_elo;
              const hasApplied = appliedJobs.includes(job.id);

              return (
                <div
                  key={job.id}
                  className="bg-slate-900/40 border border-slate-800 hover:border-slate-700 rounded-2xl p-6 transition-all shadow-md flex flex-col md:flex-row items-start md:items-center justify-between gap-6"
                >
                  <div className="space-y-3 flex-1">
                    <div className="flex flex-wrap items-center gap-3">
                      <h2 className="text-lg font-bold text-white">{job.role}</h2>
                      <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                        {job.company}
                      </span>
                      <span className="text-xs font-mono font-bold text-emerald-400 bg-emerald-500/10 px-2.5 py-0.5 rounded-md border border-emerald-500/20">
                        {job.ctc}
                      </span>
                    </div>

                    <p className="text-xs text-slate-400 leading-relaxed max-w-3xl">
                      {job.description}
                    </p>

                    <div className="flex flex-wrap items-center gap-4 text-xs text-slate-400">
                      <span className="flex items-center gap-1">
                        <MapPin className="w-3.5 h-3.5 text-slate-500" />
                        {job.location}
                      </span>
                      <span className="flex items-center gap-1 font-mono">
                        <Zap className="w-3.5 h-3.5 text-amber-400" />
                        Min. Required Rating: <strong className="text-slate-200">{job.min_elo} ELO</strong>
                      </span>
                    </div>

                    {/* Tags */}
                    <div className="flex flex-wrap gap-1.5 pt-1">
                      {job.tags?.map((t, idx) => (
                        <span
                          key={idx}
                          className="text-[10px] px-2 py-0.5 rounded bg-slate-800/80 text-slate-300 border border-slate-700/60 font-mono"
                        >
                          {t}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Apply Button Action */}
                  <div className="shrink-0 w-full md:w-auto">
                    {hasApplied ? (
                      <div className="flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold uppercase tracking-wider">
                        <CheckCircle2 className="w-4 h-4" />
                        Fast-Track Applied
                      </div>
                    ) : isQualified ? (
                      <button
                        type="button"
                        onClick={() => handleApply(job.id)}
                        disabled={applyMutation.isPending}
                        className="w-full md:w-auto px-6 py-3 rounded-xl bg-gradient-to-r from-cyan-400 to-indigo-500 hover:from-cyan-500 hover:to-indigo-600 text-slate-950 font-extrabold text-xs uppercase tracking-wider flex items-center justify-center gap-2 shadow-lg shadow-cyan-500/20 active:scale-95 transition-all disabled:opacity-50"
                      >
                        <span>{applyMutation.isPending ? "Applying..." : "1-Click Fast-Track Apply"}</span>
                        <ArrowRight className="w-3.5 h-3.5" />
                      </button>
                    ) : (
                      <div className="text-center px-4 py-2 rounded-xl bg-slate-800/60 border border-slate-700/50 text-[11px] text-slate-400 font-medium">
                        Requires {job.min_elo} ELO (+{job.min_elo - userElo} pts needed)
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
