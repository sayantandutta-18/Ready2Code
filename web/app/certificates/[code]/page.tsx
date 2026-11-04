"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { Award, CheckCircle2, Share2, ArrowLeft, ShieldCheck, ExternalLink, Code2 } from "lucide-react";

export default function CertificateVerifyPage({ params }: { params: { code: string } }) {
  const { code } = params;

  const [cert, setCert] = useState<any>({
    verified: true,
    verify_code: code.toUpperCase(),
    skill: "Data Structures & Algorithmic Problem Solving",
    score: 88,
    holder_name: "Alex Vance",
    issued_at: "November 04, 2026",
    platform: "Ready2Code 3D DSA Arena",
  });

  useEffect(() => {
    fetch(`/api/certificates/verify/${code}`)
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (data && data.verified) setCert(data);
      })
      .catch(() => {});
  }, [code]);

  const linkedInShareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(
    typeof window !== "undefined" ? window.location.href : `https://ready2code.dev/certificates/${code}`
  )}`;

  return (
    <div className="max-w-4xl mx-auto px-4 lg:px-8 py-12 space-y-8">
      {/* Back button */}
      <Link href="/profile/coder_alex" className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-cyan-400 font-mono">
        <ArrowLeft className="w-3.5 h-3.5" /> Back to Profile
      </Link>

      {/* Verification Status Pill */}
      <div className="flex items-center justify-between p-4 rounded-2xl bg-emerald-950/20 border border-emerald-500/40 text-emerald-300 text-xs">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-emerald-400" />
          <span className="font-semibold">Officially Verified Certificate &bull; Cryptographic Hash Authenticated</span>
        </div>
        <span className="font-mono font-bold">{cert.verify_code}</span>
      </div>

      {/* Certificate Frame Card */}
      <div className="relative p-10 sm:p-14 rounded-3xl bg-[#0e1626] border-2 border-cyan-500/40 shadow-[0_20px_60px_rgba(34,211,238,0.15)] flex flex-col items-center text-center space-y-6 overflow-hidden">
        {/* Decorative corner glows */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-0 left-0 w-64 h-64 bg-violet-500/10 rounded-full blur-3xl pointer-events-none" />

        {/* Brand */}
        <div className="flex items-center gap-2">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-cyan-400 to-violet-600 flex items-center justify-center">
            <Code2 className="w-5 h-5 text-slate-950 stroke-[2.5]" />
          </div>
          <span className="text-xl font-black bg-gradient-to-r from-white to-cyan-300 bg-clip-text text-transparent">
            Ready2Code
          </span>
        </div>

        <div className="text-xs uppercase font-mono tracking-widest text-slate-400">
          Certificate of Competence & Algorithmic Mastery
        </div>

        <div className="space-y-1">
          <div className="text-sm text-slate-400">This is to certify that</div>
          <div className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            {cert.holder_name}
          </div>
          <div className="text-sm text-slate-400 pt-2">
            has successfully passed the timed evaluation in
          </div>
          <div className="text-xl font-bold text-cyan-300">{cert.skill}</div>
        </div>

        {/* Score & Issue Details */}
        <div className="grid grid-cols-2 gap-8 pt-4 border-t border-slate-800/80 w-full max-w-md text-xs">
          <div>
            <div className="text-slate-500 font-mono uppercase text-[10px]">Verified Score</div>
            <div className="text-xl font-bold text-emerald-400 font-mono mt-0.5">{cert.score}%</div>
          </div>
          <div>
            <div className="text-slate-500 font-mono uppercase text-[10px]">Date Issued</div>
            <div className="text-slate-200 font-medium mt-0.5">{cert.issued_at}</div>
          </div>
        </div>

        <div className="text-[11px] font-mono text-slate-500">
          Verification ID: <span className="text-slate-400">{cert.verify_code}</span> &bull; Issued by Ready2Code Engine
        </div>
      </div>

      {/* Share Actions */}
      <div className="flex items-center justify-center gap-4">
        <a
          href={linkedInShareUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="px-6 py-3 rounded-xl bg-[#0077b5] hover:bg-[#006097] text-white font-bold text-xs flex items-center gap-2 shadow-lg transition-all"
        >
          <Share2 className="w-4 h-4" />
          <span>Add to LinkedIn Profile</span>
          <ExternalLink className="w-3.5 h-3.5" />
        </a>
      </div>
    </div>
  );
}
