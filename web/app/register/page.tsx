"use client";

import React, { useState, Suspense } from "react";
import Link from "next/link";
import dynamic from "next/dynamic";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/lib/authContext";
import {
  Code2,
  User,
  Lock,
  ArrowRight,
  Loader2,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  Eye,
  EyeOff,
  Flame,
  Zap,
  Boxes,
  ShieldCheck,
  Award,
} from "lucide-react";

// Lazy-load AuthSpatialCanvas with ssr: false
const AuthSpatialCanvas = dynamic(() => import("@/components/3d/AuthSpatialCanvas"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-[220px] sm:h-[260px] flex items-center justify-center text-emerald-400/60 font-mono text-xs">
      Initializing 3D genesis matrix...
    </div>
  ),
});

const DEMO_PROFILES = [
  { username: "algo_ninja", display_name: "Algo Ninja", streak: 7, xp: 420 },
  { username: "byte_master", display_name: "Byte Master", streak: 3, xp: 180 },
];

function RegisterForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const redirectPath = searchParams.get("redirect") || "/problems";

  const { user, register, login, logout } = useAuth();
  const [username, setUsername] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [experienceLevel, setExperienceLevel] = useState<"beginner" | "intermediate" | "advanced">("intermediate");
  const [agreeTerms, setAgreeTerms] = useState(true);
  const [errorMsg, setErrorMsg] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg("");

    const trimmedUser = username.trim().toLowerCase();
    const trimmedDisplay = displayName.trim() || trimmedUser;

    if (!trimmedUser) {
      setErrorMsg("Please choose a username.");
      return;
    }
    if (trimmedUser.length < 3 || trimmedUser.length > 24) {
      setErrorMsg("Username must be between 3 and 24 characters.");
      return;
    }
    if (!/^[a-zA-Z0-9_-]+$/.test(trimmedUser)) {
      setErrorMsg("Username may only contain letters, numbers, underscores, and hyphens.");
      return;
    }
    if (password && password.length < 6) {
      setErrorMsg("Password must be at least 6 characters.");
      return;
    }
    if (password && confirmPassword && password !== confirmPassword) {
      setErrorMsg("Passwords do not match.");
      return;
    }
    if (!agreeTerms) {
      setErrorMsg("Please accept the terms to create your account.");
      return;
    }

    setIsSubmitting(true);
    try {
      await register(trimmedUser, trimmedDisplay);
      router.push(redirectPath);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Registration failed. Username may already be taken.";
      setErrorMsg(msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDemoRegister = async (demoUsername: string) => {
    setIsSubmitting(true);
    setErrorMsg("");
    try {
      await login(demoUsername);
      router.push(redirectPath);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to load demo profile.";
      setErrorMsg(msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-[#0B1220] relative overflow-hidden">
      {/* Background ambient radial gradients */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="w-full max-w-5xl grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch relative z-10">
        {/* Left Side: 3D Genesis Matrix & Value Propositions */}
        <div className="lg:col-span-5 bg-gradient-to-br from-cyan-950/40 via-[#121C2F] to-indigo-950/30 border border-slate-800 rounded-2xl p-6 sm:p-8 flex flex-col justify-between shadow-2xl">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-mono uppercase tracking-wider mb-4">
              <Sparkles className="w-3.5 h-3.5" />
              <span>3D Algorithmic Genesis</span>
            </div>
            <h2 className="text-2xl font-bold text-white mb-2 tracking-tight">
              Level up your algorithmic mastery in 3D
            </h2>
            <p className="text-xs text-slate-300 leading-relaxed mb-4">
              Interactive spatial execution with 100+ curated problems, live streaks, and real-time code analysis.
            </p>

            {/* Interactive 3D Canvas */}
            <div className="my-2 rounded-xl overflow-hidden border border-emerald-500/20 bg-slate-950/40">
              <AuthSpatialCanvas variant="register" className="w-full h-[220px] sm:h-[250px]" />
            </div>

            <div className="space-y-3 mt-4">
              <div className="flex items-start gap-3">
                <div className="w-7 h-7 rounded-lg bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center flex-shrink-0 text-cyan-400 mt-0.5">
                  <Boxes className="w-3.5 h-3.5" />
                </div>
                <div>
                  <h4 className="text-xs font-semibold text-white">Interactive 3D Visualizer</h4>
                  <p className="text-[11px] text-slate-400">Watch pointers traverse trees, graphs, and linked lists in Three.js.</p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="w-7 h-7 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center flex-shrink-0 text-emerald-400 mt-0.5">
                  <Award className="w-3.5 h-3.5" />
                </div>
                <div>
                  <h4 className="text-xs font-semibold text-white">100+ Curated Placement Labs</h4>
                  <p className="text-[11px] text-slate-400">FAANG & tier-1 technical questions with 1,192 verified test cases.</p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="w-7 h-7 rounded-lg bg-amber-500/10 border border-amber-500/20 flex items-center justify-center flex-shrink-0 text-amber-400 mt-0.5">
                  <Flame className="w-3.5 h-3.5" />
                </div>
                <div>
                  <h4 className="text-xs font-semibold text-white">Daily Streaks & XP Leaderboards</h4>
                  <p className="text-[11px] text-slate-400">Maintain your streak, freeze missed days, and rise on rankings.</p>
                </div>
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-800 mt-4">
            <div className="text-[11px] text-slate-500 mb-2 font-mono uppercase tracking-wider">Instant Quick-Test</div>
            <div className="flex flex-wrap gap-2">
              {DEMO_PROFILES.map((dp) => (
                <button
                  key={dp.username}
                  type="button"
                  onClick={() => handleDemoRegister(dp.username)}
                  disabled={isSubmitting}
                  className="px-2.5 py-1.5 rounded-lg bg-[#0B1220] border border-slate-700 hover:border-cyan-500/50 hover:bg-cyan-500/10 text-xs text-slate-300 hover:text-cyan-300 transition-colors flex items-center gap-1.5 cursor-pointer"
                >
                  <Zap className="w-3 h-3 text-cyan-400" />
                  <span>Try as {dp.display_name}</span>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Right Side: Registration Form */}
        <div className="lg:col-span-7 bg-[#121C2F] border border-slate-800 rounded-2xl p-8 shadow-xl flex flex-col justify-center">
          {user ? (
            <div className="text-center py-6">
              <div className="w-16 h-16 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 flex items-center justify-center mx-auto mb-4">
                <CheckCircle2 className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">You are already registered</h3>
              <p className="text-sm text-slate-300 mb-6">
                Logged in as <span className="font-semibold text-cyan-300">@{user.username}</span> ({user.display_name}).
              </p>
              <div className="flex flex-col sm:flex-row gap-3 justify-center">
                <Link
                  href="/problems"
                  className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-medium text-sm transition-all flex items-center justify-center gap-2 shadow-lg shadow-cyan-500/20"
                >
                  <span>Go to Problems</span>
                  <ArrowRight className="w-4 h-4" />
                </Link>
                <button
                  onClick={logout}
                  className="px-5 py-2.5 rounded-xl bg-[#0B1220] border border-slate-700 hover:border-rose-500/50 text-slate-300 hover:text-rose-400 text-sm font-medium transition-colors cursor-pointer"
                >
                  Sign Out
                </button>
              </div>
            </div>
          ) : (
            <>
              <div className="mb-6">
                <div className="flex items-center gap-2 text-cyan-400 mb-2">
                  <Code2 className="w-5 h-5" />
                  <span className="text-xs font-mono uppercase tracking-widest text-cyan-300 font-semibold">Join Ready2Code</span>
                </div>
                <h1 className="text-2xl font-bold text-white tracking-tight">Create your account</h1>
                <p className="text-sm text-slate-300 mt-1">
                  Start coding and visualizing algorithmic concepts in under 30 seconds.
                </p>
              </div>

              {errorMsg && (
                <div className="mb-5 p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm flex items-start gap-2.5 animate-fadeIn">
                  <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5 text-rose-400" />
                  <span className="flex-1 text-xs sm:text-sm">{errorMsg}</span>
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                      Username <span className="text-cyan-400">*</span>
                    </label>
                    <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500">
                        <User className="w-4 h-4" />
                      </div>
                      <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="e.g. dev_sarah"
                        required
                        className="w-full pl-9 pr-3 py-2 rounded-xl bg-[#0B1220] border border-slate-700 text-cyan-300 font-semibold placeholder-slate-500 text-sm focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 transition-all font-mono"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                      Display Name
                    </label>
                    <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500">
                        <User className="w-4 h-4" />
                      </div>
                      <input
                        type="text"
                        value={displayName}
                        onChange={(e) => setDisplayName(e.target.value)}
                        placeholder="e.g. Sarah Connor"
                        className="w-full pl-9 pr-3 py-2 rounded-xl bg-[#0B1220] border border-slate-700 text-cyan-300 font-semibold placeholder-slate-500 text-sm focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 transition-all"
                      />
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                      Password
                    </label>
                    <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500">
                        <Lock className="w-4 h-4" />
                      </div>
                      <input
                        type={showPassword ? "text" : "password"}
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="At least 6 chars"
                        className="w-full pl-9 pr-10 py-2 rounded-xl bg-[#0B1220] border border-slate-700 text-cyan-300 font-semibold placeholder-slate-500 text-sm focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 transition-all font-mono"
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-500 hover:text-white transition-colors"
                      >
                        {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                      </button>
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                      Confirm Password
                    </label>
                    <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500">
                        <Lock className="w-4 h-4" />
                      </div>
                      <input
                        type={showPassword ? "text" : "password"}
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        placeholder="Re-type password"
                        className="w-full pl-9 pr-3 py-2 rounded-xl bg-[#0B1220] border border-slate-700 text-cyan-300 font-semibold placeholder-slate-500 text-sm focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 transition-all font-mono"
                      />
                    </div>
                  </div>
                </div>

                {/* Experience Level */}
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                    Coding Experience
                  </label>
                  <div className="grid grid-cols-3 gap-2">
                    {(
                      [
                        { id: "beginner", label: "Beginner", sub: "New to DSA" },
                        { id: "intermediate", label: "Intermediate", sub: "Prep for OAs" },
                        { id: "advanced", label: "Advanced", sub: "FAANG / CP" },
                      ] as const
                    ).map((lvl) => (
                      <button
                        key={lvl.id}
                        type="button"
                        onClick={() => setExperienceLevel(lvl.id)}
                        className={`p-2 rounded-xl border text-left transition-all cursor-pointer ${
                          experienceLevel === lvl.id
                            ? "bg-cyan-500/20 border-cyan-500 text-cyan-300 shadow-sm shadow-cyan-500/20"
                            : "bg-[#0B1220] border-slate-800 text-slate-300 hover:border-slate-700 hover:text-slate-100"
                        }`}
                      >
                        <div className="text-xs font-semibold">{lvl.label}</div>
                        <div className="text-[10px] text-slate-400">{lvl.sub}</div>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Terms agreement */}
                <div className="pt-2">
                  <label className="flex items-start gap-2.5 text-xs text-slate-300 cursor-pointer select-none">
                    <input
                      type="checkbox"
                      checked={agreeTerms}
                      onChange={(e) => setAgreeTerms(e.target.checked)}
                      className="mt-0.5 rounded border-slate-700 bg-[#0B1220] text-cyan-500 focus:ring-cyan-500"
                    />
                    <span>
                      I agree to the Ready2Code terms of service and acknowledge that all problem submissions are benchmarked against official test suites.
                    </span>
                  </label>
                </div>

                {/* Submit button */}
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full mt-2 py-3 px-4 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-medium text-sm transition-all duration-200 flex items-center justify-center gap-2 shadow-lg shadow-cyan-500/20 disabled:opacity-50 disabled:cursor-not-allowed group cursor-pointer"
                >
                  {isSubmitting ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>Creating your account...</span>
                    </>
                  ) : (
                    <>
                      <span>Create Account</span>
                      <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
                    </>
                  )}
                </button>
              </form>

              <div className="mt-6 pt-5 border-t border-slate-800 text-center">
                <p className="text-xs text-slate-400">
                  Already have an account?{" "}
                  <Link
                    href={`/login${redirectPath !== "/problems" ? `?redirect=${encodeURIComponent(redirectPath)}` : ""}`}
                    className="text-cyan-400 hover:text-cyan-300 font-medium transition-colors"
                  >
                    Sign In instead
                  </Link>
                </p>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default function RegisterPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center text-slate-400 text-sm">
          Loading 3D registration...
        </div>
      }
    >
      <RegisterForm />
    </Suspense>
  );
}
