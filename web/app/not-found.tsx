import React from "react";
import Link from "next/link";
import { Compass, BookOpen, Home, ArrowRight, Code2 } from "lucide-react";

export default function NotFound() {
  return (
    <div className="min-h-[75vh] flex items-center justify-center px-4 py-16">
      <div className="max-w-md w-full bg-slate-900/80 border border-slate-800 rounded-2xl p-8 text-center space-y-6 shadow-2xl backdrop-blur-md">
        <div className="relative">
          <div className="w-20 h-20 mx-auto rounded-3xl bg-gradient-to-br from-cyan-400/20 via-violet-500/20 to-indigo-500/20 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
            <Compass className="w-10 h-10 animate-spin" style={{ animationDuration: "12s" }} />
          </div>
          <span className="absolute -bottom-2 left-1/2 -translate-x-1/2 px-2.5 py-0.5 rounded-full bg-slate-800 border border-slate-700 font-mono text-[11px] font-bold text-cyan-300">
            404
          </span>
        </div>

        <div className="space-y-2">
          <h1 className="text-2xl font-black text-white tracking-tight">Node Not Found in Graph</h1>
          <p className="text-xs text-slate-400 leading-relaxed">
            The page or problem you are traversing to does not exist or has been relocated to another dimension.
          </p>
        </div>

        <div className="pt-2 flex flex-col sm:flex-row gap-3 justify-center">
          <Link
            href="/problems"
            className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-400 to-indigo-500 hover:from-cyan-500 hover:to-indigo-600 text-slate-950 font-bold text-xs uppercase tracking-wider shadow-lg shadow-cyan-500/20 active:scale-95 transition-all"
          >
            <BookOpen className="w-4 h-4" />
            <span>Browse Problems</span>
          </Link>
          <Link
            href="/"
            className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs uppercase tracking-wider transition-all"
          >
            <Home className="w-4 h-4" />
            <span>Home</span>
          </Link>
        </div>
      </div>
    </div>
  );
}
