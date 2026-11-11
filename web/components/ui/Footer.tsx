"use client";

import React from "react";
import Link from "next/link";
import { Code2, Github, Shield, Mail, FileText, Cookie } from "lucide-react";
import { LEGAL_CONFIG } from "@/lib/legalConfig";

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="w-full border-t border-slate-800/80 bg-[#070D18] text-slate-400 text-xs mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand Info */}
          <div className="md:col-span-2 space-y-3">
            <Link href="/" className="flex items-center gap-2 group">
              <div className="w-7 h-7 rounded-lg bg-gradient-to-tr from-cyan-500 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-cyan-500/20 group-hover:scale-105 transition-transform">
                <Code2 className="w-4 h-4" />
              </div>
              <span className="font-extrabold text-white text-base tracking-tight font-mono">
                Ready<span className="text-cyan-400">2</span>Code
              </span>
            </Link>
            <p className="text-slate-400 text-xs leading-relaxed max-w-sm">
              Interactive 3D Data Structures &amp; Algorithms platform. Practice with visual algorithm executions, pattern-based progression, and real-time benchmarking.
            </p>
            <div className="text-[11px] text-slate-500 font-mono">
              Educational Platform &bull; Launch Edition
            </div>
          </div>

          {/* Quick Links */}
          <div className="space-y-3">
            <div className="text-xs font-bold uppercase tracking-wider text-slate-300 font-mono">
              Platform
            </div>
            <ul className="space-y-2 text-slate-400">
              <li>
                <Link href="/problems" className="hover:text-cyan-400 transition-colors">
                  Problem Catalog
                </Link>
              </li>
              <li>
                <Link href="/roadmap" className="hover:text-cyan-400 transition-colors">
                  Interactive Roadmap
                </Link>
              </li>
              <li>
                <Link href="/patterns" className="hover:text-cyan-400 transition-colors">
                  DSA Patterns
                </Link>
              </li>
              <li>
                <Link href="/contests" className="hover:text-cyan-400 transition-colors">
                  Contests &amp; Battles
                </Link>
              </li>
            </ul>
          </div>

          {/* Legal & Trust Links */}
          <div className="space-y-3">
            <div className="text-xs font-bold uppercase tracking-wider text-slate-300 font-mono">
              Legal &amp; Trust
            </div>
            <ul className="space-y-2 text-slate-400">
              <li>
                <Link href="/terms" className="hover:text-cyan-400 transition-colors flex items-center gap-1.5">
                  <FileText className="w-3.5 h-3.5" />
                  <span>Terms of Service</span>
                </Link>
              </li>
              <li>
                <Link href="/privacy" className="hover:text-cyan-400 transition-colors flex items-center gap-1.5">
                  <Shield className="w-3.5 h-3.5" />
                  <span>Privacy Policy</span>
                </Link>
              </li>
              <li>
                <Link href="/contact" className="hover:text-cyan-400 transition-colors flex items-center gap-1.5">
                  <Mail className="w-3.5 h-3.5" />
                  <span>Contact &amp; Grievances</span>
                </Link>
              </li>
              <li>
                <Link href="/cookies" className="hover:text-cyan-400 transition-colors flex items-center gap-1.5">
                  <Cookie className="w-3.5 h-3.5" />
                  <span>Cookies &amp; Storage</span>
                </Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-6 border-t border-slate-800/60 flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px] text-slate-500">
          <div>
            &copy; {currentYear} {LEGAL_CONFIG.platformName}. All rights reserved.
          </div>
          <div className="flex items-center gap-6">
            <Link href="/terms" className="hover:text-slate-400 transition-colors">
              Terms
            </Link>
            <Link href="/privacy" className="hover:text-slate-400 transition-colors">
              Privacy
            </Link>
            <Link href="/contact" className="hover:text-slate-400 transition-colors">
              Grievance Redressal
            </Link>
            <a
              href="https://github.com/sayantandutta-18/Ready2Code"
              target="_blank"
              rel="noopener noreferrer"
              className="text-slate-400 hover:text-white transition-colors"
              aria-label="GitHub Repository"
            >
              <Github className="w-4 h-4" />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
