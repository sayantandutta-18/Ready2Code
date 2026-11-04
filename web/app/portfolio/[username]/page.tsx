"use client";

import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { fetchApi } from "@/lib/api";
import LoadingSkeleton from "@/components/ui/LoadingSkeleton";
import QueryErrorState from "@/components/ui/QueryErrorState";
import { User, Award, Flame, Zap, ShieldCheck, Trophy, ExternalLink, Code2, CheckCircle2, Github, Linkedin } from "lucide-react";
import TiltCard from "@/components/ui/TiltCard";
import dynamic from "next/dynamic";

const ActivityTower = dynamic(() => import("@/components/3d/ActivityTower"), { ssr: false });

interface SolvedStats {
  total: number;
  easy: number;
  medium: number;
  hard: number;
}

interface StreakInfo {
  current: number;
  longest: number;
  freezes_left: number;
}

interface UserProfile {
  id: string;
  username: string;
  display_name: string;
  avatar_url?: string | null;
  timezone?: string | null;
  solved: SolvedStats;
  streak: StreakInfo;
  xp: number;
  skills: Record<string, number>;
}

export default function PortfolioPage({ params }: { params: { username: string } }) {
  const username = params.username || "coder_alex";

  const {
    data: profile,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<UserProfile>({
    queryKey: ["portfolio-user", username],
    queryFn: () => fetchApi<UserProfile>(`/users/${username}`),
  });

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[#070D18] text-slate-100 py-10 px-4 md:px-8">
        <div className="max-w-5xl mx-auto space-y-8">
          <LoadingSkeleton variant="card" className="h-44" />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <LoadingSkeleton variant="card" className="h-48" />
            <LoadingSkeleton variant="card" className="h-48" />
            <LoadingSkeleton variant="card" className="h-48" />
          </div>
          <LoadingSkeleton variant="card" className="h-64" />
        </div>
      </div>
    );
  }

  if (isError || !profile) {
    return (
      <div className="min-h-screen bg-[#070D18] text-slate-100 py-10 px-4 md:px-8">
        <div className="max-w-5xl mx-auto">
          <QueryErrorState
            title="Portfolio Not Found"
            message={error instanceof Error ? error.message : "Unable to load candidate portfolio."}
            onRetry={() => refetch()}
          />
        </div>
      </div>
    );
  }

  const totalSolved = profile.solved?.total || 0;
  const easySolved = profile.solved?.easy || 0;
  const medSolved = profile.solved?.medium || 0;
  const hardSolved = profile.solved?.hard || 0;

  const easyPct = totalSolved > 0 ? (easySolved / totalSolved) * 100 : 0;
  const medPct = totalSolved > 0 ? (medSolved / totalSolved) * 100 : 0;
  const hardPct = totalSolved > 0 ? (hardSolved / totalSolved) * 100 : 0;

  return (
    <div className="min-h-screen bg-[#070D18] text-slate-100 py-10 px-4 md:px-8">
      <div className="max-w-5xl mx-auto space-y-8">
        {/* Top Profile Card */}
        <div className="rounded-2xl bg-gradient-to-r from-slate-900 via-[#0B1528] to-slate-900 border border-slate-800 p-8 shadow-2xl relative overflow-hidden">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6 relative z-10">
            <div className="flex flex-col md:flex-row items-center gap-5 text-center md:text-left">
              <div className="w-20 h-20 rounded-2xl bg-gradient-to-tr from-cyan-400 to-indigo-600 flex items-center justify-center font-black text-3xl text-slate-950 shadow-lg shadow-cyan-500/20">
                {profile.username.charAt(0).toUpperCase()}
              </div>
              <div className="space-y-1">
                <div className="flex items-center justify-center md:justify-start gap-2">
                  <h1 className="text-2xl font-black text-white">{profile.display_name || profile.username}</h1>
                  <span className="px-2.5 py-0.5 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-semibold flex items-center gap-1">
                    <ShieldCheck className="w-3.5 h-3.5" />
                    Verified Developer
                  </span>
                </div>
                <p className="text-xs text-slate-400">Competitive Programmer & Full-Stack Engineer</p>
                <div className="flex items-center justify-center md:justify-start gap-3 pt-2 text-slate-400 text-xs">
                  <span className="flex items-center gap-1 text-amber-400">
                    <Flame className="w-3.5 h-3.5 fill-amber-400" />
                    {profile.streak?.current || 0}-Day Streak
                  </span>
                  <span>•</span>
                  <span className="flex items-center gap-1 text-violet-400">
                    <Zap className="w-3.5 h-3.5 fill-violet-400" />
                    {1200 + (profile.xp || 0)} ELO Rating
                  </span>
                </div>
              </div>
            </div>

            {/* Direct Connect Buttons */}
            <div className="flex items-center gap-2">
              <a
                href="https://github.com"
                target="_blank"
                rel="noreferrer"
                className="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
                title="GitHub Profile"
              >
                <Github className="w-4 h-4" />
              </a>
              <a
                href="https://linkedin.com"
                target="_blank"
                rel="noreferrer"
                className="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
                title="LinkedIn Profile"
              >
                <Linkedin className="w-4 h-4" />
              </a>
              <Link
                href="/jobs"
                className="px-4 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-500 hover:from-cyan-600 hover:to-indigo-600 text-slate-950 font-bold text-xs uppercase tracking-wider shadow-lg shadow-cyan-500/20"
              >
                Fast-Track Referrals
              </Link>
            </div>
          </div>
        </div>

        {/* Problem Solved Stats & Distribution */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <TiltCard className="p-6 rounded-xl bg-slate-900/60 border border-slate-800 space-y-3">
            <div className="flex justify-between items-center text-xs text-slate-400">
              <span className="font-semibold uppercase tracking-wider">Total Solved</span>
              <span className="text-cyan-400 font-mono font-bold">{totalSolved} Problems</span>
            </div>
            <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden flex">
              <div className="bg-emerald-400 h-full transition-all" style={{ width: `${easyPct}%` }} title="Easy" />
              <div className="bg-amber-400 h-full transition-all" style={{ width: `${medPct}%` }} title="Medium" />
              <div className="bg-rose-500 h-full transition-all" style={{ width: `${hardPct}%` }} title="Hard" />
            </div>
            <div className="grid grid-cols-3 gap-2 pt-2 text-center text-xs">
              <div className="bg-slate-900/90 rounded-lg p-2">
                <div className="text-emerald-400 font-bold font-mono">{easySolved}</div>
                <div className="text-slate-500 text-[10px]">Easy</div>
              </div>
              <div className="bg-slate-900/90 rounded-lg p-2">
                <div className="text-amber-400 font-bold font-mono">{medSolved}</div>
                <div className="text-slate-500 text-[10px]">Medium</div>
              </div>
              <div className="bg-slate-900/90 rounded-lg p-2">
                <div className="text-rose-400 font-bold font-mono">{hardSolved}</div>
                <div className="text-slate-500 text-[10px]">Hard</div>
              </div>
            </div>
          </TiltCard>

          <TiltCard className="p-6 rounded-xl bg-slate-900/60 border border-slate-800 space-y-3">
            <div className="flex justify-between items-center text-xs text-slate-400">
              <span className="font-semibold uppercase tracking-wider">Skill Mastery</span>
              <span className="text-emerald-400 font-mono font-bold">Top Verified</span>
            </div>
            <div className="space-y-2 text-xs">
              {Object.keys(profile.skills || {}).length === 0 ? (
                <div className="text-slate-500 text-xs font-mono py-2">
                  Solve problems to showcase topic proficiencies.
                </div>
              ) : (
                Object.entries(profile.skills).slice(0, 3).map(([topic, count]) => (
                  <div key={topic}>
                    <div className="flex justify-between text-slate-300 mb-1">
                      <span>{topic}</span>
                      <span className="font-mono text-cyan-400">{count} solved</span>
                    </div>
                    <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                      <div className="bg-cyan-400 h-full" style={{ width: `${Math.min(100, count * 25)}%` }} />
                    </div>
                  </div>
                ))
              )}
            </div>
          </TiltCard>

          <TiltCard className="p-6 rounded-xl bg-slate-900/60 border border-slate-800 space-y-3">
            <div className="flex justify-between items-center text-xs text-slate-400">
              <span className="font-semibold uppercase tracking-wider">Verified Certificate</span>
              <Award className="w-4 h-4 text-amber-400" />
            </div>
            <div className="text-sm font-bold text-white">DSA Algorithmic Mastery</div>
            <p className="text-xs text-slate-400">Proctored assessment passed with score: 92/100</p>
            <Link
              href="/certificates/R2C-DSA-2026-X99"
              className="inline-flex items-center gap-1.5 text-xs text-cyan-400 hover:text-cyan-300 font-semibold pt-1"
            >
              <span>View On-Chain Certificate</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </Link>
          </TiltCard>
        </div>

        {/* 3D Activity Tower Heatmap */}
        <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Code2 className="w-4 h-4 text-cyan-400" />
              Annual Algorithmic Solve Activity
            </h2>
            <span className="text-xs font-mono text-slate-400">365 Days Activity Feed</span>
          </div>
          <div className="rounded-xl overflow-hidden">
            <ActivityTower
              streak={profile.streak?.current || 0}
              longestStreak={profile.streak?.longest || 0}
              solvedStats={profile.solved || { total: 0, easy: 0, medium: 0, hard: 0 }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
