"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Swords, Zap, Trophy, Shield, Flame, Play, Timer, Sparkles, Users } from "lucide-react";
import TiltCard from "@/components/ui/TiltCard";
import { fetchApi } from "@/lib/api";

export default function BattleLobbyPage() {
  const router = useRouter();
  const [isSearching, setIsSearching] = useState(false);
  const [searchTimer, setSearchTimer] = useState(0);

  const startMatchmaking = async () => {
    setIsSearching(true);
    let sec = 0;
    const interval = setInterval(() => {
      sec += 1;
      setSearchTimer(sec);
    }, 1000);

    try {
      const data = await fetchApi<any>("/battles/queue", {
        method: "POST",
        body: JSON.stringify({
          user_id: "usr_alex",
          username: "coder_alex",
          elo: 1640,
          preferred_language: "python"
        })
      });
      clearInterval(interval);
      setTimeout(() => {
        router.push(`/battles/${data.id}`);
      }, 1500);
    } catch {
      clearInterval(interval);
      // Fallback local ID
      setTimeout(() => {
        router.push(`/battles/demo-battle`);
      }, 1500);
    }
  };

  return (
    <div className="min-h-screen bg-[#070D18] text-slate-100 py-10 px-4 md:px-8">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header Hero */}
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-red-950/40 via-purple-950/30 to-cyan-950/30 border border-red-500/30 p-8 shadow-2xl">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6 relative z-10">
            <div className="space-y-3 max-w-xl text-center md:text-left">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-red-500/20 border border-red-500/40 text-red-400 text-xs font-bold tracking-wide uppercase">
                <Swords className="w-3.5 h-3.5" />
                Real-Time 1v1 PvP Coding Arena
              </div>
              <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight bg-gradient-to-r from-white via-red-200 to-amber-200 bg-clip-text text-transparent">
                Battle of the Algorithms
              </h1>
              <p className="text-sm md:text-base text-slate-300">
                Face off against an Elo-matched opponent in a 10-minute speed solve duel.
                First to pass all hidden edge test cases takes the glory, XP, and rating points!
              </p>
            </div>

            {/* Matchmaking Action Card */}
            <div className="w-full md:w-80 bg-slate-900/90 border border-red-500/40 rounded-xl p-6 text-center shadow-xl backdrop-blur-md">
              <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-red-500 to-amber-500 flex items-center justify-center shadow-lg shadow-red-500/30 animate-pulse">
                <Swords className="w-8 h-8 text-slate-950 stroke-[2.5]" />
              </div>
              <div className="text-sm font-semibold text-slate-200 mb-1">Your Competitive Rating</div>
              <div className="text-2xl font-black text-amber-400 mb-4 font-mono">1,640 ELO <span className="text-xs text-emerald-400 font-normal">(Top 8%)</span></div>

              {isSearching ? (
                <div className="space-y-3">
                  <div className="flex items-center justify-center gap-2 text-sm text-cyan-400 font-medium">
                    <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-ping" />
                    Finding matched rival... ({searchTimer}s)
                  </div>
                  <div className="text-xs text-slate-400">Searching Elo range [1600 - 1680]</div>
                </div>
              ) : (
                <button
                  onClick={startMatchmaking}
                  className="w-full py-3.5 px-4 rounded-xl bg-gradient-to-r from-red-500 via-rose-500 to-amber-500 hover:from-red-600 hover:to-amber-600 text-slate-950 font-extrabold text-sm uppercase tracking-wider flex items-center justify-center gap-2 shadow-lg shadow-red-500/25 transition-transform active:scale-95"
                >
                  <Play className="w-4 h-4 fill-slate-950" />
                  Find Ranked Match
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Live Arena Stats & Recent Duels */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <TiltCard className="p-6 rounded-xl bg-slate-900/60 border border-slate-800 space-y-3">
            <div className="flex items-center gap-3 text-cyan-400">
              <Users className="w-5 h-5" />
              <h3 className="font-bold text-sm">Active Duelists</h3>
            </div>
            <div className="text-3xl font-black font-mono text-white">412 Online</div>
            <p className="text-xs text-slate-400">Average queue wait time under 3.8 seconds.</p>
          </TiltCard>

          <TiltCard className="p-6 rounded-xl bg-slate-900/60 border border-slate-800 space-y-3">
            <div className="flex items-center gap-3 text-amber-400">
              <Trophy className="w-5 h-5" />
              <h3 className="font-bold text-sm">Season 4 Champion</h3>
            </div>
            <div className="text-xl font-bold font-mono text-white flex items-center gap-2">
              <span className="text-amber-400">👑</span> CodeMaster_99
            </div>
            <p className="text-xs text-slate-400">Rating: 2,420 ELO (Grandmaster)</p>
          </TiltCard>

          <TiltCard className="p-6 rounded-xl bg-slate-900/60 border border-slate-800 space-y-3">
            <div className="flex items-center gap-3 text-emerald-400">
              <Shield className="w-5 h-5" />
              <h3 className="font-bold text-sm">Duel Rules</h3>
            </div>
            <ul className="text-xs text-slate-300 space-y-1 list-disc list-inside">
              <li>10 Minutes max per problem</li>
              <li>First to 100% test pass wins</li>
              <li>Wrong answers incur 15s freeze penalty</li>
            </ul>
          </TiltCard>
        </div>

        {/* Recent Public Arena Matches */}
        <div className="bg-slate-900/40 border border-slate-800 rounded-xl p-6 space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Flame className="w-4 h-4 text-orange-400" />
            Recent Finished Duels
          </h2>
          <div className="divide-y divide-slate-800/80">
            {[
              { p1: "coder_alex (1640)", p2: "ByteFalcon (1615)", winner: "coder_alex", time: "4m 12s", prob: "Two Sum" },
              { p1: "DataDrake (1780)", p2: "DevSarah (1820)", winner: "DevSarah", time: "6m 45s", prob: "Container With Most Water" },
              { p1: "AlgoSam (1500)", p2: "CodeKnight (1490)", winner: "AlgoSam", time: "3m 30s", prob: "Valid Parentheses" }
            ].map((duel, i) => (
              <div key={i} className="py-3 flex items-center justify-between text-xs md:text-sm">
                <div className="flex items-center gap-3">
                  <span className="font-mono text-slate-400">{duel.prob}</span>
                  <span className="text-slate-600">•</span>
                  <span className={duel.winner === duel.p1.split(" ")[0] ? "text-emerald-400 font-bold" : "text-slate-400"}>{duel.p1}</span>
                  <span className="text-red-400 font-mono font-bold">vs</span>
                  <span className={duel.winner === duel.p2.split(" ")[0] ? "text-emerald-400 font-bold" : "text-slate-400"}>{duel.p2}</span>
                </div>
                <div className="flex items-center gap-4">
                  <span className="text-xs font-mono text-slate-400">{duel.time}</span>
                  <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-[11px] font-semibold">
                    Winner: {duel.winner}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
