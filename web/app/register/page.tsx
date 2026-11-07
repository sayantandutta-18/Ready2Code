"use client";

import React, { useState, Suspense } from "react";
import Link from "next/link";
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
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-4xl grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
        {/* Left Side: Value Proposition & Highlights */}
        <div className="lg:col-span-5 bg-gradient-to-br from-cyan-950/40 via-surface-card to-indigo-950/30 border border-border/80 rounded-2xl p-8 flex flex-col justify-between shadow-xl">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-xs font-mono uppercase tracking-wider mb-6">
              <Sparkles className="w-3.5 h-3.5" />
              Free Lifetime Access
            </div>
            <h2 className="text-2xl font-bold text-white mb-3 tracking-tight">
              Level up your algorithmic mastery in 3D
            </h2>
            <p className="text-sm text-text-secondary leading-relaxed mb-6">
              Ready2Code pairs interactive 3D spatial execution with 100+ curated placement problems, live streaks, and real-time code analysis.
            </p>

            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 rounded-lg bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center flex-shrink-0 text-cyan-400 mt-0.5">
                  <Boxes className="w-4 h-4" />
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-white">Interactive 3D Visualizer</h4>
                  <p className="text-xs text-text-secondary">Watch pointers traverse trees, graphs, and linked lists in Three.js.</p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center flex-shrink-0 text-emerald-400 mt-0.5">
                  <Award className="w-4 h-4" />
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-white">100+ Top Placement Problems</h4>
                  <p className="text-xs text-text-secondary">Curated from FAANG, tier-1 tech firms, and competitive programming.</p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="w-8 h-8 rounded-lg bg-amber-500/10 border border-amber-500/20 flex items-center justify-center flex-shrink-0 text-amber-400 mt-0.5">
                  <Flame className="w-4 h-4" />
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-white">Daily Streaks & XP Leaderboards</h4>
                  <p className="text-xs text-text-secondary">Maintain your streak, freeze missed days, and rise on global leaderboards.</p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="w-8 h-8 rounded-lg bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center flex-shrink-0 text-indigo-400 mt-0.5">
                  <ShieldCheck className="w-4 h-4" />
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-white">Zero Setup Required</h4>
                  <p className="text-xs text-text-secondary">Browser-native Monaco code editor supporting Python, JavaScript, C++, and Java.</p>
                </div>
              </div>
            </div>
          </div>

          <div className="pt-6 border-t border-border/60 mt-6">
            <div className="text-xs text-text-muted mb-2 font-mono uppercase tracking-wider">Instant Quick-Test</div>
            <div className="flex flex-wrap gap-2">
              {DEMO_PROFILES.map((dp) => (
                <button
                  key={dp.username}
                  type="button"
                  onClick={() => handleDemoRegister(dp.username)}
                  disabled={isSubmitting}
                  className="px-3 py-1.5 rounded-lg bg-surface-base border border-border/70 hover:border-cyan-500/50 hover:bg-cyan-500/5 text-xs text-text-secondary hover:text-cyan-300 transition-colors flex items-center gap-1.5"
                >
                  <Zap className="w-3 h-3 text-cyan-400" />
                  Try as {dp.display_name}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Right Side: Registration Form */}
        <div className="lg:col-span-7 bg-surface-card border border-border rounded-2xl p-8 shadow-xl flex flex-col justify-center">
          {user ? (
            <div className="text-center py-6">
              <div className="w-16 h-16 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 flex items-center justify-center mx-auto mb-4">
                <CheckCircle2 className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">You are already registered</h3>
              <p className="text-sm text-text-secondary mb-6">
                Logged in as <span className="font-semibold text-cyan-300">@{user.username}</span> ({user.display_name}).
              </p>
              <div className="flex flex-col sm:flex-row gap-3 justify-center">
                <Link
                  href="/problems"
                  className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-medium text-sm transition-all flex items-center justify-center gap-2 shadow-lg shadow-cyan-500/20"
                >
                  Go to Problems
                  <ArrowRight className="w-4 h-4" />
                </Link>
                <button
                  onClick={logout}
                  className="px-5 py-2.5 rounded-xl bg-surface-base border border-border hover:border-rose-500/50 text-text-secondary hover:text-rose-400 text-sm font-medium transition-colors"
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
                <p className="text-sm text-text-secondary mt-1">
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
                    <label className="block text-xs font-medium text-text-secondary uppercase tracking-wider mb-1.5">
                      Username <span className="text-cyan-400">*</span>
                    </label>
                    <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-text-muted">
                        <User className="w-4 h-4" />
                      </div>
                      <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="e.g. dev_sarah"
                        required
                        className="w-full pl-9 pr-3 py-2 rounded-xl bg-surface-base border border-border text-white placeholder-text-muted text-sm focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-all font-mono"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-text-secondary uppercase tracking-wider mb-1.5">
                      Display Name
                    </label>
                    <input
                      type="text"
                      value={displayName}
                      onChange={(e) => setDisplayName(e.target.value)}
                      placeholder="e.g. Sarah Connor"
                      className="w-full px-3 py-2 rounded-xl bg-surface-base border border-border text-white placeholder-text-muted text-sm focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-all"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-medium text-text-secondary uppercase tracking-wider mb-1.5">
                      Password
                    </label>
                    <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-text-muted">
                        <Lock className="w-4 h-4" />
                      </div>
                      <input
                        type={showPassword ? "text" : "password"}
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="At least 6 chars"
                        className="w-full pl-9 pr-10 py-2 rounded-xl bg-surface-base border border-border text-white placeholder-text-muted text-sm focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-all"
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute inset-y-0 right-0 pr-3 flex items-center text-text-muted hover:text-white transition-colors"
                      >
                        {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                      </button>
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-text-secondary uppercase tracking-wider mb-1.5">
                      Confirm Password
                    </label>
                    <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-text-muted">
                        <Lock className="w-4 h-4" />
                      </div>
                      <input
                        type={showPassword ? "text" : "password"}
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        placeholder="Re-type password"
                        className="w-full pl-9 pr-3 py-2 rounded-xl bg-surface-base border border-border text-white placeholder-text-muted text-sm focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-all"
                      />
                    </div>
                  </div>
                </div>

                {/* Experience Level */}
                <div>
                  <label className="block text-xs font-medium text-text-secondary uppercase tracking-wider mb-1.5">
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
                        className={`p-2 rounded-xl border text-left transition-all ${
                          experienceLevel === lvl.id
                            ? "bg-cyan-500/10 border-cyan-500/60 text-cyan-300 shadow-sm"
                            : "bg-surface-base border-border text-text-secondary hover:border-border/90"
                        }`}
                      >
                        <div className="text-xs font-semibold">{lvl.label}</div>
                        <div className="text-[10px] text-text-muted">{lvl.sub}</div>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Terms agreement */}
                <div className="pt-2">
                  <label className="flex items-start gap-2.5 text-xs text-text-secondary cursor-pointer select-none">
                    <input
                      type="checkbox"
                      checked={agreeTerms}
                      onChange={(e) => setAgreeTerms(e.target.checked)}
                      className="mt-0.5 rounded border-border bg-surface-base text-cyan-500 focus:ring-cyan-500"
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
                      Creating your account...
                    </>
                  ) : (
                    <>
                      Create Account
                      <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
                    </>
                  )}
                </button>
              </form>

              <div className="mt-6 pt-5 border-t border-border/60 text-center">
                <p className="text-xs text-text-secondary">
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
        <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center text-text-muted text-sm">
          Loading registration...
        </div>
      }
    >
      <RegisterForm />
    </Suspense>
  );
}
