"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "../../lib/authContext";
import {
  Code2,
  Flame,
  Zap,
  Compass,
  BookOpen,
  Settings,
  Trophy,
  ListTodo,
  BarChart3,
  GraduationCap,
  Sparkles,
  Swords,
  Building2,
  Briefcase,
  Menu,
  X,
  MessageSquareQuote,
  LogOut,
  UserPlus,
  Github,
} from "lucide-react";

export default function Navbar() {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { user, logout } = useAuth();

  // Close menu on Escape key and prevent background scroll
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setMobileMenuOpen(false);
      }
    };

    if (mobileMenuOpen) {
      window.addEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "";
    };
  }, [mobileMenuOpen]);

  const primaryLinks = [
    { href: "/problems", label: "Problems", icon: BookOpen },
    { href: "/roadmap", label: "Roadmap 3D", icon: Compass },
    { href: "/battles", label: "1v1 Battle", icon: Swords },
    { href: "/lists", label: "Lists", icon: ListTodo },
    { href: "/contests", label: "Contests", icon: Trophy },
    { href: "/patterns", label: "Patterns", icon: Sparkles },
    { href: "/companies", label: "Companies", icon: Building2 },
    { href: "/interviews", label: "Interviews", icon: MessageSquareQuote },
    { href: "/placement", label: "Placement", icon: GraduationCap },
    { href: "/jobs", label: "Jobs", icon: Briefcase },
    { href: "/analytics", label: "Analytics", icon: BarChart3 },
  ];

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 h-16 w-full backdrop-blur-md bg-[#0B1220]/95 border-b border-slate-800/80 px-4 lg:px-8 transition-all flex items-center">
      <div className="max-w-7xl mx-auto w-full flex items-center justify-between gap-4">
        {/* Brand */}
        <Link
          href="/"
          onClick={() => setMobileMenuOpen(false)}
          className="flex items-center gap-2.5 group shrink-0 min-h-[44px]"
        >
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-cyan-400 to-violet-600 flex items-center justify-center shadow-lg shadow-cyan-500/20 group-hover:scale-105 transition-transform">
            <Code2 className="w-5 h-5 text-slate-950 stroke-[2.5]" />
          </div>
          <div className="flex flex-col">
            <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-white via-cyan-200 to-cyan-400 bg-clip-text text-transparent">
              Ready2Code
            </span>
            <span className="text-[9px] text-cyan-400/80 uppercase tracking-widest font-mono">
              3D DSA Arena
            </span>
          </div>
        </Link>

        {/* Center Desktop Navigation Links (Visible on >= 768px) */}
        <div className="hidden md:flex items-center gap-0.5 bg-[#121C2F]/80 p-1 rounded-full border border-slate-800 text-xs">
          {primaryLinks.slice(0, 8).map((link) => {
            const Icon = link.icon;
            const isActive = pathname === link.href || (link.href !== "/" && pathname.startsWith(link.href));
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full font-medium transition-all ${
                  isActive
                    ? "bg-gradient-to-r from-cyan-500/20 to-violet-500/20 text-cyan-300 border border-cyan-500/30 shadow-sm shadow-cyan-500/20"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? "text-cyan-400" : "text-slate-400"}`} />
                <span>{link.label}</span>
              </Link>
            );
          })}
        </div>

        {/* Right Status & Profile Controls */}
        <div className="flex items-center gap-2 shrink-0">
          {/* Daily Streak */}
          <Link
            href="/daily"
            className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-semibold hover:bg-amber-500/20 transition-all min-h-[44px]"
            title={user ? `Current Streak: ${user.streak} days` : "Sign in to track your streak"}
          >
            <Flame className={`w-4 h-4 ${user && user.streak > 0 ? "fill-amber-500 text-amber-500" : "text-amber-500/70"}`} />
            <span className="hidden sm:inline">{user ? `${user.streak} Days` : "0 Days"}</span>
          </Link>

          {/* XP Leaderboard */}
          <Link
            href="/leaderboard"
            className="hidden sm:flex items-center gap-1.5 px-2.5 py-1.5 rounded-full bg-violet-500/10 border border-violet-500/30 text-violet-300 text-xs font-semibold hover:bg-violet-500/20 transition-all min-h-[44px]"
            title="Total XP"
          >
            <Zap className="w-4 h-4 fill-violet-400 text-violet-400" />
            <span>{user ? `${user.xp} XP` : "0 XP"}</span>
          </Link>

          {/* Settings */}
          <Link
            href="/settings"
            className="hidden sm:flex items-center justify-center min-w-[44px] min-h-[44px] rounded-xl text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
            title="Settings"
            aria-label="Settings"
          >
            <Settings className="w-4 h-4" />
          </Link>

          {/* GitHub Repository */}
          <a
            href="https://github.com/sayantandutta-18/Ready2Code"
            target="_blank"
            rel="noreferrer"
            className="hidden sm:flex items-center justify-center min-w-[44px] min-h-[44px] rounded-xl text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
            title="GitHub Repository"
            aria-label="GitHub Repository"
          >
            <Github className="w-4 h-4" />
          </a>

          {/* User Account / Profile or Sign In / Register (Desktop) */}
          {user ? (
            <div className="hidden sm:flex items-center gap-1.5">
              <Link
                href={`/profile/${user.username}`}
                className="flex items-center gap-1.5 pl-1.5 pr-3 py-1 rounded-full bg-slate-800/60 hover:bg-slate-800 border border-slate-700/60 transition-colors min-h-[44px]"
                title={`Profile: ${user.display_name || user.username}`}
              >
                <div className="w-7 h-7 rounded-full bg-gradient-to-tr from-cyan-400 to-indigo-500 flex items-center justify-center font-bold text-xs text-slate-950 uppercase">
                  {user.username.slice(0, 1)}
                </div>
                <span className="text-xs font-medium text-slate-300 max-w-[90px] truncate">
                  {user.display_name || user.username}
                </span>
              </Link>
              <button
                onClick={logout}
                className="min-w-[44px] min-h-[44px] flex items-center justify-center rounded-xl text-slate-400 hover:text-red-400 hover:bg-slate-800 transition-colors"
                title="Sign Out"
                aria-label="Sign Out"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <div className="hidden sm:flex items-center gap-2">
              <Link
                href="/login"
                className="min-h-[44px] px-3.5 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800 text-xs font-semibold flex items-center transition-colors"
              >
                Sign In
              </Link>
              <Link
                href="/register"
                className="min-h-[44px] flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-500 hover:from-cyan-400 hover:to-indigo-400 text-slate-950 font-bold text-xs shadow-md shadow-cyan-500/20 transition-all active:scale-95"
              >
                <UserPlus className="w-3.5 h-3.5" />
                <span>Register</span>
              </Link>
            </div>
          )}

          {/* Mobile Menu Hamburger Button (Below 768px, exactly 44x44px target) */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden min-w-[44px] min-h-[44px] flex items-center justify-center rounded-xl text-slate-300 hover:text-white hover:bg-slate-800 transition-colors focus:ring-2 focus:ring-cyan-400"
            aria-label={mobileMenuOpen ? "Close menu" : "Open menu"}
            aria-expanded={mobileMenuOpen}
          >
            {mobileMenuOpen ? (
              <X className="w-6 h-6 text-cyan-400" />
            ) : (
              <Menu className="w-6 h-6" />
            )}
          </button>
        </div>
      </div>

      {/* Full-Screen Mobile Menu Drawer (Below 768px) */}
      {mobileMenuOpen && (
        <div
          role="dialog"
          aria-modal="true"
          aria-label="Mobile Navigation Menu"
          className="fixed inset-0 top-16 z-50 bg-[#0B1220] overflow-y-auto p-5 flex flex-col justify-between animate-in fade-in slide-in-from-top-4 duration-200 md:hidden pb-10"
        >
          <div className="flex flex-col gap-1.5">
            <div className="text-[11px] font-mono uppercase tracking-widest text-slate-500 px-3 py-1">
              Arena Navigation
            </div>
            {primaryLinks.map((link) => {
              const Icon = link.icon;
              const isActive = pathname === link.href || (link.href !== "/" && pathname.startsWith(link.href));
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`min-h-[44px] flex items-center gap-3 px-4 py-2.5 rounded-xl text-base font-medium transition-all ${
                    isActive
                      ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/30"
                      : "text-slate-300 hover:text-white hover:bg-slate-800/60"
                  }`}
                >
                  <Icon className="w-5 h-5 text-cyan-400 shrink-0" />
                  <span>{link.label}</span>
                </Link>
              );
            })}

            <div className="pt-3 border-t border-slate-800/80 mt-2 flex flex-col gap-1.5">
              <Link
                href="/daily"
                onClick={() => setMobileMenuOpen(false)}
                className="min-h-[44px] flex items-center justify-between px-4 py-2.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-300 text-base font-medium"
              >
                <div className="flex items-center gap-3">
                  <Flame className="w-5 h-5 text-amber-400" />
                  <span>Daily Challenge</span>
                </div>
                <span className="text-xs font-mono">{user ? `${user.streak} Days` : "0 Days"}</span>
              </Link>

              <Link
                href="/leaderboard"
                onClick={() => setMobileMenuOpen(false)}
                className="min-h-[44px] flex items-center justify-between px-4 py-2.5 rounded-xl bg-violet-500/10 border border-violet-500/20 text-violet-300 text-base font-medium"
              >
                <div className="flex items-center gap-3">
                  <Zap className="w-5 h-5 text-violet-400" />
                  <span>XP Leaderboard</span>
                </div>
                <span className="text-xs font-mono">{user ? `${user.xp} XP` : "0 XP"}</span>
              </Link>

              <Link
                href="/settings"
                onClick={() => setMobileMenuOpen(false)}
                className="min-h-[44px] flex items-center gap-3 px-4 py-2.5 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/60 text-base font-medium"
              >
                <Settings className="w-5 h-5 text-slate-400" />
                <span>Settings</span>
              </Link>
            </div>
          </div>

          {/* Account Actions at bottom */}
          <div className="pt-6 border-t border-slate-800/80 mt-6 flex flex-col gap-3">
            {user ? (
              <div className="flex flex-col gap-2">
                <Link
                  href={`/profile/${user.username}`}
                  onClick={() => setMobileMenuOpen(false)}
                  className="min-h-[44px] flex items-center gap-3 px-4 py-2.5 rounded-xl bg-slate-800/80 text-white font-medium"
                >
                  <div className="w-7 h-7 rounded-full bg-cyan-400 text-slate-950 font-bold flex items-center justify-center uppercase text-sm">
                    {user.username.slice(0, 1)}
                  </div>
                  <div className="truncate flex-1">
                    <div className="text-sm font-semibold">{user.display_name || user.username}</div>
                    <div className="text-xs text-slate-400 font-mono">@{user.username}</div>
                  </div>
                </Link>
                <button
                  onClick={() => {
                    logout();
                    setMobileMenuOpen(false);
                  }}
                  className="min-h-[44px] w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 font-semibold text-sm hover:bg-red-500/20"
                >
                  <LogOut className="w-4 h-4" />
                  <span>Sign Out</span>
                </button>
              </div>
            ) : (
              <div className="flex flex-col gap-2.5">
                <Link
                  href="/login"
                  onClick={() => setMobileMenuOpen(false)}
                  className="min-h-[44px] flex items-center justify-center text-center px-4 py-2.5 rounded-xl bg-slate-800 border border-slate-700 text-sm font-bold text-slate-200"
                >
                  Sign In
                </Link>
                <Link
                  href="/register"
                  onClick={() => setMobileMenuOpen(false)}
                  className="min-h-[44px] flex items-center justify-center text-center px-4 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-500 text-slate-950 text-sm font-extrabold shadow-lg shadow-cyan-500/20"
                >
                  Create Account
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}
