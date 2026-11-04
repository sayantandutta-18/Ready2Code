import React from "react";

export interface LoadingSkeletonProps {
  rows?: number;
  className?: string;
  variant?: "table" | "card" | "title";
}

export default function LoadingSkeleton({
  rows = 4,
  className = "",
  variant = "table",
}: LoadingSkeletonProps) {
  if (variant === "title") {
    return (
      <div
        className={`h-8 w-48 rounded-xl bg-slate-800/80 border border-slate-700/50 animate-pulse ${className}`}
        role="status"
        aria-label="Loading content"
      >
        <span className="sr-only">Loading...</span>
      </div>
    );
  }

  if (variant === "card") {
    return (
      <div
        className={`w-full h-40 rounded-2xl bg-slate-850/60 border border-slate-800 animate-pulse p-6 flex flex-col justify-between ${className}`}
        role="status"
        aria-label="Loading content"
      >
        <div className="space-y-3">
          <div className="h-5 w-1/3 rounded bg-slate-800" />
          <div className="h-4 w-2/3 rounded bg-slate-800/60" />
        </div>
        <div className="h-8 w-1/4 rounded bg-slate-800/50" />
        <span className="sr-only">Loading...</span>
      </div>
    );
  }

  return (
    <div
      className={`w-full space-y-3 animate-pulse ${className}`}
      role="status"
      aria-label="Loading content"
    >
      {Array.from({ length: rows }).map((_, i) => (
        <div
          key={i}
          className="h-12 w-full rounded-xl bg-slate-800/60 border border-slate-700/40"
          style={{ opacity: Math.max(0.3, 1 - i * 0.15) }}
        />
      ))}
      <span className="sr-only">Loading...</span>
    </div>
  );
}
