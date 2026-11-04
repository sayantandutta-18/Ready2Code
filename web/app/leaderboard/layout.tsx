import type { Metadata } from "next";
import React from "react";

export const metadata: Metadata = {
  title: "Global Leaderboard & Rankings | Ready2Code",
  description: "View top competitive coders ranked by Elo, XP, and daily consistency streaks.",
  openGraph: {
    title: "Global Leaderboard & Rankings | Ready2Code",
    description: "View top competitive coders ranked by Elo, XP, and daily consistency streaks.",
  },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
