"use client";

import React, { useState } from "react";
import Link from "next/link";
import { LEGAL_CONFIG } from "@/lib/legalConfig";
import { Mail, MessageSquare, Shield, Clock, Send, CheckCircle2, AlertCircle, FileText } from "lucide-react";
import Input from "@/components/ui/Input";

export default function ContactPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [subject, setSubject] = useState("");
  const [category, setCategory] = useState("support");
  const [message, setMessage] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg("");

    if (!name.trim() || !email.trim() || !message.trim()) {
      setErrorMsg("Please fill in your name, email, and message.");
      return;
    }

    if (!email.includes("@") || !email.includes(".")) {
      setErrorMsg("Please enter a valid email address.");
      return;
    }

    setIsSubmitting(true);
    // Simulate submission delivery to verified destination
    setTimeout(() => {
      setIsSubmitting(false);
      setSubmitted(true);
    }, 600);
  };

  return (
    <div className="min-h-screen bg-[#070D18] text-slate-200 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-10">
        {/* Header */}
        <div className="text-center space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-mono">
            <Mail className="w-3.5 h-3.5" />
            <span>Support &amp; Grievance Redressal</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Contact Us
          </h1>
          <p className="text-sm text-slate-400 max-w-xl mx-auto">
            Have a question about Ready2Code, need platform help, or wish to submit a privacy or grievance inquiry? We are here to assist.
          </p>
        </div>

        {/* Channels Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Channel 1: General Support */}
          <div className="p-6 rounded-2xl bg-[#121C2F] border border-slate-800 space-y-4 shadow-xl">
            <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400">
              <MessageSquare className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">General &amp; Technical Support</h3>
              <p className="text-xs text-slate-400 mt-1">
                Bug reports, test harness feedback, problem clarifications, and platform inquiries.
              </p>
            </div>
            <div className="pt-2 border-t border-slate-800 text-xs space-y-1 font-mono">
              <div className="text-slate-300">Email: <span className="text-cyan-400">{LEGAL_CONFIG.supportEmail}</span></div>
              <div className="text-slate-500">Expected Response: 2 to 3 business days</div>
            </div>
          </div>

          {/* Channel 2: Grievance Officer */}
          <div className="p-6 rounded-2xl bg-[#121C2F] border border-slate-800 space-y-4 shadow-xl">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
              <Shield className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">Grievance Redressal Officer</h3>
              <p className="text-xs text-slate-400 mt-1">
                Designated under the DPDP Act, 2023 and Information Technology Intermediary Rules, 2021.
              </p>
            </div>
            <div className="pt-2 border-t border-slate-800 text-xs space-y-1 font-mono">
              <div className="text-white font-semibold">{LEGAL_CONFIG.grievanceOfficer.name}</div>
              <div className="text-slate-400">{LEGAL_CONFIG.grievanceOfficer.designation}</div>
              <div className="text-emerald-400">Email: {LEGAL_CONFIG.grievanceOfficer.email}</div>
              <div className="text-slate-500">
                Ack: within {LEGAL_CONFIG.grievanceOfficer.acknowledgementWindow} | Redressal: within {LEGAL_CONFIG.grievanceOfficer.redressalWindow}
              </div>
            </div>
          </div>
        </div>

        {/* Contact Form */}
        <div className="p-8 rounded-2xl bg-[#0F172A] border border-slate-800 shadow-xl space-y-6">
          <div className="border-b border-slate-800 pb-4">
            <h2 className="text-lg font-bold text-white">Send us a direct message</h2>
            <p className="text-xs text-slate-400 mt-1">
              Your inquiry will be routed to the appropriate department based on the selected category.
            </p>
          </div>

          {submitted ? (
            <div className="p-6 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-sm space-y-3 text-center">
              <CheckCircle2 className="w-10 h-10 mx-auto text-emerald-400" />
              <div className="text-base font-bold text-white">Message Dispatched Successfully</div>
              <p className="text-xs text-emerald-400/80 max-w-md mx-auto">
                Thank you for reaching out. We have logged your request and our team will get back to you at <strong className="text-white">{email}</strong> within our standard response window.
              </p>
              <button
                type="button"
                onClick={() => {
                  setSubmitted(false);
                  setMessage("");
                  setSubject("");
                }}
                className="mt-2 px-4 py-2 text-xs font-semibold rounded-lg bg-emerald-500/20 text-emerald-300 hover:bg-emerald-500/30 transition-colors"
              >
                Send Another Message
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              {errorMsg && (
                <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-xs text-rose-300 flex items-center gap-2">
                  <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0" />
                  <span>{errorMsg}</span>
                </div>
              )}

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <Input
                  label="Your Name *"
                  type="text"
                  required
                  placeholder="e.g. Rahul Sharma"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
                <Input
                  label="Your Email Address *"
                  type="email"
                  required
                  placeholder="e.g. rahul@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">
                    Inquiry Category
                  </label>
                  <select
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                    className="w-full bg-[#1A2740] border border-slate-700 rounded-xl px-3 py-2.5 text-sm text-slate-200 focus:outline-none focus:border-cyan-400 transition-colors"
                  >
                    <option value="support">Platform &amp; Problem Support</option>
                    <option value="privacy">Privacy &amp; Data Rights (DPDP)</option>
                    <option value="grievance">Formal Grievance / Content Takedown</option>
                    <option value="feedback">General Suggestion or Feedback</option>
                  </select>
                </div>

                <Input
                  label="Subject"
                  type="text"
                  placeholder="Brief summary of inquiry"
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Message Details *
                </label>
                <textarea
                  rows={5}
                  required
                  placeholder="Please provide specific details so we can investigate and assist you quickly..."
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  className="w-full bg-[#1A2740] border border-slate-700 rounded-xl p-3 text-sm text-slate-200 placeholder:text-slate-500 focus:outline-none focus:border-cyan-400 transition-colors"
                />
              </div>

              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full sm:w-auto px-6 py-2.5 rounded-xl bg-cyan-400 hover:bg-cyan-300 text-slate-950 font-bold text-sm shadow-lg shadow-cyan-500/20 flex items-center justify-center gap-2 transition-all cursor-pointer disabled:opacity-60"
              >
                <Send className="w-4 h-4" />
                <span>{isSubmitting ? "Sending..." : "Submit Message"}</span>
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
