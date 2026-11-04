import type { Metadata } from "next";
import React from "react";

export const metadata: Metadata = {
  title: "Spaced Repetition Review Queue | Ready2Code",
  description: "Retain algorithmic patterns using an SM-2 spaced repetition review schedule.",
  openGraph: {
    title: "Spaced Repetition Review Queue | Ready2Code",
    description: "Retain algorithmic patterns using an SM-2 spaced repetition review schedule.",
  },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
