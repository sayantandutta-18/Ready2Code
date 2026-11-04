import React from "react";

interface DifficultyChipProps {
  difficulty: "easy" | "medium" | "hard" | string;
  className?: string;
}

export default function DifficultyChip({ difficulty, className = "" }: DifficultyChipProps) {
  const d = (difficulty || "easy").toLowerCase();

  const styles = {
    easy: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20 shadow-emerald-500/10",
    medium: "text-amber-400 bg-amber-500/10 border-amber-500/20 shadow-amber-500/10",
    hard: "text-rose-400 bg-rose-500/10 border-rose-500/20 shadow-rose-500/10",
  }[d] || "text-slate-400 bg-slate-800 border-slate-700";

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold uppercase tracking-wider border shadow-sm ${styles} ${className}`}
    >
      {d}
    </span>
  );
}
