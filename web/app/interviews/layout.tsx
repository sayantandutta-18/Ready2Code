import type { Metadata } from "next";
import React from "react";

export const metadata: Metadata = {
  title: "Interview Debriefs & Discussions | Ready2Code",
  description: "Real candidate technical interview experiences, system design insights, and salary discussions.",
  openGraph: {
    title: "Interview Debriefs & Discussions | Ready2Code",
    description: "Real candidate technical interview experiences, system design insights, and salary discussions.",
  },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
