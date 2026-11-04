"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Code2,
  Flame,
  Zap,
  Compass,
  BookOpen,
  Settings,
  PlaySquare,
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
  MessageSquareQuote
} from "lucide-react";

export default function Navbar() {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

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
    <nav className="sticky top-0 z-50 w-full backdrop-blur-md bg-[#0B1220]/90 border-b border-slate-800/80 px-4 lg:px-8 py-2.5 transition-all">
      <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
        {/* Brand */}
        <Link href="/" className="flex items-center gap-2.5 group shrink-0">
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

        {/* Center Desktop Navigation Links */}
        <div className="hidden lg:flex items-center gap-0.5 bg-[#121C2F]/80 p-1 rounded-full border border-slate-800 text-xs">
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

        {/* Right Status & Profile */}
        <div className="flex items-center gap-2 shrink-0">
          {/* Daily Streak */}
          <Link
            href="/daily"
            className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-semibold hover:bg-amber-500/20 transition-all"
          >
            <Flame className="w-3.5 h-3.5 fill-amber-500 text-amber-500" />
            <span className="hidden sm:inline">3 Days</span>
          </Link>

          {/* XP Leaderboard */}
          <Link
            href="/leaderboard"
            className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-violet-500/10 border border-violet-500/30 text-violet-300 text-xs font-semibold hover:bg-violet-500/20 transition-all"
          >
            <Zap className="w-3.5 h-3.5 fill-violet-400 text-violet-400" />
            <span>185 XP</span>
          </Link>

          {/* Settings */}
          <Link
            href="/settings"
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
          >
            <Settings className="w-4 h-4" />
          </Link>

          {/* Profile */}
          <Link
            href="/portfolio/coder_alex"
            className="flex items-center gap-1.5 pl-1 pr-2.5 py-1 rounded-full bg-slate-800/60 hover:bg-slate-800 border border-slate-700/60 transition-colors"
          >
            <div className="w-6 h-6 rounded-full bg-gradient-to-tr from-cyan-400 to-indigo-500 flex items-center justify-center font-bold text-xs text-slate-950">
              A
            </div>
            <span className="text-xs font-medium text-slate-300 hidden md:inline">Portfolio</span>
          </Link>

          {/* Mobile Menu Hamburger Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="lg:hidden p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            aria-label="Toggle navigation menu"
          >
            {mobileMenuOpen ? <X className="w-5 h-5 text-cyan-400" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu Drawer */}
      {mobileMenuOpen && (
        <div className="lg:hidden mt-3 pt-3 border-t border-slate-800/80 grid grid-cols-2 sm:grid-cols-3 gap-1.5 pb-2 animate-in slide-in-from-top duration-150">
          {primaryLinks.map((link) => {
            const Icon = link.icon;
            const isActive = pathname === link.href || (link.href !== "/" && pathname.startsWith(link.href));
            return (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setMobileMenuOpen(false)}
                className={`flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-medium transition-all ${
                  isActive
                    ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/30"
                    : "text-slate-400 hover:text-white hover:bg-slate-800/60"
                }`}
              >
                <Icon className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
                <span className="truncate">{link.label}</span>
              </Link>
            );
          })}
        </div>
      )}
    </nav>
  );
}
