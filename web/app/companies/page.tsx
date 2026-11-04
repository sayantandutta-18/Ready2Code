"use client";

import React from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { Building2, ArrowRight } from "lucide-react";
import TiltCard from "../../components/ui/TiltCard";
import LoadingSkeleton from "../../components/ui/LoadingSkeleton";
import EmptyState from "../../components/ui/EmptyState";
import QueryErrorState from "../../components/ui/QueryErrorState";
import { fetchApi } from "../../lib/api";

interface CompanyItem {
  slug: string;
  name: string;
  tier: string;
  rounds: number;
  ctc: string;
  target_topics: string[];
  problem_count: number;
  description: string;
}

export default function CompaniesPage() {
  const {
    data: companies = [],
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<CompanyItem[]>({
    queryKey: ["companies"],
    queryFn: () => fetchApi<CompanyItem[]>("/companies"),
  });

  return (
    <div className="min-h-screen bg-[#070D18] text-slate-100 py-10 px-4 md:px-8">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <div className="space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-semibold">
            <Building2 className="w-3.5 h-3.5" />
            Company-Specific 60-Day Prep Tracks
          </div>
          <h1 className="text-3xl md:text-4xl font-black tracking-tight text-white">
            Target Your Dream Tech Company
          </h1>
          <p className="text-slate-400 text-sm md:text-base max-w-2xl">
            Curated high-frequency question archives, round-by-round interview breakdowns,
            and 60-day roadmaps reverse-engineered from verified campus and off-campus offers.
          </p>
        </div>

        {isError && (
          <QueryErrorState
            title="Could not load company tracks"
            message={error instanceof Error ? error.message : "Error contacting company catalog"}
            onRetry={() => refetch()}
          />
        )}

        {/* Company Grid */}
        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <LoadingSkeleton rows={4} className="h-56" />
            <LoadingSkeleton rows={4} className="h-56" />
            <LoadingSkeleton rows={4} className="h-56" />
          </div>
        ) : companies.length === 0 ? (
          <EmptyState
            title="No company roadmaps found"
            description="Company tracks are being synchronized."
          />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {companies.map((company) => (
              <TiltCard
                key={company.slug}
                className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-cyan-500/50 flex flex-col justify-between space-y-4 group transition-all"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h2 className="text-xl font-black text-white group-hover:text-cyan-300 transition-colors">
                      {company.name}
                    </h2>
                    <span className="text-[11px] px-2.5 py-1 rounded-full bg-slate-800 border border-slate-700 text-slate-300 font-mono">
                      {company.tier}
                    </span>
                  </div>

                  <p className="text-xs text-slate-300 leading-relaxed">
                    {company.description}
                  </p>

                  <div className="pt-2 border-t border-slate-800/80 space-y-1.5 text-xs">
                    <div className="flex justify-between text-slate-400">
                      <span>Average Package:</span>
                      <span className="font-semibold text-emerald-400 font-mono">{company.ctc}</span>
                    </div>
                    <div className="flex justify-between text-slate-400">
                      <span>Interview Stages:</span>
                      <span className="font-mono text-slate-200">{company.rounds} Rounds</span>
                    </div>
                  </div>

                  {/* Topics */}
                  <div className="flex flex-wrap gap-1.5 pt-1">
                    {company.target_topics?.map((topic, i) => (
                      <span
                        key={i}
                        className="text-[10px] px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-300 border border-cyan-500/20"
                      >
                        {topic}
                      </span>
                    ))}
                  </div>
                </div>

                <Link
                  href={`/companies/${company.slug}`}
                  className="w-full py-2.5 px-4 rounded-xl bg-slate-800 hover:bg-cyan-500 hover:text-slate-950 text-slate-200 text-xs font-bold uppercase tracking-wider flex items-center justify-center gap-2 transition-all mt-4"
                >
                  <span>View 60-Day Roadmap</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </TiltCard>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
