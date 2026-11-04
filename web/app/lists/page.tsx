"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import TiltCard from "../../components/ui/TiltCard";
import { ListTodo, Calendar, Plus, CheckCircle2, ChevronRight, Layers, Sparkles } from "lucide-react";

export default function ListsPage() {
  const [lists, setLists] = useState<any[]>([
    {
      id: "blind-75",
      name: "Blind 75 High-Frequency Core",
      description: "Essential foundational algorithmic patterns curated for top tech interviews.",
      total_problems: 8,
      solved_count: 5,
      is_system: true,
    },
    {
      id: "neetcode-150",
      name: "NeetCode 150 Essentials",
      description: "Structured curriculum spanning arrays, linked lists, trees, graphs, and dynamic programming.",
      total_problems: 6,
      solved_count: 3,
      is_system: true,
    },
  ]);

  const [plans, setPlans] = useState<any[]>([
    {
      id: "30-day-bootcamp",
      name: "30-Day Interview Readiness Bootcamp",
      description: "Daily assigned algorithmic challenges progressing from arrays to dynamic programming.",
      duration_days: 30,
      total_problems: 12,
    },
  ]);

  const [newListName, setNewListName] = useState("");
  const [showCreateModal, setShowCreateModal] = useState(false);

  useEffect(() => {
    fetch("/api/lists")
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) setLists(data);
      })
      .catch(() => {});

    fetch("/api/plans")
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) setPlans(data);
      })
      .catch(() => {});
  }, []);

  const handleCreateCustomList = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newListName.trim()) return;
    try {
      const res = await fetch("/api/lists", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: newListName.trim(), problem_slugs: ["two-sum"] }),
      });
      if (res.ok) {
        const created = await res.json();
        setLists((prev) => [
          ...prev,
          { id: created.id, name: created.name, description: "Custom practice collection", total_problems: 1, is_system: false },
        ]);
        setNewListName("");
        setShowCreateModal(false);
      }
    } catch {
      setShowCreateModal(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 lg:px-8 py-10 space-y-10">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-black text-white tracking-tight flex items-center gap-3">
            <ListTodo className="w-8 h-8 text-cyan-400" />
            <span>Curated Lists & Study Plans</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Industry-standard problem sets and calendar-based study plans to structure your prep.
          </p>
        </div>

        <button
          onClick={() => setShowCreateModal(true)}
          className="px-4 py-2.5 rounded-xl bg-cyan-400 hover:bg-cyan-300 text-slate-950 font-bold text-xs shadow-lg shadow-cyan-500/20 flex items-center gap-2 self-start sm:self-auto transition-all"
        >
          <Plus className="w-4 h-4" />
          <span>Create Custom List</span>
        </button>
      </div>

      {/* Curated Lists Section */}
      <div className="space-y-4">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <Layers className="w-5 h-5 text-violet-400" />
          <span>Curated Problem Collections</span>
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {lists.map((l) => (
            <Link key={l.id} href={`/lists/${l.id}`} className="block">
              <TiltCard className="h-full flex flex-col justify-between hover:border-cyan-500/50">
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-cyan-400 px-2 py-0.5 rounded bg-cyan-950/60 border border-cyan-500/30">
                      {l.is_system ? "System Curated" : "Custom List"}
                    </span>
                    <span className="text-xs text-slate-400 font-mono">
                      {l.total_problems} Problems
                    </span>
                  </div>
                  <h3 className="text-lg font-bold text-white group-hover:text-cyan-300">
                    {l.name}
                  </h3>
                  <p className="text-xs text-slate-400 leading-relaxed">{l.description}</p>
                </div>

                <div className="pt-4 mt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
                  <span className="text-cyan-400 font-semibold flex items-center gap-1">
                    Open Collection <ChevronRight className="w-3.5 h-3.5" />
                  </span>
                </div>
              </TiltCard>
            </Link>
          ))}
        </div>
      </div>

      {/* 30/60/90-Day Study Plans Section (C2.1) */}
      <div className="space-y-4">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <Calendar className="w-5 h-5 text-amber-400" />
          <span>Day-by-Day Study Plans (30 / 60 / 90 Days)</span>
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {plans.map((p) => (
            <Link key={p.id} href={`/plans/${p.id}`} className="block">
              <TiltCard className="h-full flex flex-col justify-between hover:border-amber-500/50">
                <div className="space-y-2">
                  <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-amber-400 px-2 py-0.5 rounded bg-amber-950/60 border border-amber-500/30">
                    {p.duration_days}-Day Bootcamp
                  </span>
                  <h3 className="text-base font-bold text-white">{p.name}</h3>
                  <p className="text-xs text-slate-400 leading-relaxed">{p.description}</p>
                </div>

                <div className="pt-4 mt-4 border-t border-slate-800 flex items-center justify-between text-xs text-amber-400 font-semibold">
                  <span>Start Day 1 &bull; {p.total_problems} Days Active</span>
                  <ChevronRight className="w-4 h-4" />
                </div>
              </TiltCard>
            </Link>
          ))}
        </div>
      </div>

      {/* Create Custom List Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="bg-[#121C2F] rounded-2xl border border-slate-700 p-6 max-w-md w-full space-y-4 shadow-2xl">
            <h3 className="text-lg font-bold text-white">Create New Custom List</h3>
            <p className="text-xs text-slate-400">
              Name your personal problem playlist to organize study topics and track mastery.
            </p>
            <input
              type="text"
              placeholder="e.g. Dynamic Programming Drill, Google Final Round..."
              value={newListName}
              onChange={(e) => setNewListName(e.target.value)}
              className="w-full bg-[#0B1220] border border-slate-700 rounded-xl px-4 py-2 text-sm text-slate-200 focus:outline-none focus:border-cyan-400"
            />
            <div className="flex justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setShowCreateModal(false)}
                className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 text-xs font-semibold"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleCreateCustomList}
                className="px-4 py-2 rounded-xl bg-cyan-400 text-slate-950 text-xs font-bold shadow"
              >
                Create List
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
