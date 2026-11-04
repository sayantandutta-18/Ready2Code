"use client";

import React from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { fetchApi } from "@/lib/api";
import LoadingSkeleton from "@/components/ui/LoadingSkeleton";
import QueryErrorState from "@/components/ui/QueryErrorState";
import ActivityTower from "../../../components/3d/ActivityTower";
import { User, Trophy, Zap, Flame, Award, CheckCircle2, Code2 } from "lucide-react";

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

export default function ProfilePage({ params }: { params: { username: string } }) {
  const { username } = params;

  const {
    data: profile,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<UserProfile>({
    queryKey: ["user-profile", username],
    queryFn: () => fetchApi<UserProfile>(`/users/${username}`),
  });

  const badges = [
    { title: "First Blood", desc: "Solved first algorithmic problem", icon: "⚔️", unlocked: (profile?.solved?.total || 0) >= 1 },
    { title: "Streak Master", desc: "Maintained a 3-day solve streak", icon: "🔥", unlocked: (profile?.streak?.current || 0) >= 3 },
    { title: "Pointer Virtuoso", desc: "Mastered Two Pointers & Sliding Window", icon: "🎯", unlocked: (profile?.skills?.["Arrays"] || 0) >= 2 },
    { title: "Graph Explorer", desc: "Solved 5 graph traversal challenges", icon: "🌐", unlocked: (profile?.skills?.["Graphs"] || 0) >= 5 },
  ];

  if (isLoading) {
    return (
      <div className="max-w-6xl mx-auto px-4 lg:px-8 py-10 space-y-6">
        <LoadingSkeleton variant="card" className="h-44" />
        <LoadingSkeleton variant="card" className="h-64" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <LoadingSkeleton variant="card" className="h-48" />
          <LoadingSkeleton variant="card" className="h-48" />
        </div>
      </div>
    );
  }

  if (isError || !profile) {
    return (
      <div className="max-w-6xl mx-auto px-4 lg:px-8 py-10">
        <QueryErrorState
          title="User profile not found"
          message={error instanceof Error ? error.message : "Unable to load profile data for this user."}
          onRetry={() => refetch()}
        />
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 lg:px-8 py-10 space-y-8">
      {/* Header Profile Card */}
      <div className="p-8 rounded-3xl bg-[#121C2F] border border-slate-800 shadow-2xl flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="flex items-center gap-5">
          <div className="w-20 h-20 rounded-2xl bg-gradient-to-tr from-cyan-400 to-indigo-600 flex items-center justify-center font-extrabold text-2xl text-slate-950 shadow-xl shadow-cyan-500/20">
            {profile.username[0]?.toUpperCase() || "A"}
          </div>
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-black text-white">{profile.display_name || profile.username}</h1>
              <span className="text-xs font-mono text-cyan-400 px-2 py-0.5 rounded bg-cyan-950/60 border border-cyan-500/30">
                @{profile.username}
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Member of Ready2Code 3D DSA Arena &bull; {profile.timezone || "UTC"} Timezone
            </p>
            <div className="flex items-center gap-4 mt-3 text-xs">
              <span className="flex items-center gap-1.5 text-amber-400 font-semibold">
                <Flame className="w-4 h-4 fill-amber-500" /> {profile.streak?.current || 0} Days Streak
              </span>
              <span className="flex items-center gap-1.5 text-violet-400 font-semibold">
                <Zap className="w-4 h-4 fill-violet-400" /> {profile.xp || 0} Total XP
              </span>
            </div>
          </div>
        </div>

        <Link
          href="/settings"
          className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs font-semibold text-slate-200 transition-colors"
        >
          Edit Profile
        </Link>
      </div>

      {/* 365-Day Activity Tower Section */}
      <ActivityTower
        streak={profile.streak?.current || 0}
        longestStreak={profile.streak?.longest || 0}
        solvedStats={profile.solved || { total: 0, easy: 0, medium: 0, hard: 0 }}
      />

      {/* Skills Breakdown & Badges */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Skills Radar / Breakdown */}
        <div className="p-6 rounded-2xl bg-[#121C2F] border border-slate-800 shadow-xl space-y-4">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
            <Code2 className="w-4 h-4 text-cyan-400" />
            <span>Topic Mastery Breakdown</span>
          </h2>

          <div className="space-y-3">
            {Object.keys(profile.skills || {}).length === 0 ? (
              <div className="p-6 text-center text-xs text-slate-500 font-mono">
                Solve problems to see topic breakdown analytics.
              </div>
            ) : (
              Object.entries(profile.skills).map(([topic, count]) => (
                <div key={topic} className="space-y-1">
                  <div className="flex justify-between text-xs text-slate-300">
                    <span>{topic}</span>
                    <span className="font-mono text-cyan-400 font-semibold">{count} Solved</span>
                  </div>
                  <div className="w-full h-2 rounded-full bg-slate-900 overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-cyan-400 to-indigo-500 rounded-full"
                      style={{ width: `${Math.min(100, count * 25)}%` }}
                    />
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Badges Cabinet */}
        <div className="p-6 rounded-2xl bg-[#121C2F] border border-slate-800 shadow-xl space-y-4">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
            <Award className="w-4 h-4 text-violet-400" />
            <span>Earned Achievements</span>
          </h2>

          <div className="grid grid-cols-2 gap-3">
            {badges.map((b) => (
              <div
                key={b.title}
                className={`p-3.5 rounded-xl border flex items-center gap-3 ${
                  b.unlocked
                    ? "bg-[#0B1220] border-slate-700/80 text-slate-200"
                    : "bg-[#0B1220]/40 border-slate-800 text-slate-600 opacity-50"
                }`}
              >
                <div className="text-2xl">{b.icon}</div>
                <div>
                  <div className="text-xs font-bold">{b.title}</div>
                  <div className="text-[10px] text-slate-400">{b.desc}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
