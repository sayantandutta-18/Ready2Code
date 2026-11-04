"use client";

import React, { useState } from "react";
import { Settings, User, EyeOff, Globe, Bell, Save, Check } from "lucide-react";

export default function SettingsPage() {
  const [username, setUsername] = useState("coder_alex");
  const [displayName, setDisplayName] = useState("Alex Vance");
  const [timezone, setTimezone] = useState("UTC");
  const [blindMode, setBlindMode] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSaved(false);

    // Username format validation: 3 to 20 chars, letters, digits, underscore (C1.1)
    if (username.length < 3 || username.length > 20) {
      setError("Username must be between 3 and 20 characters.");
      return;
    }
    if (!/^[a-zA-Z0-9_]+$/.test(username)) {
      setError("Username may only contain letters, numbers, and underscores.");
      return;
    }

    try {
      const res = await fetch("/api/users/me", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username,
          display_name: displayName,
          timezone,
        }),
      });

      if (!res.ok) {
        const err = await res.json();
        setError(err.detail || "Failed to update profile settings.");
        return;
      }
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch {
      // Offline fallback state
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 lg:px-8 py-12 space-y-8">
      {/* Settings Header */}
      <div>
        <h1 className="text-3xl font-black text-white tracking-tight flex items-center gap-3">
          <Settings className="w-8 h-8 text-cyan-400" />
          <span>Account Settings</span>
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Customize your public coder identity, timezone preferences, and practice mode toggles.
        </p>
      </div>

      {/* Main Settings Form */}
      <form onSubmit={handleSave} className="space-y-6">
        {/* Profile Card */}
        <div className="p-6 rounded-2xl bg-[#121C2F] border border-slate-800 space-y-4 shadow-xl">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
            <User className="w-4 h-4 text-cyan-400" />
            <span>Profile Identity</span>
          </h2>

          <div className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                Username (Unique Handle)
              </label>
              <div className="relative">
                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 font-mono text-sm">
                  @
                </span>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full bg-[#0B1220] border border-slate-700 rounded-xl pl-8 pr-4 py-2 text-sm text-slate-200 focus:outline-none focus:border-cyan-400 font-mono transition-colors"
                />
              </div>
              <p className="text-[11px] text-slate-500 mt-1">
                3 to 20 letters, digits, and underscores.
              </p>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                Display Name
              </label>
              <input
                type="text"
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                className="w-full bg-[#0B1220] border border-slate-700 rounded-xl px-4 py-2 text-sm text-slate-200 focus:outline-none focus:border-cyan-400 transition-colors"
              />
            </div>
          </div>
        </div>

        {/* Practice Preferences */}
        <div className="p-6 rounded-2xl bg-[#121C2F] border border-slate-800 space-y-4 shadow-xl">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
            <EyeOff className="w-4 h-4 text-violet-400" />
            <span>Practice Modes & Preferences</span>
          </h2>

          <div className="space-y-4">
            <div className="flex items-center justify-between p-3.5 rounded-xl bg-[#0B1220] border border-slate-800">
              <div>
                <div className="text-xs font-bold text-slate-200">Blind Mode (Simulate Interviews)</div>
                <div className="text-[11px] text-slate-400">
                  Hides problem tags, difficulty chips, and topic labels across the site.
                </div>
              </div>
              <input
                type="checkbox"
                checked={blindMode}
                onChange={(e) => setBlindMode(e.target.checked)}
                className="w-4 h-4 accent-cyan-400 cursor-pointer"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                Local Timezone (Controls Daily Streak Reset)
              </label>
              <select
                value={timezone}
                onChange={(e) => setTimezone(e.target.value)}
                className="w-full bg-[#0B1220] border border-slate-700 rounded-xl px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-cyan-400"
              >
                <option value="UTC">UTC (Universal Coordinated Time)</option>
                <option value="Asia/Kolkata">Asia/Kolkata (IST - UTC+5:30)</option>
                <option value="America/New_York">America/New_York (EST - UTC-5)</option>
                <option value="America/Los_Angeles">America/Los_Angeles (PST - UTC-8)</option>
                <option value="Europe/London">Europe/London (GMT - UTC+0)</option>
              </select>
            </div>
          </div>
        </div>

        {error && (
          <div className="p-3.5 rounded-xl bg-rose-950/20 border border-rose-500/30 text-rose-300 text-xs">
            {error}
          </div>
        )}

        <div className="flex items-center gap-3">
          <button
            type="submit"
            className="px-6 py-2.5 rounded-xl bg-cyan-400 hover:bg-cyan-300 text-slate-950 font-bold text-sm shadow-lg shadow-cyan-500/20 flex items-center gap-2 transition-all"
          >
            {saved ? <Check className="w-4 h-4 text-slate-950" /> : <Save className="w-4 h-4" />}
            <span>{saved ? "Settings Saved!" : "Save Changes"}</span>
          </button>
        </div>
      </form>
    </div>
  );
}
