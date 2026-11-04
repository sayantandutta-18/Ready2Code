"use client";

import React from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import TiltCard from "../../components/ui/TiltCard";
import LoadingSkeleton from "../../components/ui/LoadingSkeleton";
import EmptyState from "../../components/ui/EmptyState";
import QueryErrorState from "../../components/ui/QueryErrorState";
import { fetchApi } from "../../lib/api";
import { Trophy, Clock, Users, ArrowRight, Flame } from "lucide-react";

interface ContestItem {
  id: string;
  title: string;
  starts_at: string;
  duration_min: number;
  type: string;
  status: "live" | "upcoming" | "past";
  total_problems: number;
}

export default function ContestsPage() {
  const {
    data: contests = [],
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<ContestItem[]>({
    queryKey: ["contests"],
    queryFn: () => fetchApi<ContestItem[]>("/contests"),
  });

  const getStatusBadge = (status: string) => {
    if (status === "live") {
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-rose-500/15 border border-rose-500/30 text-rose-400 animate-pulse">
          <span className="w-2 h-2 rounded-full bg-rose-500" />
          <span>LIVE NOW</span>
        </span>
      );
    }
    if (status === "upcoming") {
      return (
        <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-cyan-500/15 border border-cyan-500/30 text-cyan-300">
          UPCOMING
        </span>
      );
    }
    return (
      <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-800 text-slate-400">
        ENDED
      </span>
    );
  };

  return (
    <div className="max-w-7xl mx-auto px-4 lg:px-8 py-10 space-y-10">
      {/* Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-black text-white tracking-tight flex items-center gap-3">
            <Trophy className="w-8 h-8 text-amber-400" />
            <span>Competitive Arena & Contests</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Timed 90-minute contests with Elo rating adjustments and live sub-minute standings.
          </p>
        </div>

        <Link
          href="/leaderboard"
          className="px-4 py-2 rounded-xl bg-[#121C2F] hover:bg-slate-800 border border-slate-700 text-xs font-semibold text-slate-200 transition-colors self-start sm:self-auto flex items-center gap-1.5"
        >
          <span>View Global Leaderboard</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>

      {isError && (
        <QueryErrorState
          title="Could not load contests"
          message={error instanceof Error ? error.message : "Unable to reach the contest server."}
          onRetry={() => refetch()}
        />
      )}

      {/* Contests Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <LoadingSkeleton rows={3} className="h-48" />
          <LoadingSkeleton rows={3} className="h-48" />
          <LoadingSkeleton rows={3} className="h-48" />
        </div>
      ) : contests.length === 0 ? (
        <EmptyState
          title="No scheduled contests"
          description="Check back soon for the next weekly competitive round."
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {contests.map((c) => (
            <Link key={c.id} href={`/contests/${c.id}`} className="block">
              <TiltCard className="h-full flex flex-col justify-between space-y-4 hover:border-cyan-500/50">
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400">
                      {c.type} Round
                    </span>
                    {getStatusBadge(c.status)}
                  </div>

                  <h3 className="text-lg font-bold text-white group-hover:text-cyan-300">
                    {c.title}
                  </h3>

                  <div className="space-y-1 text-xs text-slate-400 font-mono">
                    <div className="flex items-center gap-2">
                      <Clock className="w-3.5 h-3.5 text-slate-500" />
                      <span>Duration: {c.duration_min} minutes</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Users className="w-3.5 h-3.5 text-slate-500" />
                      <span>{c.total_problems} Algorithmic Challenges</span>
                    </div>
                  </div>
                </div>

                <div className="pt-3 border-t border-slate-800 flex items-center justify-between text-xs font-bold text-cyan-400">
                  <span>{c.status === "live" ? "Enter Arena" : "View Standings"}</span>
                  <ArrowRight className="w-4 h-4" />
                </div>
              </TiltCard>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
