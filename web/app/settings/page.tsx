"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/authContext";
import { Settings, User, EyeOff, Save, Check, Trash2, AlertTriangle, X, Loader2, ShieldAlert } from "lucide-react";

export default function SettingsPage() {
  const router = useRouter();
  const { user, logout } = useAuth();

  const [username, setUsername] = useState(user?.username || "coder_alex");
  const [displayName, setDisplayName] = useState(user?.display_name || "Alex Vance");
  const [timezone, setTimezone] = useState(user?.timezone || "UTC");
  const [blindMode, setBlindMode] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Deletion modal state
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deleteConfirmationText, setDeleteConfirmationText] = useState("");
  const [isDeleting, setIsDeleting] = useState(false);
  const [deleteError, setDeleteError] = useState<string | null>(null);

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

  const handleDeleteAccount = async () => {
    if (deleteConfirmationText.trim().toUpperCase() !== "DELETE") {
      setDeleteError("Please type 'DELETE' to confirm.");
      return;
    }

    setIsDeleting(true);
    setDeleteError(null);

    try {
      const token = typeof window !== "undefined" ? localStorage.getItem("ready2code_auth_token") : null;
      const res = await fetch("/api/users/me", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
      });

      if (!res.ok) {
        const err = await res.json();
        setDeleteError(err.detail || "Failed to delete account. Please try again.");
        setIsDeleting(false);
        return;
      }

      // Logout and redirect to home
      logout();
      setShowDeleteModal(false);
      router.push("/");
    } catch {
      logout();
      setShowDeleteModal(false);
      router.push("/");
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
            <span>Practice Modes &amp; Preferences</span>
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
            className="px-6 py-2.5 rounded-xl bg-cyan-400 hover:bg-cyan-300 text-slate-950 font-bold text-sm shadow-lg shadow-cyan-500/20 flex items-center gap-2 transition-all cursor-pointer"
          >
            {saved ? <Check className="w-4 h-4 text-slate-950" /> : <Save className="w-4 h-4" />}
            <span>{saved ? "Settings Saved!" : "Save Changes"}</span>
          </button>
        </div>
      </form>

      {/* Danger Zone: Account Deletion (DPDP Act Compliance) */}
      <div className="p-6 rounded-2xl bg-[#161220] border border-rose-500/30 space-y-4 shadow-xl">
        <h2 className="text-sm font-bold uppercase tracking-wider text-rose-400 flex items-center gap-2">
          <ShieldAlert className="w-4 h-4 text-rose-400" />
          <span>Danger Zone &amp; Privacy Rights</span>
        </h2>

        <p className="text-xs text-slate-300 leading-relaxed">
          Under the Digital Personal Data Protection Act, 2023, you have the right to request erasure of your account and personal data. Deleting your account is permanent and cannot be undone.
        </p>

        <div className="pt-2">
          <button
            type="button"
            onClick={() => {
              setDeleteConfirmationText("");
              setDeleteError(null);
              setShowDeleteModal(true);
            }}
            className="px-4 py-2 text-xs font-bold rounded-xl bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/30 flex items-center gap-2 transition-colors cursor-pointer"
          >
            <Trash2 className="w-4 h-4" />
            <span>Delete Account &amp; Personal Data</span>
          </button>
        </div>
      </div>

      {/* Account Deletion Confirmation Modal */}
      {showDeleteModal && (
        <div
          role="dialog"
          aria-modal="true"
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-in fade-in duration-150"
        >
          <div
            className="w-full max-w-md bg-[#121C2F] border border-rose-500/30 rounded-2xl shadow-2xl p-6 relative overflow-hidden text-slate-200 space-y-4"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Close Button */}
            <button
              onClick={() => setShowDeleteModal(false)}
              className="absolute top-4 right-4 p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
              aria-label="Close dialog"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-center justify-center text-rose-400">
                <AlertTriangle className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-white">Permanently Delete Account?</h3>
                <p className="text-xs text-slate-400">This action is irreversible.</p>
              </div>
            </div>

            <div className="p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/20 text-xs text-rose-200 leading-relaxed space-y-1.5">
              <div className="font-semibold text-rose-300">Consequences of account deletion:</div>
              <ul className="list-disc pl-4 space-y-1 text-slate-300 text-[11px]">
                <li>All active session tokens will be permanently revoked immediately.</li>
                <li>Your streak count, XP ledger, and bookmarks will be purged.</li>
                <li>Your personal notes and problem status records will be deleted.</li>
                <li>Security audit logs may be retained for up to 90 days as permitted under law for fraud prevention.</li>
              </ul>
            </div>

            {deleteError && (
              <div className="p-2.5 rounded-lg bg-rose-950/40 border border-rose-500/40 text-rose-300 text-xs">
                {deleteError}
              </div>
            )}

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                Type <span className="font-mono text-rose-400 font-bold">DELETE</span> to confirm:
              </label>
              <input
                type="text"
                value={deleteConfirmationText}
                onChange={(e) => setDeleteConfirmationText(e.target.value)}
                placeholder="DELETE"
                className="w-full bg-[#0B1220] border border-slate-700 rounded-xl px-3 py-2 text-sm text-slate-200 font-mono focus:outline-none focus:border-rose-400"
              />
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setShowDeleteModal(false)}
                className="px-4 py-2 text-xs font-semibold text-slate-400 hover:text-white transition-colors cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="button"
                disabled={isDeleting || deleteConfirmationText.trim().toUpperCase() !== "DELETE"}
                onClick={handleDeleteAccount}
                className="px-4 py-2 text-xs font-bold rounded-xl bg-rose-500 hover:bg-rose-600 text-white shadow-lg shadow-rose-500/20 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1.5 transition-all cursor-pointer"
              >
                {isDeleting ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Trash2 className="w-3.5 h-3.5" />}
                <span>Confirm Permanent Deletion</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
