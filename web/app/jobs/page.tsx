"use client";

import { useState } from "react";
import Link from "next/link";
import { Briefcase, MapPin, Building2, CheckCircle2, ShieldCheck, Zap, ArrowRight, ExternalLink } from "lucide-react";
import TiltCard from "@/components/ui/TiltCard";

const JOBS_DATA = [
  {
    id: "job-1",
    company: "Razorpay",
    role: "Software Development Engineer (Backend)",
    location: "Bengaluru, India (Hybrid)",
    ctc: "₹24 - ₹32 LPA",
    minElo: 1550,
    tags: ["Go", "Distributed Systems", "DSA", "Kafka"],
    description: "Scale India's premier financial payments infrastructure handling 10,000+ transactions per second."
  },
  {
    id: "job-2",
    company: "Zepto",
    role: "SDE-1 (Supply Chain & Routing)",
    location: "Mumbai / Bengaluru",
    ctc: "₹28 - ₹36 LPA",
    minElo: 1600,
    tags: ["Python", "Algorithms", "Graph Theory", "Redis"],
    description: "Design hyper-optimized routing and dispatch algorithms for 10-minute grocery fulfillment."
  },
  {
    id: "job-3",
    company: "Cred",
    role: "Backend Engineer (Payments & Trust)",
    location: "Bengaluru, India",
    ctc: "₹30 - ₹45 LPA",
    minElo: 1650,
    tags: ["Java", "High Concurrency", "System Design"],
    description: "Architect mission-critical payment workflows with four 9s reliability and microsecond latency."
  },
  {
    id: "job-4",
    company: "Swiggy",
    role: "Software Engineer (Delivery Logistics)",
    location: "Bengaluru / Remote",
    ctc: "₹22 - ₹30 LPA",
    minElo: 1500,
    tags: ["Java", "Data Structures", "Dynamic Programming"],
    description: "Optimize real-time batching and delivery assignment algorithms across 500+ Indian cities."
  },
  {
    id: "job-5",
    company: "Meesho",
    role: "SDE-1 (Platform & Search)",
    location: "Bengaluru, India",
    ctc: "₹20 - ₹28 LPA",
    minElo: 1500,
    tags: ["Elasticsearch", "DSA", "Node.js"],
    description: "Power high-throughput search and discovery for 100M+ monthly active Indian consumers."
  }
];

export default function JobsPage() {
  const [appliedJobs, setAppliedJobs] = useState<string[]>([]);
  const userElo = 1640;

  const handleApply = (jobId: string) => {
    if (!appliedJobs.includes(jobId)) {
      setAppliedJobs([...appliedJobs, jobId]);
    }
  };

  return (
    <div className="min-h-screen bg-[#070D18] text-slate-100 py-10 px-4 md:px-8">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <div className="space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold">
            <Briefcase className="w-3.5 h-3.5" />
            Verified Skill Hiring Board
          </div>
          <h1 className="text-3xl md:text-4xl font-black tracking-tight text-white">
            Skip the Resume Black Hole
          </h1>
          <p className="text-slate-400 text-sm md:text-base max-w-2xl">
            Top tech engineering teams hire directly through Ready2Code verified skill badges and Elo ratings.
            Fast-Track applications bypass HR screeners directly to the technical hiring manager.
          </p>
        </div>

        {/* User Verified Status Bar */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-cyan-500/20 text-cyan-400 flex items-center justify-center font-bold">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <div className="text-sm font-bold text-white flex items-center gap-2">
                Your Ready2Code Verified Profile
                <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono">Qualified for 4/5 Roles</span>
              </div>
              <div className="text-xs text-slate-400">Competitive Rating: <strong className="text-amber-400 font-mono">1,640 ELO</strong> • Solved: <strong>148 Problems</strong></div>
            </div>
          </div>
          <Link
            href="/portfolio/coder_alex"
            className="text-xs text-cyan-400 hover:text-cyan-300 font-semibold flex items-center gap-1 self-start sm:self-auto"
          >
            <span>Edit Public Portfolio</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </Link>
        </div>

        {/* Job Listings Grid */}
        <div className="space-y-4">
          {JOBS_DATA.map((job) => {
            const isQualified = userElo >= job.minElo;
            const hasApplied = appliedJobs.includes(job.id);

            return (
              <div
                key={job.id}
                className="bg-slate-900/40 border border-slate-800 hover:border-slate-700 rounded-2xl p-6 transition-all shadow-md flex flex-col md:flex-row items-start md:items-center justify-between gap-6"
              >
                <div className="space-y-3 flex-1">
                  <div className="flex flex-wrap items-center gap-3">
                    <h2 className="text-lg font-bold text-white">{job.role}</h2>
                    <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                      {job.company}
                    </span>
                    <span className="text-xs font-mono font-bold text-emerald-400 bg-emerald-500/10 px-2.5 py-0.5 rounded-md border border-emerald-500/20">
                      {job.ctc}
                    </span>
                  </div>

                  <p className="text-xs text-slate-400 leading-relaxed max-w-3xl">
                    {job.description}
                  </p>

                  <div className="flex flex-wrap items-center gap-4 text-xs text-slate-400">
                    <span className="flex items-center gap-1">
                      <MapPin className="w-3.5 h-3.5 text-slate-500" />
                      {job.location}
                    </span>
                    <span className="flex items-center gap-1 font-mono">
                      <Zap className="w-3.5 h-3.5 text-amber-400" />
                      Min. Required Rating: <strong className="text-slate-200">{job.minElo} ELO</strong>
                    </span>
                  </div>

                  {/* Tags */}
                  <div className="flex flex-wrap gap-1.5 pt-1">
                    {job.tags.map((t, idx) => (
                      <span
                        key={idx}
                        className="text-[10px] px-2 py-0.5 rounded bg-slate-800/80 text-slate-300 border border-slate-700/60 font-mono"
                      >
                        {t}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Apply Button Action */}
                <div className="shrink-0 w-full md:w-auto">
                  {hasApplied ? (
                    <div className="flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold uppercase tracking-wider">
                      <CheckCircle2 className="w-4 h-4" />
                      Fast-Track Applied
                    </div>
                  ) : isQualified ? (
                    <button
                      onClick={() => handleApply(job.id)}
                      className="w-full md:w-auto px-6 py-3 rounded-xl bg-gradient-to-r from-cyan-400 to-indigo-500 hover:from-cyan-500 hover:to-indigo-600 text-slate-950 font-extrabold text-xs uppercase tracking-wider flex items-center justify-center gap-2 shadow-lg shadow-cyan-500/20 active:scale-95 transition-all"
                    >
                      <span>1-Click Fast-Track Apply</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  ) : (
                    <div className="text-center px-4 py-2 rounded-xl bg-slate-800/60 border border-slate-700/50 text-[11px] text-slate-400 font-medium">
                      Requires {job.minElo} ELO (+{job.minElo - userElo} pts needed)
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
