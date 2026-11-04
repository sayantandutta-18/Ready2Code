"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import ActivityTower from "../../../components/3d/ActivityTower";
import { User, Trophy, Zap, Flame, Award, CheckCircle2, Code2, Globe } from "lucide-react";

export default function ProfilePage({ params }: { params: { username: string } }) {
  const { username } = params;

  const [profile, setProfile] = useState<any>({
    username: username,
    display_name: "Alex Vance",
    solved: { total: 7, easy: 4, medium: 3, hard: 0 },
    streak: { current: 3, longest: 7, freezes_left: 2 },
    xp: 185,
    skills: {
      Arrays: 3,
      "Stack and Queue": 1,
      "Linked List": 1,
      "Binary Search": 1,
      Strings: 1,
    },
  });

  useEffect(() => {
    fetch(`/api/users/${username}`)
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (data) setProfile(data);
      })
      .catch(() => {});
  }, [username]);

  const badges = [
    { title: "First Blood", desc: "Solved first algorithmic problem", icon: "⚔️", unlocked: true },
    { title: "Streak Master", desc: "Maintained a 3-day solve streak", icon: "🔥", unlocked: true },
    { title: "Pointer Virtuoso", desc: "Mastered Two Pointers & Sliding Window", icon: "🎯", unlocked: true },
    { title: "Graph Explorer", desc: "Solved 5 graph traversal challenges", icon: "🌐", unlocked: false },
  ];

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
              Member of Ready2Code 3D DSA Arena &bull; UTC Timezone
            </p>
            <div className="flex items-center gap-4 mt-3 text-xs">
              <span className="flex items-center gap-1.5 text-amber-400 font-semibold">
                <Flame className="w-4 h-4 fill-amber-500" /> {profile.streak.current} Days Streak
              </span>
              <span className="flex items-center gap-1.5 text-violet-400 font-semibold">
                <Zap className="w-4 h-4 fill-violet-400" /> {profile.xp} Total XP
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

      {/* 365-Day Activity Tower Section (C1.9) */}
      <ActivityTower
        streak={profile.streak.current}
        longestStreak={profile.streak.longest}
        solvedStats={profile.solved}
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
            {Object.entries(profile.skills || {}).map(([topic, count]: [string, any]) => (
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
            ))}
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
                    : "bg-[#0B1220]/40 border-slate-850 text-slate-600 opacity-50"
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
