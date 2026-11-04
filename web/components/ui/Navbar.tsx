"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Code2, Flame, Zap, Compass, BookOpen, User, Settings, PlaySquare } from "lucide-react";

export default function Navbar() {
  const pathname = usePathname();

  const navLinks = [
    { href: "/problems", label: "Problems", icon: BookOpen },
    { href: "/roadmap", label: "Roadmap 3D", icon: Compass },
    { href: "/daily", label: "Daily Challenge", icon: Flame },
    { href: "/visualizer/two-sum", label: "3D Visualizer", icon: PlaySquare },
  ];

  return (
    <nav className="sticky top-0 z-50 w-full backdrop-blur-md bg-[#0B1220]/80 border-b border-slate-800/80 px-4 lg:px-8 py-3.5 transition-all">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* Brand */}
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-400 to-violet-600 flex items-center justify-center shadow-lg shadow-cyan-500/20 group-hover:scale-105 transition-transform">
            <Code2 className="w-6 h-6 text-slate-950 stroke-[2.5]" />
          </div>
          <div className="flex flex-col">
            <span className="font-extrabold text-xl tracking-tight bg-gradient-to-r from-white via-cyan-200 to-cyan-400 bg-clip-text text-transparent">
              Ready2Code
            </span>
            <span className="text-[10px] text-cyan-400/80 uppercase tracking-widest font-mono">
              3D DSA Arena
            </span>
          </div>
        </Link>

        {/* Center Navigation */}
        <div className="hidden md:flex items-center gap-1.5 bg-[#121C2F]/80 p-1 rounded-full border border-slate-800">
          {navLinks.map((link) => {
            const Icon = link.icon;
            const isActive = pathname === link.href || (link.href !== "/" && pathname.startsWith(link.href));
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`flex items-center gap-2 px-4 py-1.5 rounded-full text-sm font-medium transition-all ${
                  isActive
                    ? "bg-gradient-to-r from-cyan-500/20 to-violet-500/20 text-cyan-300 border border-cyan-500/30 shadow-sm shadow-cyan-500/20"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? "text-cyan-400" : "text-slate-400"}`} />
                {link.label}
              </Link>
            );
          })}
        </div>

        {/* Right Status & Profile */}
        <div className="flex items-center gap-3">
          {/* Streak pill */}
          <Link
            href="/daily"
            className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-semibold hover:bg-amber-500/20 transition-all"
            title="Current Streak: 3 Days"
          >
            <Flame className="w-4 h-4 fill-amber-500 text-amber-500" />
            <span>3 Days</span>
          </Link>

          {/* XP Badge */}
          <div className="hidden sm:flex items-center gap-1.5 px-3 py-1 rounded-full bg-violet-500/10 border border-violet-500/30 text-violet-300 text-xs font-semibold">
            <Zap className="w-3.5 h-3.5 fill-violet-400 text-violet-400" />
            <span>185 XP</span>
          </div>

          {/* Settings */}
          <Link
            href="/settings"
            className="p-2 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
            title="Settings"
          >
            <Settings className="w-5 h-5" />
          </Link>

          {/* User profile */}
          <Link
            href="/profile/coder_alex"
            className="flex items-center gap-2 pl-1 pr-3 py-1 rounded-full bg-slate-800/60 hover:bg-slate-800 border border-slate-700/60 transition-colors"
          >
            <div className="w-7 h-7 rounded-full bg-gradient-to-tr from-cyan-500 to-indigo-500 flex items-center justify-center font-bold text-xs text-slate-950">
              A
            </div>
            <span className="text-xs font-medium text-slate-300 hidden lg:inline">coder_alex</span>
          </Link>
        </div>
      </div>
    </nav>
  );
}
