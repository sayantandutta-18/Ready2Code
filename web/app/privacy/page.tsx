import React from "react";
import Link from "next/link";
import { LEGAL_CONFIG } from "@/lib/legalConfig";
import { ShieldCheck, Lock, Database, UserCheck, Trash2, Mail, FileText, CheckCircle2 } from "lucide-react";

export const metadata = {
  title: "Privacy Policy | Ready2Code",
  description: "How Ready2Code collects, uses, processes, and protects your personal and operational data.",
};

export default function PrivacyPage() {
  return (
    <div className="min-h-screen bg-[#070D18] text-slate-200 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-8">
        {/* Header */}
        <div className="border-b border-slate-800 pb-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono mb-4">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Policy Version {LEGAL_CONFIG.privacyVersion}</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Privacy Policy
          </h1>
          <p className="text-sm text-slate-400 mt-2">
            Effective Date: <span className="text-slate-300">{LEGAL_CONFIG.effectiveDate}</span> | Last Updated: <span className="text-slate-300">{LEGAL_CONFIG.lastUpdated}</span>
          </p>
        </div>

        {/* Intro */}
        <div className="p-4 rounded-xl bg-[#0F172A] border border-slate-800 text-slate-300 text-sm leading-relaxed">
          <p>
            This Privacy Policy explains how <strong className="text-white">{LEGAL_CONFIG.platformName}</strong> (&ldquo;we&rdquo;, &ldquo;us&rdquo;, or &ldquo;our&rdquo;) collects, uses, stores, and protects personal data when you use our website, APIs, and services. We are committed to processing data transparently in accordance with the <strong className="text-white">Digital Personal Data Protection Act, 2023 (DPDP Act)</strong> and the <strong className="text-white">Information Technology Act, 2000</strong>.
          </p>
        </div>

        {/* Sections */}
        <div className="space-y-8 text-sm leading-relaxed text-slate-300">
          {/* Section 1: Data We Collect */}
          <section className="space-y-3">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <span className="text-emerald-400 font-mono text-base">1.</span>
              <span>Data Categories We Collect and Process</span>
            </h2>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border border-slate-800 rounded-lg overflow-hidden">
                <thead className="bg-[#121C2F] text-slate-200 uppercase font-semibold">
                  <tr>
                    <th className="p-3 border-b border-slate-800">Category</th>
                    <th className="p-3 border-b border-slate-800">Specific Fields</th>
                    <th className="p-3 border-b border-slate-800">Mandatory / Optional</th>
                    <th className="p-3 border-b border-slate-800">Purpose</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  <tr className="hover:bg-slate-900/50">
                    <td className="p-3 font-medium text-white">Account Credentials</td>
                    <td className="p-3 font-mono text-slate-400">username, password_hash, display_name</td>
                    <td className="p-3 text-cyan-400">Username mandatory, Display name optional</td>
                    <td className="p-3">User authentication, session maintenance, and public coder identity.</td>
                  </tr>
                  <tr className="hover:bg-slate-900/50">
                    <td className="p-3 font-medium text-white">Code & Submissions</td>
                    <td className="p-3 font-mono text-slate-400">source_code, language, runtime, memory, verdict</td>
                    <td className="p-3 text-cyan-400">Mandatory to evaluate code</td>
                    <td className="p-3">Sandboxed execution, automated testing, runtime benchmarking, and leaderboard scoring.</td>
                  </tr>
                  <tr className="hover:bg-slate-900/50">
                    <td className="p-3 font-medium text-white">Learning Activity</td>
                    <td className="p-3 font-mono text-slate-400">streaks, XP ledger, problem bookmarks, personal notes</td>
                    <td className="p-3 text-slate-400">Generated on usage</td>
                    <td className="p-3">Track learning progress, spaced-repetition review queues, and streak consistency.</td>
                  </tr>
                  <tr className="hover:bg-slate-900/50">
                    <td className="p-3 font-medium text-white">User-Generated Content</td>
                    <td className="p-3 font-mono text-slate-400">discussion posts, solution write-ups, comments</td>
                    <td className="p-3 text-slate-400">Optional</td>
                    <td className="p-3">Community collaboration, peer explanations, and knowledge sharing.</td>
                  </tr>
                  <tr className="hover:bg-slate-900/50">
                    <td className="p-3 font-medium text-white">Technical & Security Logs</td>
                    <td className="p-3 font-mono text-slate-400">IP address, user agent, request timestamp, rate-limit state</td>
                    <td className="p-3 text-slate-400">Automatic / Mandatory</td>
                    <td className="p-3">DDoS defense, abuse prevention, sandbox security, and rate-limiting.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          {/* Section 2: Lawful Basis and Purpose */}
          <section className="space-y-3">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <span className="text-emerald-400 font-mono text-base">2.</span>
              <span>Lawful Grounds for Processing</span>
            </h2>
            <p>We process your personal data under the following legal bases:</p>
            <ul className="list-disc pl-5 space-y-2">
              <li>
                <strong className="text-white">Consent:</strong> Provided affirmatively when registering an account, accepting these Terms, or saving optional preferences. You may withdraw consent at any time by deleting your account.
              </li>
              <li>
                <strong className="text-white">Contractual Performance:</strong> Processing required to deliver the core service, compile and evaluate your code submissions, and maintain your learning progress.
              </li>
              <li>
                <strong className="text-white">Legal and Security Compliance:</strong> Preventing abuse, defending against cyber threats, adhering to lawful requests, and enforcing sandbox execution boundaries.
              </li>
            </ul>
          </section>

          {/* Section 3: Third-Party Service Processors */}
          <section className="space-y-3">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <span className="text-emerald-400 font-mono text-base">3.</span>
              <span>Infrastructure and Data Processors</span>
            </h2>
            <p>
              We do not sell, rent, or trade your personal data. We engage verified cloud service infrastructure strictly to operate the platform:
            </p>
            <ul className="list-disc pl-5 space-y-2">
              <li>
                <strong className="text-white">Vercel Inc.:</strong> Hosting for the frontend Next.js application, serverless rendering, and edge routing.
              </li>
              <li>
                <strong className="text-white">Railway / Cloud Hosting:</strong> Hosting and worker processes for the backend FastAPI and judge services.
              </li>
              <li>
                <strong className="text-white">Neon Inc. / PostgreSQL:</strong> Managed cloud database for user accounts, problem metadata, and submissions.
              </li>
              <li>
                <strong className="text-white">Upstash / Redis:</strong> Temporary caching for streak calculations, rate-limiting counters, and battle matchmaking.
              </li>
            </ul>
          </section>

          {/* Section 4: Data Retention and Deletion */}
          <section className="space-y-3">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <span className="text-emerald-400 font-mono text-base">4.</span>
              <span>Data Retention and Account Deletion</span>
            </h2>
            <p>
              We retain personal data only for as long as necessary to fulfill the purposes outlined in this policy:
            </p>
            <ul className="list-disc pl-5 space-y-2">
              <li>
                <strong className="text-white">Active Accounts:</strong> User profile, bookmarks, notes, and solved status are retained as long as your account remains active.
              </li>
              <li>
                <strong className="text-white">Account Deletion Process:</strong> You can initiate account deletion directly from <Link href="/settings" className="text-cyan-400 underline hover:text-cyan-300">Settings &rarr; Account</Link>. Upon confirmed deletion, your profile record, personal bookmarks, private notes, and authentication sessions are permanently deleted. Public discussions or submissions are either deleted or anonymized to prevent broken threads while scrubbing personally identifying handles.
              </li>
              <li>
                <strong className="text-white">Security & Audit Logs:</strong> Access logs, IP security records, and rate-limiting metrics are purged on a rolling cycle within 90 days, unless a security incident requires extended retention.
              </li>
            </ul>
          </section>

          {/* Section 5: Security Measures */}
          <section className="space-y-3">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <span className="text-emerald-400 font-mono text-base">5.</span>
              <span>Security Safeguards Implemented</span>
            </h2>
            <p>We implement technical and organizational controls to safeguard your data:</p>
            <ul className="list-disc pl-5 space-y-2">
              <li>
                <strong className="text-white">Cryptographic Hashing:</strong> User passwords are encrypted using one-way <code>bcrypt</code> hashing with salted rounds. Plaintext passwords are never stored or logged.
              </li>
              <li>
                <strong className="text-white">Tokenized Authentication:</strong> Sessions utilize industry-standard JSON Web Tokens (JWT) signed server-side with strict expiration and verification.
              </li>
              <li>
                <strong className="text-white">Encrypted Transport:</strong> All data in transit is encrypted using HTTPS/TLS 1.3 across web, API, and database endpoints.
              </li>
              <li>
                <strong className="text-white">Isolated Sandbox:</strong> Untrusted user code is executed in constrained sandbox runners with isolated processes, no host filesystem access, and strict memory/timeout barriers.
              </li>
            </ul>
          </section>

          {/* Section 6: User Rights */}
          <section className="space-y-3">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <span className="text-emerald-400 font-mono text-base">6.</span>
              <span>Your Rights Under DPDP Act, 2023</span>
            </h2>
            <p>As a data principal, you hold the following statutory rights:</p>
            <ul className="list-disc pl-5 space-y-2">
              <li><strong className="text-white">Right to Access:</strong> The right to view information about your personal data processed by us.</li>
              <li><strong className="text-white">Right to Correction and Erasure:</strong> The right to update inaccurate details or request deletion of personal data.</li>
              <li><strong className="text-white">Right to Grievance Redressal:</strong> The right to lodge complaints with our designated Grievance Officer and subsequently the Data Protection Board of India.</li>
              <li><strong className="text-white">Right to Nominate:</strong> The right to nominate an individual to exercise rights on your behalf in the event of death or incapacity.</li>
            </ul>
          </section>

          {/* Section 7: Grievance Officer */}
          <section className="space-y-3">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <span className="text-emerald-400 font-mono text-base">7.</span>
              <span>Grievance Redressal Officer Contact</span>
            </h2>
            <p>
              In accordance with the DPDP Act, 2023 and the Information Technology (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021, our Grievance Redressal Officer details are:
            </p>
            <div className="p-4 rounded-xl bg-[#121C2F] border border-slate-800 text-xs space-y-1.5 font-mono">
              <div className="text-white font-bold">{LEGAL_CONFIG.grievanceOfficer.name}</div>
              <div className="text-slate-400">{LEGAL_CONFIG.grievanceOfficer.designation}</div>
              <div className="text-emerald-400">Email: {LEGAL_CONFIG.grievanceOfficer.email}</div>
              <div className="text-slate-400">Postal Address: {LEGAL_CONFIG.grievanceOfficer.address}</div>
              <div className="text-slate-500 pt-1">
                Acknowledgement: within {LEGAL_CONFIG.grievanceOfficer.acknowledgementWindow} | Resolution: within {LEGAL_CONFIG.grievanceOfficer.redressalWindow}
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}
