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
} from "lucide-react";

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

      <div className="w-full max-w-md bg-[#121C2F] border border-slate-800 rounded-3xl p-8 shadow-2xl relative z-10 text-slate-200">
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

        {/* Error notification */}
        {errorMsg && (
          <div className="mb-5 p-3.5 rounded-2xl bg-red-500/10 border border-red-500/30 text-xs text-red-400 flex items-center gap-2.5 animate-in fade-in">
            <AlertCircle className="w-4 h-4 shrink-0 text-red-400" />
            <span>{errorMsg}</span>
          </div>
        )}

        {/* Login form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-1.5">
              Username or Handle
            </label>
            <div className="relative">
              <User className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                required
                autoComplete="username"
                placeholder="e.g. algo_ninja"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full bg-[#0B1220] border border-slate-700/80 rounded-xl pl-10 pr-3.5 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 transition-all"
              />
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label className="text-[11px] font-mono uppercase tracking-wider text-slate-400">
                Password
              </label>
              <span className="text-[11px] text-slate-500 font-mono">Optional for demo accounts</span>
            </div>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type={showPassword ? "text" : "password"}
                autoComplete="current-password"
                placeholder="••••••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-[#0B1220] border border-slate-700/80 rounded-xl pl-10 pr-10 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 transition-all"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300 transition-colors p-1"
                aria-label={showPassword ? "Hide password" : "Show password"}
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>

          <div className="flex items-center justify-between pt-1 text-xs">
            <label className="flex items-center gap-2 cursor-pointer text-slate-400 select-none">
              <input
                type="checkbox"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                className="rounded border-slate-700 bg-[#0B1220] text-cyan-500 focus:ring-cyan-400 focus:ring-offset-0"
              />
              <span>Remember this session</span>
            </label>
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full py-3 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-500 hover:from-cyan-600 hover:to-indigo-600 text-slate-950 font-bold text-xs uppercase tracking-wider flex items-center justify-center gap-2 shadow-lg shadow-cyan-500/20 active:scale-95 transition-all disabled:opacity-60"
          >
            {isSubmitting ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <>
                <span>Sign In to Arena</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        {/* Demo login options */}
        <div className="mt-6 pt-5 border-t border-slate-800">
          <p className="text-[11px] text-slate-400 mb-2.5 flex items-center justify-center gap-1.5 font-medium">
            <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
            <span>Instant 1-Click Demo Profiles:</span>
          </p>
          <div className="grid grid-cols-2 gap-2">
            <button
              type="button"
              disabled={isSubmitting}
              onClick={() => handleDemoLogin("algo_ninja")}
              className="px-3 py-2 rounded-xl bg-[#0B1220] hover:bg-slate-800/80 border border-slate-700/60 text-xs text-slate-300 hover:text-cyan-300 font-medium transition-colors text-center"
            >
              🥷 Ninja Coder
            </button>
            <button
              type="button"
              disabled={isSubmitting}
              onClick={() => handleDemoLogin("byte_master")}
              className="px-3 py-2 rounded-xl bg-[#0B1220] hover:bg-slate-800/80 border border-slate-700/60 text-xs text-slate-300 hover:text-cyan-300 font-medium transition-colors text-center"
            >
              ⚡ Byte Master
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
  );
}

export default function LoginPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center text-slate-400 text-sm">
          Loading sign in...
        </div>
      }
    >
      <LoginForm />
    </Suspense>
  );
}
