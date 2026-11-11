import React from "react";
import Link from "next/link";
import { LEGAL_CONFIG } from "@/lib/legalConfig";
import { Cookie, ShieldCheck, Database, CheckCircle2, Lock } from "lucide-react";

export const metadata = {
  title: "Cookies & Local Storage Policy | Ready2Code",
  description: "Information regarding the use of cookies and browser local storage on Ready2Code.",
};

export default function CookiesPage() {
  return (
    <div className="min-h-screen bg-[#070D18] text-slate-200 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-8">
        {/* Header */}
        <div className="border-b border-slate-800 pb-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-mono mb-4">
            <Cookie className="w-3.5 h-3.5" />
            <span>Storage &amp; Cookie Disclosure</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Cookies &amp; Local Storage Policy
          </h1>
          <p className="text-sm text-slate-400 mt-2">
            Effective Date: <span className="text-slate-300">{LEGAL_CONFIG.effectiveDate}</span> | Last Updated: <span className="text-slate-300">{LEGAL_CONFIG.lastUpdated}</span>
          </p>
        </div>

        {/* Intro */}
        <div className="p-4 rounded-xl bg-[#0F172A] border border-slate-800 text-slate-300 text-sm leading-relaxed">
          <p>
            <strong className="text-white">{LEGAL_CONFIG.platformName}</strong> respects your digital privacy. We do not use third-party advertising cookies, cross-site tracking pixels, or commercial tracking networks. We utilize only strictly necessary browser storage essential to maintain your logged-in session and platform preferences.
          </p>
        </div>

        {/* Inventory of Storage Items */}
        <div className="space-y-4">
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Database className="w-5 h-5 text-cyan-400" />
            <span>Complete Inventory of Browser Storage Used</span>
          </h2>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border border-slate-800 rounded-lg overflow-hidden">
              <thead className="bg-[#121C2F] text-slate-200 uppercase font-semibold">
                <tr>
                  <th className="p-3 border-b border-slate-800">Storage Key</th>
                  <th className="p-3 border-b border-slate-800">Storage Type</th>
                  <th className="p-3 border-b border-slate-800">Classification</th>
                  <th className="p-3 border-b border-slate-800">Purpose &amp; Lifecycle</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                <tr className="hover:bg-slate-900/50">
                  <td className="p-3 font-mono text-cyan-300">ready2code_auth_token</td>
                  <td className="p-3">localStorage</td>
                  <td className="p-3 font-semibold text-emerald-400">Strictly Necessary</td>
                  <td className="p-3">
                    Stores the user&apos;s signed JSON Web Token (JWT) to maintain authenticated session across page navigation and reloads. Cleared automatically upon clicking &ldquo;Sign Out&rdquo;.
                  </td>
                </tr>
                <tr className="hover:bg-slate-900/50">
                  <td className="p-3 font-mono text-cyan-300">ready2code_user</td>
                  <td className="p-3">localStorage</td>
                  <td className="p-3 font-semibold text-emerald-400">Strictly Necessary</td>
                  <td className="p-3">
                    Caches user profile summary (username, display name, avatar) for immediate header rendering without blocking network waterfalls. Cleared upon logout.
                  </td>
                </tr>
                <tr className="hover:bg-slate-900/50">
                  <td className="p-3 font-mono text-cyan-300">ready2code_onboarding_dismissed</td>
                  <td className="p-3">localStorage</td>
                  <td className="p-3 text-slate-300">Functional / UX Preference</td>
                  <td className="p-3">
                    Remembers whether the new-coder welcome modal has been dismissed so it is not repeatedly displayed.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* User Controls */}
        <div className="space-y-4 text-sm text-slate-300">
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Lock className="w-5 h-5 text-emerald-400" />
            <span>How to Manage or Clear Browser Storage</span>
          </h2>
          <p>
            Because our storage is strictly functional and essential for session integrity, blocking local storage will prevent sign-in from functioning properly. However, you retain full control over your browser data:
          </p>
          <ul className="list-disc pl-5 space-y-2">
            <li>
              <strong className="text-white">Signing Out:</strong> Clicking &ldquo;Sign Out&rdquo; in the header immediately purges your authentication tokens and user profile from <code>localStorage</code>.
            </li>
            <li>
              <strong className="text-white">Browser Developer Tools / Settings:</strong> You can clear cookies and site data at any time via your browser settings (under Privacy &amp; Security &rarr; Clear Browsing Data) or via Developer Tools (Application &rarr; Storage &rarr; Clear site data).
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
