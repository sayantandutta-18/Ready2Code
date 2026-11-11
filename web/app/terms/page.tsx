import React from "react";
import Link from "next/link";
import { LEGAL_CONFIG } from "@/lib/legalConfig";
import { Shield, FileText, CheckCircle2, AlertTriangle, Scale, Lock, RefreshCw, Mail } from "lucide-react";

export const metadata = {
  title: "Terms of Service | Ready2Code",
  description: "Terms and conditions governing the use of the Ready2Code interactive DSA platform.",
};

export default function TermsPage() {
  return (
    <div className="min-h-screen bg-[#070D18] text-slate-200 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-8">
        {/* Header */}
        <div className="border-b border-slate-800 pb-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-mono mb-4">
            <FileText className="w-3.5 h-3.5" />
            <span>Version {LEGAL_CONFIG.termsVersion}</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Terms of Service
          </h1>
          <p className="text-sm text-slate-400 mt-2">
            Effective Date: <span className="text-slate-300">{LEGAL_CONFIG.effectiveDate}</span> | Last Updated: <span className="text-slate-300">{LEGAL_CONFIG.lastUpdated}</span>
          </p>
        </div>

        {/* Notice Banner */}
        <div className="p-4 rounded-xl bg-[#0F172A] border border-cyan-500/20 text-slate-300 text-sm leading-relaxed">
          <p>
            Please read these Terms of Service (&ldquo;Terms&rdquo;) carefully before accessing or using the{" "}
            <strong className="text-white">{LEGAL_CONFIG.platformName}</strong> platform (&ldquo;Service&rdquo;). By accessing the Service, registering an account, or submitting code, you agree to be bound by these Terms and acknowledge our{" "}
            <Link href="/privacy" className="text-cyan-400 underline hover:text-cyan-300">
              Privacy Policy
            </Link>. If you do not agree, do not access or use the Service.
          </p>
        </div>

        {/* Content Sections */}
        <div className="space-y-8 text-sm leading-relaxed text-slate-300">
          {/* Section 1 */}
          <section className="space-y-3">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <span className="text-cyan-400 font-mono text-base">1.</span>
              <span>The Platform and Services</span>
            </h2>
            <p>
              {LEGAL_CONFIG.platformName} is an educational platform providing 3D algorithm visualizers, a curated data structures and algorithms (DSA) problem catalog, automated code execution benchmarking, mock interview timers, and community discussion boards.
            </p>
            <p>
              <strong className="text-white">Free Launch Tier:</strong> The Service is presently offered as a free educational tool. No subscription, enrollment fee, or paid plan is currently mandatory to access problem catalogs, visualizers, or standard submission evaluation. Future optional commercial tiers, if introduced, will be governed by updated, explicitly communicated terms.
            </p>
          </section>

          {/* Section 2 */}
          <section className="space-y-3">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <span className="text-cyan-400 font-mono text-base">2.</span>
              <span>Eligibility and Account Registration</span>
            </h2>
            <ul className="list-disc pl-5 space-y-2">
              <li>
                <strong className="text-white">Age Requirement:</strong> You must be at least 18 years of age to independently create an account. If you are under 18 years of age, you may use the Service only with the consent, supervision, and approval of a parent or legal guardian who agrees to be bound by these Terms.
              </li>
              <li>
                <strong className="text-white">Account Security:</strong> You are responsible for maintaining the confidentiality of your account credentials and for all activities that occur under your account. You agree to notify us immediately of any unauthorized use at <span className="font-mono text-cyan-400">{LEGAL_CONFIG.supportEmail}</span>.
              </li>
              <li>
                <strong className="text-white">Account Deletion:</strong> You may request deletion of your account at any time through the Account Settings page or by contacting our team. Deletion removes or anonymizes your active profile, streaks, and bookmarks, subject to residual legal or security obligations detailed in our Privacy Policy.
              </li>
            </ul>
          </section>

          {/* Section 3 */}
          <section className="space-y-3">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <span className="text-cyan-400 font-mono text-base">3.</span>
              <span>Code Execution, Sandbox, and Judge Limitations</span>
            </h2>
            <p>
              Code submitted through the platform is executed in automated sandboxed environments:
            </p>
            <ul className="list-disc pl-5 space-y-2">
              <li>
                <strong className="text-white">Resource Limits:</strong> Each execution is subject to strict CPU time limits (standard: 1,000 milliseconds) and memory limits (standard: 128 MB). Submissions exceeding these thresholds will be terminated with Time Limit Exceeded (TLE) or Memory Limit Exceeded (MLE) verdicts.
              </li>
              <li>
                <strong className="text-white">Best-Effort Evaluation:</strong> Automated test execution is provided on a best-effort basis. Network delays, transient queueing, or sandbox restarts may occasionally cause execution delays. We do not guarantee uninterrupted evaluation availability.
              </li>
              <li>
                <strong className="text-white">Hidden Tests:</strong> To maintain academic integrity, hidden test cases used for final verdict assessment are held server-side and will not be displayed in full to users.
              </li>
            </ul>
          </section>

          {/* Section 4 */}
          <section className="space-y-3">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <span className="text-cyan-400 font-mono text-base">4.</span>
              <span>Acceptable Use and Prohibited Conduct</span>
            </h2>
            <p>You agree not to engage in any of the following prohibited activities:</p>
            <ul className="list-disc pl-5 space-y-2">
              <li>Attempting to bypass, escape, or exploit the code execution sandbox, judge containers, or host networking.</li>
              <li>Using automated bots, scrapers, or scripts to bulk-download problem statements, test cases, or visualizer assets.</li>
              <li>Submitting malicious payloads, denial-of-service attempts, fork bombs, or code designed to interfere with system operations.</li>
              <li>Cheating, automated solution generation during timed contests, or reverse-engineering hidden test suites through side-channels.</li>
              <li>Harassing, abusing, or posting unlawful, defamatory, or obscene content in discussion posts, solutions, or username fields.</li>
            </ul>
          </section>

          {/* Section 5 */}
          <section className="space-y-3">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <span className="text-cyan-400 font-mono text-base">5.</span>
              <span>Intellectual Property and User Submissions</span>
            </h2>
            <ul className="list-disc pl-5 space-y-2">
              <li>
                <strong className="text-white">Platform Ownership:</strong> The {LEGAL_CONFIG.platformName} software, 3D visualizer shaders, user interface designs, logo, problem write-ups, and documentation are proprietary assets protected by copyright and intellectual property laws.
              </li>
              <li>
                <strong className="text-white">User Code Ownership:</strong> You retain ownership of the original code solutions and explanations you write and submit. By submitting code or posts, you grant {LEGAL_CONFIG.platformName} a limited, worldwide, non-exclusive, royalty-free license to store, process, execute, display, benchmark, and moderate that content solely for operating and improving the Service.
              </li>
            </ul>
          </section>

          {/* Section 6 */}
          <section className="space-y-3">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <span className="text-cyan-400 font-mono text-base">6.</span>
              <span>AI Features and Placement Disclaimers</span>
            </h2>
            <ul className="list-disc pl-5 space-y-2">
              <li>
                <strong className="text-white">AI-Assisted Features:</strong> AI hints, code review feedback, and interview dialogue are generated using machine learning models. These outputs are automated educational aids, may occasionally contain inaccuracies or omissions, and should be verified independently.
              </li>
              <li>
                <strong className="text-white">No Guarantee of Employment:</strong> Company-specific roadmaps, placement modules, and interview preparation materials are strictly educational. {LEGAL_CONFIG.platformName} is not affiliated with, endorsed by, or sponsored by any represented technology companies. Use of the Service does not constitute an offer, interview guarantee, or employment assurance.
              </li>
            </ul>
          </section>

          {/* Section 7 */}
          <section className="space-y-3">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <span className="text-cyan-400 font-mono text-base">7.</span>
              <span>Disclaimers and Limitation of Liability</span>
            </h2>
            <p>
              THE SERVICE IS PROVIDED ON AN &ldquo;AS IS&rdquo; AND &ldquo;AS AVAILABLE&rdquo; BASIS WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED. TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, {LEGAL_CONFIG.platformName} AND ITS OPERATORS DISCLAIM ALL WARRANTIES, INCLUDING MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.
            </p>
            <p>
              IN NO EVENT SHALL {LEGAL_CONFIG.platformName} BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES ARISING OUT OF YOUR USE OR INABILITY TO USE THE SERVICE. NOTHING IN THESE TERMS EXCLUDES OR LIMITS ANY STATUTORY CONSUMER RIGHTS THAT CANNOT BE LAWFULLY EXCLUDED UNDER APPLICABLE LAW.
            </p>
          </section>

          {/* Section 8 */}
          <section className="space-y-3">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <span className="text-cyan-400 font-mono text-base">8.</span>
              <span>Governing Law and Grievance Redressal</span>
            </h2>
            <p>
              These Terms are governed by and construed in accordance with the laws of the <strong className="text-white">{LEGAL_CONFIG.governingLaw}</strong>. Subject to applicable consumer protection laws, courts located in {LEGAL_CONFIG.jurisdictionVenue} shall have competent jurisdiction.
            </p>
            <p>
              For grievances, concerns, or legal queries regarding these Terms, please contact our Grievance Officer:
            </p>
            <div className="p-4 rounded-xl bg-[#121C2F] border border-slate-800 text-xs space-y-1 font-mono">
              <div className="text-white font-bold">{LEGAL_CONFIG.grievanceOfficer.name}</div>
              <div className="text-slate-400">{LEGAL_CONFIG.grievanceOfficer.designation}</div>
              <div className="text-cyan-400">Email: {LEGAL_CONFIG.grievanceOfficer.email}</div>
              <div className="text-slate-500">Acknowledgement: Within {LEGAL_CONFIG.grievanceOfficer.acknowledgementWindow} | Redressal: Within {LEGAL_CONFIG.grievanceOfficer.redressalWindow}</div>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}
