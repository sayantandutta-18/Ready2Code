"use client";

import React, { useState, useMemo } from "react";
import dynamic from "next/dynamic";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import DifficultyChip from "../../components/ui/DifficultyChip";
import LoadingSkeleton from "../../components/ui/LoadingSkeleton";
import QueryErrorState from "../../components/ui/QueryErrorState";
import { fetchApi } from "../../lib/api";
import { Compass, BookOpen, ChevronRight, CheckCircle2 } from "lucide-react";
import { RoadmapTopic } from "../../components/3d/Roadmap3D";

// Lazy-load Roadmap3D with ssr: false (Section 4.6 requirement)
const Roadmap3D = dynamic(() => import("../../components/3d/Roadmap3D"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-[460px] flex items-center justify-center text-slate-500 font-mono text-sm bg-[#0B1220] rounded-2xl border border-slate-800">
      Rendering 3D topic spatial universe...
    </div>
  ),
});

interface ProblemItem {
  id: string;
  slug: string;
  title: string;
  difficulty: "easy" | "medium" | "hard";
  topic: string;
  status: "todo" | "attempted" | "solved";
}

const TOPIC_CONFIG = [
  { slug: "arrays", name: "Arrays", order: 1 },
  { slug: "strings", name: "Strings", order: 2 },
  { slug: "linked-list", name: "Linked List", order: 3 },
  { slug: "stack-and-queue", name: "Stack and Queue", order: 4 },
  { slug: "trees", name: "Trees", order: 5 },
  { slug: "graphs", name: "Graphs", order: 6 },
  { slug: "dp", name: "Dynamic Programming", order: 7 },
  { slug: "binary-search", name: "Binary Search", order: 8 },
];

export default function RoadmapPage() {
  const {
    data: allProblems = [],
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<ProblemItem[]>({
    queryKey: ["roadmap-problems"],
    queryFn: () => fetchApi<ProblemItem[]>("/problems"),
  });

  const { topics, topicProblems } = useMemo(() => {
    const problemsByTopic: Record<string, ProblemItem[]> = {};
    for (const t of TOPIC_CONFIG) {
      problemsByTopic[t.slug] = [];
    }

    for (const p of allProblems) {
      const topicLower = (p.topic || "arrays").toLowerCase().replace(/ /g, "-");
      const matched = TOPIC_CONFIG.find(
        (t) =>
          t.slug === topicLower ||
          t.name.toLowerCase() === (p.topic || "").toLowerCase()
      );
      const targetSlug = matched ? matched.slug : "arrays";
      if (!problemsByTopic[targetSlug]) problemsByTopic[targetSlug] = [];
      problemsByTopic[targetSlug].push(p);
    }

    const calculatedTopics: RoadmapTopic[] = TOPIC_CONFIG.map((t, idx) => {
      const list = problemsByTopic[t.slug] || [];
      const solved = list.filter((p) => p.status === "solved").length;
      return {
        id: String(idx + 1),
        slug: t.slug,
        name: t.name,
        totalProblems: Math.max(1, list.length),
        solvedCount: solved,
        order: t.order,
      };
    });

    return { topics: calculatedTopics, topicProblems: problemsByTopic };
  }, [allProblems]);

  const [selectedTopicSlug, setSelectedTopicSlug] = useState<string>("arrays");

  const currentTopic =
    topics.find((t) => t.slug === selectedTopicSlug) ||
    topics[0] || {
      id: "1",
      slug: "arrays",
      name: "Arrays",
      totalProblems: 1,
      solvedCount: 0,
      order: 1,
    };

  const activeProblems = topicProblems[currentTopic.slug] || [];

  return (
    <div className="max-w-7xl mx-auto px-4 lg:px-8 py-8 space-y-8">
      {/* Title */}
      <div>
        <h1 className="text-3xl font-black text-white tracking-tight flex items-center gap-3">
          <Compass className="w-8 h-8 text-cyan-400" />
          <span>3D Topic Island Roadmap</span>
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Progress from foundational arrays through advanced graph theory and dynamic programming.
          Master 80% to unlock subsequent islands.
        </p>
      </div>

      {isError && (
        <QueryErrorState
          title="Could not load roadmap"
          message={error instanceof Error ? error.message : "Error contacting problem server"}
          onRetry={() => refetch()}
        />
      )}

      {/* 3D Scene Platform */}
      {isLoading ? (
        <LoadingSkeleton rows={4} className="h-[460px]" />
      ) : (
        <Roadmap3D
          topics={topics}
          onSelectTopic={(t) => setSelectedTopicSlug(t.slug)}
          selectedTopicSlug={currentTopic.slug}
        />
      )}

      {/* Drawer showing problems for selected topic */}
      <div className="bg-[#121C2F] rounded-2xl border border-slate-800 p-6 shadow-2xl">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-4">
          <div className="flex items-center gap-3">
            <BookOpen className="w-5 h-5 text-cyan-400" />
            <h2 className="text-lg font-bold text-white">
              {currentTopic.name} &bull; Practice Curriculum
            </h2>
          </div>
          <span className="text-xs text-slate-400 font-mono">
            {currentTopic.solvedCount} of {currentTopic.totalProblems} Solved
          </span>
        </div>

        {activeProblems.length === 0 ? (
          <div className="text-center py-8 text-slate-500 text-xs">
            No problems currently tagged under this topic.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {activeProblems.map((prob) => (
              <Link
                key={prob.slug}
                href={`/problems/${prob.slug}`}
                className="p-3.5 rounded-xl bg-[#0B1220] border border-slate-800/80 hover:border-cyan-500/40 flex items-center justify-between group transition-all"
              >
                <div className="flex items-center gap-3">
                  {prob.status === "solved" ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  ) : (
                    <span className="w-3.5 h-3.5 rounded-full border border-slate-600 block" />
                  )}
                  <div>
                    <div className="text-sm font-semibold text-slate-200 group-hover:text-cyan-300 transition-colors">
                      {prob.title}
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <DifficultyChip difficulty={prob.difficulty} />
                  <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-cyan-400 transition-colors" />
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
