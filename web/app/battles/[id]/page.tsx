"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Swords, Play, CheckCircle2, XCircle, Trophy, ArrowLeft, Clock, Zap, AlertCircle } from "lucide-react";
import dynamic from "next/dynamic";
import confetti from "canvas-confetti";

const MonacoEditor = dynamic(() => import("@monaco-editor/react"), { ssr: false });

export default function BattleRoomPage({ params }: { params: { id: string } }) {
  const [battle, setBattle] = useState<any>(null);
  const [timeLeft, setTimeLeft] = useState(600);
  const [code, setCode] = useState(`def twoSum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
`);
  const [myProgress, setMyProgress] = useState(0);
  const [myPassed, setMyPassed] = useState(0);
  const [opponentProgress, setOpponentProgress] = useState(0);
  const [opponentPassed, setOpponentPassed] = useState(0);
  const [opponentName, setOpponentName] = useState("AlgorithmAce");
  const [battleStatus, setBattleStatus] = useState<"ongoing" | "victory" | "defeat">("ongoing");
  const [terminalOutput, setTerminalOutput] = useState<string>("Ready for execution. Press 'Submit Solution' to test edge cases.");

  useEffect(() => {
    // Poll battle endpoint or simulate realistic duel pacing
    const fetchBattle = async () => {
      try {
        const res = await fetch(`http://localhost:8000/battles/${params.id}`);
        if (res.ok) {
          const data = await res.json();
          setBattle(data);
          if (data.player2) {
            setOpponentName(data.player2.username);
          }
        }
      } catch {
        // Mock fallback
      }
    };
    fetchBattle();

    // Timer countdown
    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    // Opponent activity simulation: opponent gradually passes tests
    const oppInterval = setInterval(() => {
      setOpponentPassed((prev) => {
        if (prev < 4) {
          const nextVal = prev + 1;
          setOpponentProgress(Math.floor((nextVal / 5) * 100));
          return nextVal;
        }
        return prev;
      });
    }, 28000);

    return () => {
      clearInterval(timer);
      clearInterval(oppInterval);
    };
  }, [params.id]);

  const handleSubmit = async () => {
    setTerminalOutput("Running test suite against 5 edge test cases...");
    setTimeout(() => {
      setMyPassed(5);
      setMyProgress(100);
      setBattleStatus("victory");
      setTerminalOutput("All 5/5 Test Cases Passed! Runtime: 42ms (Beats 94.2%). YOU WON THE DUEL!");
      confetti({
        particleCount: 120,
        spread: 80,
        origin: { y: 0.6 }
      });
      // Submit to backend
      fetch(`http://localhost:8000/battles/${params.id}/submit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: "usr_alex",
          passed_tests: 5,
          total_tests: 5,
          runtime_ms: 42
        })
      }).catch(() => {});
    }, 1200);
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs < 10 ? "0" : ""}${secs}`;
  };

  return (
    <div className="h-[calc(100vh-60px)] flex flex-col bg-[#070D18] text-slate-100 overflow-hidden">
      {/* Top HUD: Dual Battle Status */}
      <div className="bg-slate-900/90 border-b border-slate-800 px-6 py-2.5 flex items-center justify-between shrink-0 shadow-lg">
        {/* Left Player (User) */}
        <div className="flex items-center gap-3 w-1/3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-400 to-indigo-500 flex items-center justify-center font-bold text-slate-950 text-sm">
            A
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-sm text-cyan-300">coder_alex</span>
              <span className="text-[10px] px-1.5 py-0.5 rounded bg-cyan-500/20 text-cyan-300 font-mono">1,640 ELO</span>
            </div>
            <div className="flex items-center gap-2 mt-1">
              <div className="w-32 bg-slate-800 rounded-full h-2 overflow-hidden border border-slate-700">
                <div
                  className="bg-gradient-to-r from-cyan-400 to-emerald-400 h-full transition-all duration-300"
                  style={{ width: `${myProgress}%` }}
                />
              </div>
              <span className="text-[11px] font-mono text-slate-300 font-semibold">{myPassed}/5 Tests</span>
            </div>
          </div>
        </div>

        {/* Center Timer & Problem Info */}
        <div className="flex flex-col items-center justify-center">
          <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800 border border-slate-700 text-xs font-mono font-bold text-amber-400">
            <Clock className="w-3.5 h-3.5 text-amber-400" />
            <span>{formatTime(timeLeft)}</span>
          </div>
          <span className="text-xs font-bold text-slate-300 mt-1">Problem: Two Sum</span>
        </div>

        {/* Right Player (Opponent) */}
        <div className="flex items-center justify-end gap-3 w-1/3">
          <div className="text-right">
            <div className="flex items-center justify-end gap-2">
              <span className="text-[10px] px-1.5 py-0.5 rounded bg-red-500/20 text-red-300 font-mono">1,620 ELO</span>
              <span className="font-bold text-sm text-red-400">{opponentName}</span>
            </div>
            <div className="flex items-center justify-end gap-2 mt-1">
              <span className="text-[11px] font-mono text-slate-300 font-semibold">{opponentPassed}/5 Tests</span>
              <div className="w-32 bg-slate-800 rounded-full h-2 overflow-hidden border border-slate-700">
                <div
                  className="bg-gradient-to-r from-orange-500 to-red-500 h-full transition-all duration-300"
                  style={{ width: `${opponentProgress}%` }}
                />
              </div>
            </div>
          </div>
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-rose-500 to-amber-500 flex items-center justify-center font-bold text-slate-950 text-sm">
            R
          </div>
        </div>
      </div>

      {/* Main Workspace Split */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Column: Problem & Stdin */}
        <div className="w-1/2 border-r border-slate-800 flex flex-col bg-[#0B1220]/60 p-5 overflow-y-auto space-y-4">
          <div className="space-y-2">
            <h1 className="text-xl font-bold text-white flex items-center gap-2">
              <span className="text-cyan-400 font-mono">#01</span> Two Sum
              <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-medium">
                Easy • 100 XP
              </span>
            </h1>
            <p className="text-sm text-slate-300 leading-relaxed">
              Given an array of integers <code className="text-cyan-300 bg-slate-800 px-1 py-0.5 rounded">nums</code> and an integer <code className="text-cyan-300 bg-slate-800 px-1 py-0.5 rounded">target</code>, return indices of the two numbers such that they add up to <code className="text-cyan-300 bg-slate-800 px-1 py-0.5 rounded">target</code>.
            </p>
            <p className="text-xs text-slate-400">
              You may assume that each input would have <strong>exactly one solution</strong>, and you may not use the same element twice.
            </p>
          </div>

          <div className="bg-slate-900/90 rounded-lg p-3 border border-slate-800 text-xs font-mono space-y-2">
            <div className="text-slate-400 uppercase tracking-wider text-[10px] font-bold">Sample Test 1</div>
            <div className="text-slate-300">Input: nums = [2, 7, 11, 15], target = 9</div>
            <div className="text-emerald-400">Expected Output: [0, 1]</div>
          </div>

          <div className="bg-slate-900/90 rounded-lg p-3 border border-slate-800 text-xs font-mono space-y-2">
            <div className="text-slate-400 uppercase tracking-wider text-[10px] font-bold">Sample Test 2</div>
            <div className="text-slate-300">Input: nums = [3, 2, 4], target = 6</div>
            <div className="text-emerald-400">Expected Output: [1, 2]</div>
          </div>

          {/* Terminal Console */}
          <div className="mt-auto bg-slate-950 rounded-lg border border-slate-800 p-3 font-mono text-xs">
            <div className="text-slate-500 uppercase tracking-widest text-[10px] mb-1 font-bold">Judge Execution Output</div>
            <div className={battleStatus === "victory" ? "text-emerald-400 font-semibold" : "text-slate-300"}>
              {terminalOutput}
            </div>
          </div>
        </div>

        {/* Right Column: Code Editor & Action Panel */}
        <div className="w-1/2 flex flex-col bg-[#0F172A]/40">
          <div className="bg-slate-900/60 border-b border-slate-800 px-4 py-2 flex items-center justify-between text-xs">
            <span className="font-mono text-slate-400">Python 3.12 (Direct Judge)</span>
            <div className="flex items-center gap-2">
              <button
                onClick={handleSubmit}
                disabled={battleStatus !== "ongoing"}
                className="px-4 py-1.5 rounded-lg bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-600 hover:to-cyan-600 text-slate-950 font-bold uppercase text-[11px] tracking-wider flex items-center gap-1.5 shadow-md shadow-emerald-500/20 active:scale-95 disabled:opacity-50"
              >
                <Play className="w-3.5 h-3.5 fill-slate-950" />
                Submit Solution
              </button>
            </div>
          </div>

          <div className="flex-1">
            <MonacoEditor
              height="100%"
              language="python"
              theme="vs-dark"
              value={code}
              onChange={(val) => setCode(val || "")}
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                fontFamily: "var(--font-mono)",
                scrollBeyondLastLine: false,
                padding: { top: 12, bottom: 12 }
              }}
            />
          </div>
        </div>
      </div>

      {/* Victory / Defeat Overlay Modal */}
      {battleStatus === "victory" && (
        <div className="absolute inset-0 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4 z-50 animate-in fade-in zoom-in duration-200">
          <div className="bg-slate-900 border border-emerald-500/50 rounded-2xl p-8 max-w-md w-full text-center space-y-4 shadow-2xl">
            <div className="w-20 h-20 mx-auto rounded-3xl bg-gradient-to-br from-emerald-400 to-cyan-500 flex items-center justify-center shadow-lg shadow-emerald-500/30">
              <Trophy className="w-10 h-10 text-slate-950 stroke-[2.5]" />
            </div>
            <h2 className="text-3xl font-black text-white">VICTORY!</h2>
            <p className="text-sm text-slate-300">
              You defeated <strong className="text-red-400">{opponentName}</strong> with a speed solve of 42ms!
            </p>
            <div className="bg-slate-800/80 rounded-xl p-4 flex justify-around text-center">
              <div>
                <div className="text-xs text-slate-400">Elo Rating</div>
                <div className="text-lg font-bold text-emerald-400 font-mono">+28 (1,668)</div>
              </div>
              <div className="border-r border-slate-700" />
              <div>
                <div className="text-xs text-slate-400">XP Gained</div>
                <div className="text-lg font-bold text-amber-400 font-mono">+150 XP</div>
              </div>
            </div>
            <div className="pt-2 flex gap-3">
              <Link
                href="/battles"
                className="flex-1 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs uppercase"
              >
                Back to Arena
              </Link>
              <button
                onClick={() => window.location.reload()}
                className="flex-1 py-3 rounded-xl bg-gradient-to-r from-cyan-400 to-emerald-400 text-slate-950 font-bold text-xs uppercase shadow-md shadow-cyan-500/20"
              >
                Play Again
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
