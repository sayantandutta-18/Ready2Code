import type { Metadata } from "next";
import React from "react";

export const metadata: Metadata = {
  title: "Contests & Live Arena | Ready2Code",
  description: "Participate in live timed competitive programming contests with real-time standings and Elo ratings.",
  openGraph: {
    title: "Contests & Live Arena | Ready2Code",
    description: "Participate in live timed competitive programming contests with real-time standings and Elo ratings.",
  },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
