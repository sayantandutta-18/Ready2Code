import React from "react";
import { CheckCircle2, XCircle, Clock, AlertTriangle, FileCode } from "lucide-react";

interface VerdictBadgeProps {
  verdict: "AC" | "WA" | "TLE" | "RE" | "CE" | string;
  size?: "sm" | "md" | "lg";
}

export default function VerdictBadge({ verdict, size = "md" }: VerdictBadgeProps) {
  const v = (verdict || "AC").toUpperCase();

  const configs: Record<string, { label: string; bg: string; text: string; border: string; glow: string; icon: any }> = {
    AC: {
      label: "Accepted",
      bg: "bg-emerald-500/15",
      text: "text-emerald-400",
      border: "border-emerald-500/30",
      glow: "shadow-[0_0_20px_rgba(34,197,94,0.35)]",
      icon: CheckCircle2,
    },
    WA: {
      label: "Wrong Answer",
      bg: "bg-rose-500/15",
      text: "text-rose-400",
      border: "border-rose-500/30",
      glow: "shadow-[0_0_20px_rgba(244,63,94,0.35)]",
      icon: XCircle,
    },
    TLE: {
      label: "Time Limit Exceeded",
      bg: "bg-amber-500/15",
      text: "text-amber-400",
      border: "border-amber-500/30",
      glow: "shadow-[0_0_20px_rgba(245,158,11,0.35)]",
      icon: Clock,
    },
    RE: {
      label: "Runtime Error",
      bg: "bg-orange-500/15",
      text: "text-orange-400",
      border: "border-orange-500/30",
      glow: "shadow-[0_0_20px_rgba(249,115,22,0.35)]",
      icon: AlertTriangle,
    },
    CE: {
      label: "Compilation Error",
      bg: "bg-purple-500/15",
      text: "text-purple-400",
      border: "border-purple-500/30",
      glow: "shadow-[0_0_20px_rgba(168,85,247,0.35)]",
      icon: FileCode,
    },
  };

  const item = configs[v] || configs["WA"];
  const Icon = item.icon;

  const sizeClasses = {
    sm: "px-2 py-0.5 text-xs gap-1",
    md: "px-3 py-1 text-sm gap-1.5",
    lg: "px-4 py-1.5 text-base gap-2 font-bold",
  }[size];

  return (
    <span
      className={`inline-flex items-center rounded-lg border font-semibold ${item.bg} ${item.text} ${item.border} ${item.glow} ${sizeClasses} transition-all`}
    >
      <Icon className={size === "sm" ? "w-3.5 h-3.5" : "w-4 h-4"} />
      <span>{item.label}</span>
    </span>
  );
}
