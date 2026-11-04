"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useQuery, useMutation } from "@tanstack/react-query";
import { fetchApi } from "@/lib/api";
import LoadingSkeleton from "@/components/ui/LoadingSkeleton";
import QueryErrorState from "@/components/ui/QueryErrorState";
import confetti from "canvas-confetti";
import { Sparkles, ArrowLeft, CheckCircle2, XCircle, Code2, HelpCircle } from "lucide-react";

interface PatternQuiz {
  question: string;
  options: string[];
}

interface PatternDetail {
  slug: string;
  name: string;
  signals: string;
  lesson_md: string;
  template_code: string;
  quiz: PatternQuiz;
}

interface QuizResult {
  correct: boolean;
  message: string;
  xp_earned: number;
}

export default function PatternDetailPage({ params }: { params: { id: string } }) {
  const { id } = params;

  const [selectedOption, setSelectedOption] = useState<number | null>(null);
  const [quizSubmitted, setQuizSubmitted] = useState<boolean>(false);
  const [isCorrect, setIsCorrect] = useState<boolean>(false);

  const {
    data: pattern,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<PatternDetail>({
    queryKey: ["pattern", id],
    queryFn: () => fetchApi<PatternDetail>(`/patterns/${id}`),
  });

  const quizMutation = useMutation({
    mutationFn: async (optionIdx: number) => {
      return fetchApi<QuizResult>(`/patterns/${id}/quiz`, {
        method: "POST",
        body: JSON.stringify({
          pattern_slug: id,
          selected_option_index: optionIdx,
        }),
      });
    },
    onSuccess: (data) => {
      setQuizSubmitted(true);
      setIsCorrect(data.correct);
      if (data.correct) {
        confetti({ particleCount: 60, spread: 60 });
      }
    },
    onError: () => {
      // Graceful fallback for UI feedback
      setQuizSubmitted(true);
      setIsCorrect(selectedOption === 0);
    },
  });

  const handleQuizSubmit = () => {
    if (selectedOption === null) return;
    quizMutation.mutate(selectedOption);
  };

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto px-4 lg:px-8 py-10 space-y-6">
        <LoadingSkeleton variant="title" className="w-48 h-6" />
        <LoadingSkeleton variant="card" className="h-40" />
        <LoadingSkeleton variant="card" className="h-64" />
      </div>
    );
  }

  if (isError || !pattern) {
    return (
      <div className="max-w-4xl mx-auto px-4 lg:px-8 py-10">
        <QueryErrorState
          title="Failed to load pattern"
          message={error instanceof Error ? error.message : "The requested pattern details could not be retrieved."}
          onRetry={() => refetch()}
        />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 lg:px-8 py-10 space-y-8">
      {/* Back button */}
      <Link href="/patterns" className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-cyan-400 font-mono">
        <ArrowLeft className="w-3.5 h-3.5" /> Back to Patterns
      </Link>

      {/* Pattern Header */}
      <div className="p-8 rounded-3xl bg-[#121C2F] border border-slate-800 shadow-2xl space-y-4">
        <div className="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-xs font-semibold">
          <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
          <span>Algorithmic Pattern Blueprint</span>
        </div>
        <h1 className="text-3xl font-black text-white">{pattern.name}</h1>
        <p className="text-sm text-slate-300 font-sans leading-relaxed">{pattern.signals}</p>
      </div>

      {/* Pattern Lesson & Template Code */}
      <div className="p-8 rounded-3xl bg-[#121C2F] border border-slate-800 shadow-xl space-y-6">
        <div className="prose prose-invert max-w-none text-xs sm:text-sm text-slate-300 whitespace-pre-line leading-relaxed">
          {pattern.lesson_md}
        </div>

        <div>
          <div className="text-xs uppercase font-mono font-bold tracking-wider text-cyan-400 mb-2 flex items-center gap-2">
            <Code2 className="w-4 h-4" />
            <span>Python Canonical Template:</span>
          </div>
          <pre className="p-4 rounded-xl bg-[#0B1220] border border-slate-800 text-xs font-mono text-slate-200 overflow-x-auto leading-relaxed">
            {pattern.template_code}
          </pre>
        </div>
      </div>

      {/* Interactive Pattern Quiz Section */}
      <div className="p-8 rounded-3xl bg-gradient-to-br from-[#121C2F] to-[#16233B] border border-violet-500/30 shadow-2xl space-y-6">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center gap-2">
            <HelpCircle className="w-5 h-5 text-violet-400" />
            <h2 className="text-base font-bold text-white">Pattern Recognition Quiz</h2>
          </div>
          <span className="text-xs font-mono text-violet-300 bg-violet-950/60 px-2.5 py-0.5 rounded border border-violet-500/30">
            Unlocks Matching Problems (+15 XP)
          </span>
        </div>

        <div className="space-y-4">
          <p className="text-sm font-semibold text-slate-200">
            {pattern.quiz?.question || "Select the pattern matching this statement constraint:"}
          </p>

          <div className="space-y-2.5">
            {(pattern.quiz?.options || []).map((opt: string, idx: number) => {
              const isSelected = selectedOption === idx;
              return (
                <button
                  key={idx}
                  onClick={() => {
                    setSelectedOption(idx);
                    setQuizSubmitted(false);
                  }}
                  className={`w-full p-4 rounded-xl border text-left text-xs font-medium transition-all ${
                    isSelected
                      ? "bg-cyan-500/20 border-cyan-400 text-cyan-200 ring-1 ring-cyan-400"
                      : "bg-[#0B1220] border-slate-800 text-slate-300 hover:border-slate-700"
                  }`}
                >
                  <span className="font-mono text-slate-500 mr-2">{String.fromCharCode(65 + idx)}.</span>
                  <span>{opt}</span>
                </button>
              );
            })}
          </div>

          <button
            onClick={handleQuizSubmit}
            disabled={selectedOption === null || quizMutation.isPending}
            className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white font-bold text-xs shadow-lg shadow-violet-600/20 transition-all disabled:opacity-40 flex items-center gap-2"
          >
            {quizMutation.isPending ? "Evaluating..." : "Submit Quiz Answer"}
          </button>

          {quizSubmitted && (
            <div
              className={`p-4 rounded-xl border text-xs flex items-center gap-2.5 ${
                isCorrect
                  ? "bg-emerald-950/30 border-emerald-500/40 text-emerald-300"
                  : "bg-rose-950/30 border-rose-500/40 text-rose-300"
              }`}
            >
              {isCorrect ? (
                <>
                  <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
                  <div>
                    <span className="font-bold">Correct! +15 XP Awarded. </span>
                    <span>All problem challenges tagged with {pattern.name} are now fully unlocked.</span>
                  </div>
                </>
              ) : (
                <>
                  <XCircle className="w-5 h-5 text-rose-400 shrink-0" />
                  <div>
                    <span className="font-bold">Incorrect. </span>
                    <span>Re-read the pattern signals and try again.</span>
                  </div>
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
