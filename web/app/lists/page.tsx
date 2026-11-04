"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import TiltCard from "../../components/ui/TiltCard";
import LoadingSkeleton from "../../components/ui/LoadingSkeleton";
import EmptyState from "../../components/ui/EmptyState";
import QueryErrorState from "../../components/ui/QueryErrorState";
import { fetchApi } from "../../lib/api";
import { ListTodo, Calendar, Plus, CheckCircle2, ChevronRight, Layers, Sparkles } from "lucide-react";

interface ProblemListItem {
  id: string;
  name: string;
  description: string;
  total_problems: number;
  solved_count?: number;
  is_system: boolean;
}

interface StudyPlanItem {
  id: string;
  name: string;
  description: string;
  duration_days: number;
  total_problems: number;
}

export default function ListsPage() {
  const queryClient = useQueryClient();
  const [newListName, setNewListName] = useState("");
  const [showCreateModal, setShowCreateModal] = useState(false);

  // Fetch Lists
  const {
    data: lists = [],
    isLoading: isListsLoading,
    isError: isListsError,
    error: listsError,
    refetch: refetchLists,
  } = useQuery<ProblemListItem[]>({
    queryKey: ["lists"],
    queryFn: () => fetchApi<ProblemListItem[]>("/lists"),
  });

  // Fetch Study Plans
  const {
    data: plans = [],
    isLoading: isPlansLoading,
    isError: isPlansError,
    error: plansError,
    refetch: refetchPlans,
  } = useQuery<StudyPlanItem[]>({
    queryKey: ["plans"],
    queryFn: () => fetchApi<StudyPlanItem[]>("/plans"),
  });

  // Create Custom List Mutation
  const createListMutation = useMutation({
    mutationFn: (name: string) =>
      fetchApi("/lists", {
        method: "POST",
        body: JSON.stringify({ name, problem_slugs: ["two-sum"] }),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["lists"] });
      setNewListName("");
      setShowCreateModal(false);
    },
  });

  const handleCreateCustomList = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newListName.trim()) return;
    createListMutation.mutate(newListName.trim());
  };

  return (
    <div className="max-w-7xl mx-auto px-4 lg:px-8 py-10 space-y-12">
      {/* Section 1: Curated & Custom Problem Lists */}
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-black text-white tracking-tight flex items-center gap-3">
              <ListTodo className="w-8 h-8 text-cyan-400" />
              <span>Curated Problem Collections</span>
            </h1>
            <p className="text-sm text-slate-400 mt-1">
              Authoritative syllabi including Blind 75, NeetCode 150, and community sets.
            </p>
          </div>

          <button
            onClick={() => setShowCreateModal(true)}
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 text-xs font-semibold transition-all self-start sm:self-auto active:scale-95"
          >
            <Plus className="w-4 h-4" />
            <span>Create Custom List</span>
          </button>
        </div>

        {isListsError && (
          <QueryErrorState
            title="Could not load problem lists"
            message={listsError instanceof Error ? listsError.message : "Error contacting lists API"}
            onRetry={() => refetchLists()}
          />
        )}

        {isListsLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <LoadingSkeleton rows={3} className="h-44" />
            <LoadingSkeleton rows={3} className="h-44" />
          </div>
        ) : lists.length === 0 ? (
          <EmptyState
            title="No problem collections"
            description="Create your first practice collection using the button above."
          />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {lists.map((l) => (
              <Link key={l.id} href={`/lists/${l.id}`} className="block">
                <TiltCard className="h-full flex flex-col justify-between space-y-4 hover:border-cyan-500/50">
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400">
                        {l.is_system ? "Verified Curriculum" : "Personal Collection"}
                      </span>
                      {l.is_system && (
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                          SYSTEM
                        </span>
                      )}
                    </div>

                    <h3 className="text-xl font-bold text-white group-hover:text-cyan-300">
                      {l.name}
                    </h3>
                    <p className="text-xs text-slate-400 leading-relaxed">{l.description}</p>
                  </div>

                  <div className="pt-3 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400 font-mono">
                    <div className="flex items-center gap-1.5">
                      <Layers className="w-3.5 h-3.5 text-cyan-400" />
                      <span>{l.total_problems} Problems</span>
                    </div>
                    <div className="text-cyan-400 font-semibold flex items-center gap-1">
                      <span>Explore</span>
                      <ChevronRight className="w-4 h-4" />
                    </div>
                  </div>
                </TiltCard>
              </Link>
            ))}
          </div>
        )}
      </div>

      {/* Section 2: Guided Study Plans */}
      <div className="space-y-6 pt-6 border-t border-slate-800/80">
        <div>
          <h2 className="text-2xl font-black text-white tracking-tight flex items-center gap-3">
            <Calendar className="w-7 h-7 text-violet-400" />
            <span>Structured 30/60/90-Day Plans</span>
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Day-by-day assigned algorithmic milestones to build deep muscle memory.
          </p>
        </div>

        {isPlansError && (
          <QueryErrorState
            title="Could not load study plans"
            message={plansError instanceof Error ? plansError.message : "Error contacting plans API"}
            onRetry={() => refetchPlans()}
          />
        )}

        {isPlansLoading ? (
          <LoadingSkeleton rows={4} className="h-36" />
        ) : plans.length === 0 ? (
          <EmptyState
            title="No active study plans"
            description="Check back soon for new guided study bootcamps."
          />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {plans.map((p) => (
              <Link key={p.id} href={`/plans/${p.id}`} className="block">
                <TiltCard className="h-full flex flex-col justify-between space-y-4 hover:border-violet-500/50">
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400">
                        {p.duration_days}-Day Intensive
                      </span>
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-violet-500/10 text-violet-300 border border-violet-500/20">
                        BOOTCAMP
                      </span>
                    </div>

                    <h3 className="text-xl font-bold text-white group-hover:text-violet-300">
                      {p.name}
                    </h3>
                    <p className="text-xs text-slate-400 leading-relaxed">{p.description}</p>
                  </div>

                  <div className="pt-3 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400 font-mono">
                    <span>{p.total_problems} Assigned Solves</span>
                    <div className="text-violet-400 font-semibold flex items-center gap-1">
                      <span>Start Plan</span>
                      <ChevronRight className="w-4 h-4" />
                    </div>
                  </div>
                </TiltCard>
              </Link>
            ))}
          </div>
        )}
      </div>

      {/* Modal for creating custom list */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="max-w-md w-full bg-[#121C2F] border border-slate-800 rounded-2xl p-6 space-y-4 shadow-2xl">
            <h3 className="text-lg font-bold text-white">Create Practice Collection</h3>
            <p className="text-xs text-slate-400">
              Curate and order your personal set of problems for interview focus.
            </p>
            <form onSubmit={handleCreateCustomList} className="space-y-4">
              <input
                type="text"
                placeholder="Collection name (e.g. 'Amazon High Frequency')"
                value={newListName}
                onChange={(e) => setNewListName(e.target.value)}
                autoFocus
                className="w-full bg-[#0B1220] border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-400"
              />
              <div className="flex items-center justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={!newListName.trim() || createListMutation.isPending}
                  className="px-4 py-2 rounded-xl bg-cyan-500 hover:bg-cyan-600 text-slate-950 text-xs font-bold transition-all disabled:opacity-50"
                >
                  {createListMutation.isPending ? "Creating..." : "Create Collection"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
