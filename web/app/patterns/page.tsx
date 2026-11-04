"use client";

import React from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { fetchApi } from "@/lib/api";
import LoadingSkeleton from "@/components/ui/LoadingSkeleton";
import QueryErrorState from "@/components/ui/QueryErrorState";
import EmptyState from "@/components/ui/EmptyState";
import TiltCard from "../../components/ui/TiltCard";
import { Sparkles, ChevronRight, BookOpen, Layers } from "lucide-react";

interface PatternItem {
  slug: string;
  name: string;
  order_index: number;
  signals: string;
}

export default function PatternsCatalogPage() {
  const {
    data: patterns = [],
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<PatternItem[]>({
    queryKey: ["patterns"],
    queryFn: () => fetchApi<PatternItem[]>("/patterns"),
  });

  return (
    <div className="max-w-7xl mx-auto px-4 lg:px-8 py-10 space-y-8">
      {/* Header */}
      <div className="space-y-2">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-xs font-semibold">
          <Sparkles className="w-4 h-4 text-cyan-400" />
          <span>Pattern-First Learning Engine</span>
        </div>
        <h1 className="text-3xl font-black text-white tracking-tight">Essential Algorithmic Patterns</h1>
        <p className="text-sm text-slate-400 max-w-2xl">
          Rather than memorizing thousands of isolated solutions, master the reusable patterns that
          underpin 95% of interview questions. Pass each pattern quiz to unlock its problem suite.
        </p>
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array.from({ length: 6 }).map((_, i) => (
            <LoadingSkeleton key={i} variant="card" className="h-52" />
          ))}
        </div>
      ) : isError ? (
        <QueryErrorState
          title="Failed to load patterns catalog"
          message={error instanceof Error ? error.message : "Unable to load algorithmic patterns."}
          onRetry={() => refetch()}
        />
      ) : patterns.length === 0 ? (
        <EmptyState
          title="No patterns available"
          description="Pattern lessons will be published shortly."
        />
      ) : (
        /* Patterns Grid */
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {patterns.map((p, idx) => (
            <Link key={p.slug} href={`/patterns/${p.slug}`} className="block">
              <TiltCard className="h-full flex flex-col justify-between space-y-4 hover:border-cyan-500/50">
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-mono uppercase tracking-wider text-cyan-400 px-2 py-0.5 rounded bg-cyan-950/60 border border-cyan-500/30">
                      Pattern #{p.order_index || idx + 1}
                    </span>
                    <span className="text-[11px] text-slate-500 font-mono">Quiz +15 XP</span>
                  </div>

                  <h3 className="text-lg font-bold text-white group-hover:text-cyan-300 transition-colors">
                    {p.name}
                  </h3>

                  <div>
                    <div className="text-[10px] uppercase font-mono tracking-wider text-slate-500 mb-1">
                      Problem Signals:
                    </div>
                    <p className="text-xs text-slate-300 leading-relaxed font-sans">{p.signals}</p>
                  </div>
                </div>

                <div className="pt-3 border-t border-slate-800 flex items-center justify-between text-xs font-bold text-cyan-400">
                  <span>Study Pattern & Take Quiz</span>
                  <ChevronRight className="w-4 h-4" />
                </div>
              </TiltCard>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
