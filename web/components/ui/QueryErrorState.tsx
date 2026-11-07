import React from "react";
import { AlertCircle, RotateCcw, Terminal } from "lucide-react";

interface QueryErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
}

export default function QueryErrorState({
  title = "Failed to load data",
  message,
  onRetry,
}: QueryErrorStateProps) {
  const isNetworkOrConnectionError =
    !message ||
    message.toLowerCase().includes("fetch") ||
    message.toLowerCase().includes("network") ||
    message.toLowerCase().includes("connection") ||
    message.toLowerCase().includes("failed") ||
    message.toLowerCase().includes("econrefused");

  const displayMessage = message || "Unable to reach the Ready2Code API backend.";

  return (
    <div className="w-full py-12 px-6 rounded-2xl bg-rose-950/20 border border-rose-500/30 flex flex-col items-center justify-center text-center space-y-4 my-4">
      <div className="w-12 h-12 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-center justify-center text-rose-400">
        <AlertCircle className="w-6 h-6" />
      </div>
      <div className="space-y-2 max-w-lg">
        <h3 className="text-sm font-bold text-rose-200">{title}</h3>
        <p className="text-xs text-rose-300/80 leading-relaxed">{displayMessage}</p>

        {isNetworkOrConnectionError && (
          <div className="p-3 mt-2 rounded-xl bg-[#0B1220] border border-rose-900/60 text-left text-[11px] text-slate-300 space-y-1 font-mono">
            <div className="flex items-center gap-1.5 text-rose-400 font-sans font-semibold">
              <Terminal className="w-3.5 h-3.5" />
              <span>How to start the local API backend:</span>
            </div>
            <div className="text-cyan-300">python -m uvicorn app.main:app --app-dir api --port 8000</div>
            <div className="text-slate-500 text-[10px]">Ensure NEXT_PUBLIC_API_URL=http://localhost:8000 in web/.env.local</div>
          </div>
        )}
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
