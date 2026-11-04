import React from "react";
import { AlertCircle, RotateCcw } from "lucide-react";

interface QueryErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
}

export default function QueryErrorState({
  title = "Failed to load data",
  message = "We encountered an issue communicating with the Ready2Code backend. Please check your connection and retry.",
  onRetry,
}: QueryErrorStateProps) {
  return (
    <div className="w-full py-12 px-6 rounded-2xl bg-rose-950/20 border border-rose-500/30 flex flex-col items-center justify-center text-center space-y-4 my-4">
      <div className="w-12 h-12 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-center justify-center text-rose-400">
        <AlertCircle className="w-6 h-6" />
      </div>
      <div className="space-y-1 max-w-md">
        <h3 className="text-sm font-bold text-rose-200">{title}</h3>
        <p className="text-xs text-rose-300/80 leading-relaxed">{message}</p>
      </div>
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-rose-500/20 hover:bg-rose-500/30 text-rose-200 border border-rose-500/40 text-xs font-semibold transition-all active:scale-95"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>Retry</span>
        </button>
      )}
    </div>
  );
}
