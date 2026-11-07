"use client";

import React, { useState, useEffect } from "react";
import { useAuth } from "../../lib/authContext";
import Input from "./Input";
import { X, Code2, Sparkles, User, ArrowRight, Loader2, Lock } from "lucide-react";

export default function AuthModal() {
  const { isAuthModalOpen, closeAuthModal, login, register } = useAuth();
  const [tab, setTab] = useState<"login" | "register">("login");
  const [username, setUsername] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isAuthModalOpen) {
        closeAuthModal();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isAuthModalOpen, closeAuthModal]);

  if (!isAuthModalOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg("");
    if (!username.trim()) {
      setErrorMsg("Please enter a username.");
      return;
    }

    setIsSubmitting(true);
    try {
      if (tab === "login") {
        await login(username.trim());
      } else {
        await register(username.trim(), undefined, displayName.trim() || undefined);
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Authentication failed. Please try again.";
      setErrorMsg(msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleQuickLogin = async (demoUsername: string) => {
    setErrorMsg("");
    setIsSubmitting(true);
    try {
      await login(demoUsername);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Demo sign in failed.";
      setErrorMsg(msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="auth-modal-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-in fade-in duration-150"
    >
      <div
        className="w-full max-w-md bg-[#121C2F] border border-slate-800 rounded-2xl shadow-2xl p-6 relative overflow-hidden text-slate-200"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Glow accent */}
        <div className="absolute -top-16 -right-16 w-36 h-36 bg-cyan-500/20 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -bottom-16 -left-16 w-36 h-36 bg-indigo-500/20 rounded-full blur-3xl pointer-events-none" />

        {/* Close Button */}
        <button
          onClick={closeAuthModal}
          className="absolute top-4 right-4 p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          aria-label="Close modal"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Brand Header */}
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-400 to-violet-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
            <Code2 className="w-5 h-5 text-slate-950 stroke-[2.5]" />
          </div>
          <div>
            <h2 id="auth-modal-title" className="text-lg font-black text-white tracking-tight">
              Ready2Code Account
            </h2>
            <p className="text-xs text-slate-400">
              Sign in to record your streak, submissions, and notes.
            </p>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex bg-[#0B1220] p-1 rounded-xl mb-5 border border-slate-800">
          <button
            type="button"
            onClick={() => {
              setTab("login");
              setErrorMsg("");
            }}
            className={`flex-1 py-1.5 text-xs font-semibold rounded-lg transition-all ${
              tab === "login"
                ? "bg-gradient-to-r from-cyan-500/20 to-violet-500/20 text-cyan-300 border border-cyan-500/30 shadow-sm"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Sign In
          </button>
          <button
            type="button"
            onClick={() => {
              setTab("register");
              setErrorMsg("");
            }}
            className={`flex-1 py-1.5 text-xs font-semibold rounded-lg transition-all ${
              tab === "register"
                ? "bg-gradient-to-r from-cyan-500/20 to-violet-500/20 text-cyan-300 border border-cyan-500/30 shadow-sm"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Create Account
          </button>
        </div>

        {/* Error message */}
        {errorMsg && (
          <div className="mb-4 p-3 rounded-xl bg-red-500/10 border border-red-500/30 text-xs text-red-400">
            {errorMsg}
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-3.5">
          <Input
            label="Username"
            type="text"
            required
            placeholder="e.g. algo_master"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            leftIcon={<User className="w-4 h-4" />}
            className="font-mono text-sm py-2"
          />

          {tab === "register" && (
            <Input
              label="Display Name (Optional)"
              type="text"
              placeholder="e.g. Alex Chen"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              className="text-sm py-2"
            />
          )}

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-500 hover:from-cyan-600 hover:to-indigo-600 text-slate-950 font-bold text-xs uppercase tracking-wider flex items-center justify-center gap-2 shadow-lg shadow-cyan-500/20 active:scale-95 transition-all disabled:opacity-60"
          >
            {isSubmitting ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <>
                <span>{tab === "login" ? "Sign In" : "Get Started"}</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        {/* One-click demo sign in */}
        <div className="mt-5 pt-4 border-t border-slate-800">
          <p className="text-[11px] text-slate-400 mb-2 flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
            <span>Or continue with one-click demo coder:</span>
          </p>
          <div className="flex gap-2">
            <button
              type="button"
              disabled={isSubmitting}
              onClick={() => handleQuickLogin("algo_ninja")}
              className="flex-1 px-2.5 py-1.5 rounded-lg bg-[#0B1220] hover:bg-slate-800 border border-slate-700/60 text-xs text-slate-300 font-medium transition-colors text-center"
            >
              Ninja Coder
            </button>
            <button
              type="button"
              disabled={isSubmitting}
              onClick={() => handleQuickLogin("byte_master")}
              className="flex-1 px-2.5 py-1.5 rounded-lg bg-[#0B1220] hover:bg-slate-800 border border-slate-700/60 text-xs text-slate-300 font-medium transition-colors text-center"
            >
              Byte Master
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
