import type { Metadata } from "next";
import React from "react";

export const metadata: Metadata = {
  title: "Algorithmic Patterns Catalog | Ready2Code",
  description: "Learn 15 core algorithmic design patterns with signal recognition quizzes and canonical templates.",
  openGraph: {
    title: "Algorithmic Patterns Catalog | Ready2Code",
    description: "Learn 15 core algorithmic design patterns with signal recognition quizzes and canonical templates.",
  },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
