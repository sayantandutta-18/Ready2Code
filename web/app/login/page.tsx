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
  Shield,
  Layers,
} from "lucide-react";

// Lazy-load AuthSpatialCanvas with ssr: false
const AuthSpatialCanvas = dynamic(() => import("@/components/3d/AuthSpatialCanvas"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-[320px] lg:h-[420px] flex items-center justify-center text-cyan-400/60 font-mono text-xs">
      Initializing 3D spatial vault...
    </div>
  ),
});

function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const redirectPath = searchParams.get("redirect") || "/problems";

  const { user, login, logout } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(true);
  const [errorMsg, setErrorMsg] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg("");

    const trimmedUser = username.trim();
    if (!trimmedUser) {
      setErrorMsg("Please enter your username.");
      return;
    }

    setIsSubmitting(true);
    try {
      await login(trimmedUser, password || undefined);
      router.push(redirectPath);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Invalid credentials. Please verify your username.";
      setErrorMsg(msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDemoLogin = async (demoUsername: string) => {
    setErrorMsg("");
    setIsSubmitting(true);
    try {
      await login(demoUsername);
      router.push(redirectPath);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Demo sign in failed.";
      setErrorMsg(msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  // If user is already authenticated
  if (user) {
    return (
      <div className="min-h-[calc(100vh-65px)] flex items-center justify-center px-4 py-12 bg-[#0B1220]">
        <div className="w-full max-w-md bg-[#121C2F] border border-slate-800 rounded-3xl p-8 shadow-2xl text-center space-y-6 relative overflow-hidden">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-cyan-400 to-indigo-600 flex items-center justify-center font-black text-2xl text-slate-950 mx-auto shadow-lg shadow-cyan-500/25">
            {user.username.charAt(0).toUpperCase()}
          </div>

          <div className="space-y-1">
            <h1 className="text-2xl font-black text-white">You are Signed In</h1>
            <p className="text-sm text-slate-400">
              Welcome back, <span className="text-cyan-400 font-semibold">{user.display_name || user.username}</span>
            </p>
          </div>

          <div className="grid grid-cols-2 gap-3 p-4 bg-[#0B1220] rounded-2xl border border-slate-800 text-xs font-mono">
            <div className="flex items-center justify-center gap-1.5 text-amber-400">
              <Flame className="w-4 h-4 fill-amber-400" />
              <span>{user.streak} Day Streak</span>
            </div>
            <div className="flex items-center justify-center gap-1.5 text-violet-400">
              <Zap className="w-4 h-4 fill-violet-400" />
              <span>{user.xp} XP</span>
            </div>
          </div>

          <div className="space-y-2.5 pt-2">
            <Link
              href={redirectPath}
              className="w-full py-3 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-500 hover:from-cyan-600 hover:to-indigo-600 text-slate-950 font-bold text-xs uppercase tracking-wider flex items-center justify-center gap-2 shadow-lg shadow-cyan-500/20 transition-all active:scale-95"
            >
              <span>Continue to Problems</span>
              <ArrowRight className="w-4 h-4" />
            </Link>

            <button
              onClick={logout}
              className="w-full py-2.5 rounded-xl bg-slate-800/80 hover:bg-slate-800 border border-slate-700/60 text-slate-300 text-xs font-semibold transition-colors"
            >
              Sign Out
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-[calc(100vh-65px)] flex items-center justify-center px-4 py-12 bg-[#0B1220] relative overflow-hidden">
      {/* Background glow effects */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="w-full max-w-5xl grid grid-cols-1 lg:grid-cols-12 gap-8 items-center relative z-10">
        {/* Left Column: 3D Holographic Vault Showcase */}
        <div className="lg:col-span-6 bg-gradient-to-br from-cyan-950/40 via-[#121C2F] to-indigo-950/30 border border-slate-800 rounded-3xl p-6 sm:p-8 flex flex-col justify-between shadow-2xl relative overflow-hidden">
          <div className="space-y-4">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-xs font-mono uppercase tracking-wider">
              <Shield className="w-3.5 h-3.5" />
              <span>Spatial 3D Security Vault</span>
            </div>

            <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight leading-tight">
              Re-enter your 3D Algorithmic Sandbox
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 leading-relaxed">
              Resume your streaks, inspect code execution in spatial 3D arrays, and benchmark your solutions across 1,192 automated test suites.
            </p>
          </div>

          {/* Interactive 3D Canvas */}
          <div className="my-4">
            <AuthSpatialCanvas variant="login" className="w-full h-[280px] sm:h-[340px]" />
          </div>

          <div className="pt-4 border-t border-slate-800/80 grid grid-cols-2 gap-3 text-xs text-slate-400 font-mono">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
              <span>100+ Verified DSA Labs</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-cyan-400" />
              <span>Three.js Spatial Engine</span>
            </div>
          </div>
        </div>

        {/* Right Column: Sign In Form */}
        <div className="lg:col-span-6 bg-[#121C2F] border border-slate-800 rounded-3xl p-8 shadow-2xl relative z-10 text-slate-200">
          {/* Brand header */}
          <div className="text-center space-y-2 mb-8">
            <Link href="/" className="inline-flex items-center justify-center gap-2.5 group mb-2">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-400 to-violet-600 flex items-center justify-center shadow-lg shadow-cyan-500/20 group-hover:scale-105 transition-transform">
                <Code2 className="w-5 h-5 text-slate-950 stroke-[2.5]" />
              </div>
              <span className="font-extrabold text-xl tracking-tight bg-gradient-to-r from-white via-cyan-200 to-cyan-400 bg-clip-text text-transparent">
                Ready2Code
              </span>
            </Link>

            <h1 className="text-2xl font-black text-white tracking-tight">Sign In to Your Arena</h1>
            <p className="text-xs text-slate-400">
              Access your 3D algorithm progress, saved code, and placement tracks.
            </p>
          </div>

          {/* Error Banner */}
          {errorMsg && (
            <div className="mb-6 p-3.5 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-xs flex items-center gap-2.5 animate-in fade-in duration-200">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span className="flex-1 font-medium">{errorMsg}</span>
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                Username
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
                  <User className="w-4 h-4" />
                </div>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="e.g. algo_ninja"
                  autoComplete="username"
                  required
                  className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-[#0B1220] border border-slate-700/80 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 transition-all font-mono"
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider">
                  Password
                </label>
                <span className="text-[11px] text-slate-500 font-mono">(Optional for guest session)</span>
              </div>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
                  <Lock className="w-4 h-4" />
                </div>
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="&bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull;"
                  autoComplete="current-password"
                  className="w-full pl-10 pr-10 py-2.5 rounded-xl bg-[#0B1220] border border-slate-700/80 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 transition-all font-mono"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-slate-500 hover:text-slate-300 transition-colors"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            <div className="flex items-center justify-between pt-1">
              <label className="flex items-center gap-2 cursor-pointer text-xs text-slate-400 select-none">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  className="rounded border-slate-700 bg-[#0B1220] text-cyan-500 focus:ring-cyan-400/20"
                />
                <span>Remember this workstation</span>
              </label>
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full py-3 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-500 hover:from-cyan-400 hover:to-indigo-400 text-slate-950 font-bold text-xs uppercase tracking-wider flex items-center justify-center gap-2 shadow-lg shadow-cyan-500/20 active:scale-95 transition-all disabled:opacity-50 disabled:pointer-events-none mt-2 cursor-pointer"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Authenticating...</span>
                </>
              ) : (
                <>
                  <span>Sign In</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          {/* Quick Demo Logins */}
          <div className="mt-8 pt-6 border-t border-slate-800">
            <div className="text-center mb-3">
              <span className="text-[11px] font-mono text-slate-500 uppercase tracking-widest flex items-center justify-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
                <span>Or explore with 1-click demo coder</span>
              </span>
            </div>

            <div className="grid grid-cols-2 gap-2.5">
              <button
                type="button"
                onClick={() => handleDemoLogin("algo_ninja")}
                disabled={isSubmitting}
                className="p-2.5 rounded-xl bg-[#0B1220] border border-slate-800 hover:border-cyan-500/50 hover:bg-cyan-500/5 text-left transition-all group"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-200 group-hover:text-cyan-300">algo_ninja</span>
                  <Flame className="w-3.5 h-3.5 text-amber-400 fill-amber-400" />
                </div>
                <span className="text-[10px] text-slate-500 font-mono">7-day streak &bull; 420 XP</span>
              </button>

              <button
                type="button"
                onClick={() => handleDemoLogin("byte_master")}
                disabled={isSubmitting}
                className="p-2.5 rounded-xl bg-[#0B1220] border border-slate-800 hover:border-indigo-500/50 hover:bg-indigo-500/5 text-left transition-all group"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-200 group-hover:text-indigo-300">byte_master</span>
                  <Zap className="w-3.5 h-3.5 text-violet-400 fill-violet-400" />
                </div>
                <span className="text-[10px] text-slate-500 font-mono">3-day streak &bull; 180 XP</span>
              </button>
            </div>
          </div>

          {/* Switch to Register link */}
          <div className="mt-6 text-center text-xs text-slate-400">
            Don&apos;t have an account yet?{" "}
            <Link
              href={`/register${redirectPath !== "/problems" ? `?redirect=${encodeURIComponent(redirectPath)}` : ""}`}
              className="text-cyan-400 hover:text-cyan-300 font-semibold underline underline-offset-4 decoration-cyan-400/40 hover:decoration-cyan-300 transition-colors"
            >
              Create free account &rarr;
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function LoginPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center text-slate-400 text-sm">
          Loading 3D sign in...
        </div>
      }
    >
      <LoginForm />
    </Suspense>
  );
}
